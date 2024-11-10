import pandas as pd
import json
from io import StringIO
from mcc_map import convert_mcc_to_category
from pydantic import BaseModel, ValidationError
from openai import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS


class UserInfo(BaseModel):
    username: str
    password: str
    income: float
    age: int
    oldestAccountLengthYears: int
    creditScore: int
    annualFeeWillingness: float


class CreditCardRec(BaseModel):
    rec_reasoning: str
    card_name: str


class RecommendationResponse(BaseModel):
    global_reasoning: str
    recommendations: list[CreditCardRec]


app = Flask(__name__)
CORS(app)

# Import credit card data
with open("data/credit-card-data.json", "rb") as file:
    credit_card_info = json.load(file)


@app.route("/api/recommendations", methods=["POST"])  # Add OPTIONS method
def recommend():
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    try:
        # Parse JSON body
        data = request.get_json()

        # Add debug logging
        print("Received request data:", data)  # Debug print

        # Extract transactions CSV string
        transactions_csv = data.get("transactions_csv")
        if not transactions_csv:
            return jsonify({"error": "Missing 'transactions_csv' in request body"}), 400

        # Convert list of dictionaries to CSV string
        csv_data = pd.DataFrame(transactions_csv).to_csv(index=False)

        # Read CSV data from string
        tx_df = pd.read_csv(StringIO(csv_data))

        # Process transaction data
        convert_mcc_to_category(tx_df)
        tx_df["Amount"] = tx_df["Amount"].replace("[\$,]", "", regex=True).astype(float)
        tx_data = tx_df.groupby("MCC")["Amount"].sum().sort_values(ascending=False)

        # Extract and validate user info
        user_info = data.get("user_info")
        if not user_info:
            return jsonify({"error": "Missing 'user_info' in request body"}), 400

        user_info = json.loads(json.dumps(user_info))  # Ensure it's a proper dict
        validated_user_info = UserInfo(**user_info)  # Validate user info

        # Load prompts
        with open("prompts/sys-prompt.txt", "r") as f:
            sys_prompt = f.read()
        with open("prompts/rec-prompt.txt", "r") as f:
            rec_prompt = f.read()

        # Get recommendations
        client = OpenAI()
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": rec_prompt.format(
                    user_info=user_info,
                    transactions=tx_data.to_dict(),
                    credit_cards=credit_card_info
                )}
            ],
            response_format=RecommendationResponse,
        )

        rec_json = completion.choices[0].message.parsed.model_dump()
        for rec in rec_json["recommendations"]:
            card_name = rec["card_name"]
            rec["card_info"] = credit_card_info[card_name]

        return jsonify(rec_json), 200

    except ValidationError as e:
        return jsonify({"error": "Invalid user info format", "details": str(e)}), 400
    except pd.errors.EmptyDataError:
        return jsonify({"error": "Empty CSV data"}), 400
    except pd.errors.ParserError:
        return jsonify({"error": "Invalid CSV format"}), 400
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=8000, debug=True)