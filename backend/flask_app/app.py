import pandas as pd
import json
from backend.flask_app.utils.mcc_map import convert_mcc_to_category
from pydantic import BaseModel, ValidationError

from openai import OpenAI


def validate_user_info(data: dict) -> bool:
    """
    Validates a JSON dictionary against the UserInfo model.

    Parameters:
        data (dict): The JSON dictionary to validate.

    Returns:
        bool: True if JSON is valid, otherwise False
    """

    class UserInfo(BaseModel):
        username: str
        password: str
        income: float
        age: int
        oldestAccountLengthYears: int
        creditScore: int
        annualFeeWillingness: float

    try:
        # Attempt to parse and validate data with UserInfo model
        _ = UserInfo(**data)
        return True
    except ValidationError as e:
        # Return False and the error message if validation fails
        return False


from flask import Flask, jsonify, request

tx_data = None
user_info = None

# Import credit card data
with open("data/credit-card-data.json", "rb") as file:
    credit_card_info = json.load(file)

app = Flask(__name__)

@app.route("/api/upload-tx-data", methods=["POST"])
def upload_tx_data():
    global tx_data

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected for upload"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    try:
        tx_df = pd.read_csv(file)
        convert_mcc_to_category(tx_df)
        tx_df["Amount"] = tx_df["Amount"].replace("[\$,]", "", regex=True).astype(float)

        tx_data = tx_df.groupby("MCC")["Amount"].sum().sort_values(ascending=False)

        response = {
            "message": "CSV file uploaded successfully!",
            "columns": list(tx_df.columns),
            "row_count": len(tx_df),
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload-user-info", methods=["POST"])
def upload_user_info():
    global user_info

    try:
        data = request.get_json()
        if validate_user_info(data):
            user_info = data
            response = {
                "message": "User data uploaded successfully!",
                "data": user_info
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/recommend")
def recommend():
    global user_info, tx_data

    client = OpenAI()

    with open("prompts/sys-prompt.txt", "r") as file:
        sys_prompt = file.read()

    with open("prompts/rec-prompt.txt", "r") as file:
        rec_prompt = file.read()

    class CreditCardRec(BaseModel):
        rec_reasoning: str
        card_name: str

    class UserInfo(BaseModel):
        global_reasoning: str
        recommendations: list[CreditCardRec]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": rec_prompt.format(
                    user_info=user_info,
                    transactions=tx_data,
                    credit_cards=credit_card_info
                )
            },
        ],
        response_format=UserInfo,
    )

    return jsonify(completion.choices[0].message.parsed.model_dump()), 200


if __name__ == "__main__":
    app.run(debug=True)
