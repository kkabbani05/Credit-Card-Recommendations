import pandas as pd
import json
from io import StringIO
from mcc_map import convert_mcc_to_category
from pydantic import BaseModel, ValidationError
from openai import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from urllib.parse import unquote
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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
        tx_df["Amount"] = tx_df["Amount"].replace(r"[\$,]", "", regex=True).astype(float)
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
        client = OpenAI(api_key="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")
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

@app.route("/api/graph", methods=["POST"])
def graph():
    mcc_map = {5812: 'dining', 5813: 'dining', 5814: 'dining', 5820: 'dining', 5462: 'dining', 7832: 'entertainment',
           7922: 'entertainment', 7929: 'entertainment', 7933: 'entertainment', 7941: 'entertainment',
           7991: 'entertainment', 7992: 'entertainment', 7996: 'entertainment', 7997: 'entertainment',
           7998: 'entertainment', 7999: 'entertainment', 7800: 'entertainment', 7841: 'entertainment', 4900: 'gas',
           5541: 'gas', 5542: 'gas', 5172: 'gas', 9752: 'gas', 5411: 'grocery', 5300: 'grocery', 5715: 'grocery',
           5422: 'grocery', 5451: 'grocery', 3501: 'hotel', 3502: 'hotel', 3503: 'hotel', 3504: 'hotel', 3505: 'hotel',
           3506: 'hotel', 3507: 'hotel', 3508: 'hotel', 3509: 'hotel', 3510: 'hotel', 3511: 'hotel', 3512: 'hotel',
           3513: 'hotel', 3514: 'hotel', 3515: 'hotel', 3516: 'hotel', 3517: 'hotel', 3518: 'hotel', 3519: 'hotel',
           3520: 'hotel', 3521: 'hotel', 3522: 'hotel', 3523: 'hotel', 3524: 'hotel', 3525: 'hotel', 3526: 'hotel',
           3527: 'hotel', 3528: 'hotel', 3529: 'hotel', 3530: 'hotel', 3531: 'hotel', 3532: 'hotel', 3533: 'hotel',
           3534: 'hotel', 3535: 'hotel', 3536: 'hotel', 3537: 'hotel', 3538: 'hotel', 3539: 'hotel', 3540: 'hotel',
           3541: 'hotel', 3542: 'hotel', 3543: 'hotel', 3544: 'hotel', 3545: 'hotel', 3546: 'hotel', 3547: 'hotel',
           3548: 'hotel', 3549: 'hotel', 3550: 'hotel', 3551: 'hotel', 3552: 'hotel', 3553: 'hotel', 3554: 'hotel',
           3555: 'hotel', 3556: 'hotel', 3557: 'hotel', 3558: 'hotel', 3559: 'hotel', 3560: 'hotel', 3561: 'hotel',
           3562: 'hotel', 3563: 'hotel', 3564: 'hotel', 3565: 'hotel', 3566: 'hotel', 3567: 'hotel', 3568: 'hotel',
           3569: 'hotel', 3570: 'hotel', 3571: 'hotel', 3572: 'hotel', 3573: 'hotel', 3574: 'hotel', 3575: 'hotel',
           3576: 'hotel', 3577: 'hotel', 3578: 'hotel', 3579: 'hotel', 3580: 'hotel', 3581: 'hotel', 3582: 'hotel',
           3583: 'hotel', 3584: 'hotel', 3585: 'hotel', 3586: 'hotel', 3587: 'hotel', 3588: 'hotel', 3589: 'hotel',
           3590: 'hotel', 3591: 'hotel', 3592: 'hotel', 3593: 'hotel', 3594: 'hotel', 3595: 'hotel', 3596: 'hotel',
           3597: 'hotel', 3598: 'hotel', 3599: 'hotel', 3600: 'hotel', 3601: 'hotel', 3602: 'hotel', 3603: 'hotel',
           3604: 'hotel', 3605: 'hotel', 3606: 'hotel', 3607: 'hotel', 3608: 'hotel', 3609: 'hotel', 3610: 'hotel',
           3611: 'hotel', 3612: 'hotel', 3613: 'hotel', 3614: 'hotel', 3615: 'hotel', 3616: 'hotel', 3617: 'hotel',
           3618: 'hotel', 3619: 'hotel', 3620: 'hotel', 3621: 'hotel', 3622: 'hotel', 3623: 'hotel', 3624: 'hotel',
           3625: 'hotel', 3626: 'hotel', 3627: 'hotel', 3628: 'hotel', 3629: 'hotel', 3630: 'hotel', 3631: 'hotel',
           3632: 'hotel', 3633: 'hotel', 3634: 'hotel', 3635: 'hotel', 3636: 'hotel', 3637: 'hotel', 3638: 'hotel',
           3639: 'hotel', 3640: 'hotel', 3641: 'hotel', 3642: 'hotel', 3643: 'hotel', 3644: 'hotel', 3645: 'hotel',
           3646: 'hotel', 3647: 'hotel', 3648: 'hotel', 3649: 'hotel', 3650: 'hotel', 3651: 'hotel', 3652: 'hotel',
           3653: 'hotel', 3654: 'hotel', 3655: 'hotel', 3656: 'hotel', 3657: 'hotel', 3658: 'hotel', 3659: 'hotel',
           3660: 'hotel', 3661: 'hotel', 3662: 'hotel', 3663: 'hotel', 3664: 'hotel', 3665: 'hotel', 3666: 'hotel',
           3667: 'hotel', 3668: 'hotel', 3669: 'hotel', 3670: 'hotel', 3671: 'hotel', 3672: 'hotel', 3673: 'hotel',
           3674: 'hotel', 3675: 'hotel', 3676: 'hotel', 3677: 'hotel', 3678: 'hotel', 3679: 'hotel', 3680: 'hotel',
           3681: 'hotel', 3682: 'hotel', 3683: 'hotel', 3684: 'hotel', 3685: 'hotel', 3686: 'hotel', 3687: 'hotel',
           3688: 'hotel', 3689: 'hotel', 3690: 'hotel', 3691: 'hotel', 3692: 'hotel', 3693: 'hotel', 3694: 'hotel',
           3695: 'hotel', 3696: 'hotel', 3697: 'hotel', 3698: 'hotel', 3699: 'hotel', 3700: 'hotel', 3701: 'hotel',
           3702: 'hotel', 3703: 'hotel', 3704: 'hotel', 3705: 'hotel', 3706: 'hotel', 3707: 'hotel', 3708: 'hotel',
           3709: 'hotel', 3710: 'hotel', 3711: 'hotel', 3712: 'hotel', 3713: 'hotel', 3714: 'hotel', 3715: 'hotel',
           3716: 'hotel', 3717: 'hotel', 3718: 'hotel', 3719: 'hotel', 3720: 'hotel', 3721: 'hotel', 3722: 'hotel',
           3723: 'hotel', 3724: 'hotel', 3725: 'hotel', 3726: 'hotel', 3727: 'hotel', 3728: 'hotel', 3729: 'hotel',
           3730: 'hotel', 3731: 'hotel', 3732: 'hotel', 3733: 'hotel', 3734: 'hotel', 3735: 'hotel', 3736: 'hotel',
           3737: 'hotel', 3738: 'hotel', 3739: 'hotel', 3740: 'hotel', 3741: 'hotel', 3742: 'hotel', 3743: 'hotel',
           3744: 'hotel', 3745: 'hotel', 3746: 'hotel', 3747: 'hotel', 3748: 'hotel', 3749: 'hotel', 3750: 'hotel',
           3751: 'hotel', 3752: 'hotel', 3753: 'hotel', 3754: 'hotel', 3755: 'hotel', 3756: 'hotel', 3757: 'hotel',
           3758: 'hotel', 3759: 'hotel', 3760: 'hotel', 3761: 'hotel', 3762: 'hotel', 3763: 'hotel', 3764: 'hotel',
           3765: 'hotel', 3766: 'hotel', 3767: 'hotel', 3768: 'hotel', 3769: 'hotel', 3770: 'hotel', 3771: 'hotel',
           3772: 'hotel', 3773: 'hotel', 3774: 'hotel', 3775: 'hotel', 3776: 'hotel', 3777: 'hotel', 3778: 'hotel',
           3779: 'hotel', 3780: 'hotel', 3781: 'hotel', 3782: 'hotel', 3783: 'hotel', 3784: 'hotel', 3785: 'hotel',
           3786: 'hotel', 3787: 'hotel', 3788: 'hotel', 3789: 'hotel', 3790: 'hotel', 3791: 'hotel', 3792: 'hotel',
           3793: 'hotel', 3794: 'hotel', 3795: 'hotel', 3796: 'hotel', 3797: 'hotel', 3798: 'hotel', 3799: 'hotel',
           3800: 'hotel', 3801: 'hotel', 3802: 'hotel', 3803: 'hotel', 3804: 'hotel', 3805: 'hotel', 3806: 'hotel',
           3807: 'hotel', 3808: 'hotel', 3809: 'hotel', 3810: 'hotel', 3811: 'hotel', 3812: 'hotel', 3813: 'hotel',
           3814: 'hotel', 3815: 'hotel', 3816: 'hotel', 3817: 'hotel', 3818: 'hotel', 3819: 'hotel', 3820: 'hotel',
           3821: 'hotel', 3822: 'hotel', 3823: 'hotel', 3824: 'hotel', 3825: 'hotel', 3826: 'hotel', 3827: 'hotel',
           3828: 'hotel', 3829: 'hotel', 3830: 'hotel', 7011: 'hotel', 5815: 'onlineDining', 5816: 'onlineDining',
           5961: 'onlineGrocery', 3351: 'rentalCar', 3352: 'rentalCar', 3353: 'rentalCar', 3354: 'rentalCar',
           3355: 'rentalCar', 3356: 'rentalCar', 3357: 'rentalCar', 3358: 'rentalCar', 3359: 'rentalCar',
           3360: 'rentalCar', 7512: 'rentalCar', 5310: 'retail', 5311: 'retail', 5331: 'retail', 5399: 'retail',
           5611: 'retail', 5621: 'retail', 5631: 'retail', 5641: 'retail', 5651: 'retail', 5655: 'retail',
           5661: 'retail', 5681: 'retail', 5691: 'retail', 5697: 'retail', 5698: 'retail', 5699: 'retail',
           5712: 'retail', 5713: 'retail', 5714: 'retail', 5718: 'retail', 5719: 'retail', 5722: 'retail',
           5732: 'retail', 5733: 'retail', 5734: 'retail', 5735: 'retail', 5912: 'retail', 5940: 'retail',
           5941: 'retail', 5942: 'retail', 5943: 'retail', 5944: 'retail', 5945: 'retail', 5946: 'retail',
           5947: 'retail', 5948: 'retail', 5949: 'retail', 5950: 'retail', 5964: 'retail', 5965: 'retail',
           5969: 'retail', 5970: 'retail', 5971: 'retail', 5972: 'retail', 5973: 'retail', 5975: 'retail',
           5976: 'retail', 5977: 'retail', 5978: 'retail', 5983: 'retail', 5992: 'retail', 5993: 'retail',
           5994: 'retail', 5995: 'retail', 5996: 'retail', 5997: 'retail', 5998: 'retail', 5999: 'retail',
           4899: 'streaming', 5968: 'streaming', 4111: 'transit', 4112: 'transit', 4121: 'transit', 4131: 'transit',
           4784: 'transit', 7523: 'transit', 4011: 'transit', 4789: 'transit', 3000: 'travel', 3001: 'travel',
           3002: 'travel', 3003: 'travel', 3004: 'travel', 3005: 'travel', 3006: 'travel', 3007: 'travel',
           3008: 'travel', 3009: 'travel', 3010: 'travel', 3011: 'travel', 3012: 'travel', 3013: 'travel',
           3014: 'travel', 3015: 'travel', 3016: 'travel', 3017: 'travel', 3018: 'travel', 3020: 'travel',
           3021: 'travel', 3022: 'travel', 3023: 'travel', 3024: 'travel', 3025: 'travel', 3026: 'travel',
           3027: 'travel', 3028: 'travel', 3029: 'travel', 3030: 'travel', 3031: 'travel', 3032: 'travel',
           3033: 'travel', 3034: 'travel', 3035: 'travel', 3036: 'travel', 3037: 'travel', 3038: 'travel',
           3039: 'travel', 3040: 'travel', 3041: 'travel', 3042: 'travel', 3043: 'travel', 3044: 'travel',
           3045: 'travel', 3046: 'travel', 3051: 'travel', 3061: 'travel', 3075: 'travel', 3256: 'travel',
           4411: 'travel', 4511: 'travel', 4722: 'travel', 5962: 'travel'}

    try:
        data = request.json
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        transaction_info = data.get('transaction_info')
        rec_info = data.get('rec_info')

        if not transaction_info or not rec_info:
            return jsonify({"error": "Missing required data"}), 400

        # Convert to DataFrame and process
        tx_df = pd.DataFrame(transaction_info)
        print(tx_df.head())
        # Clean amount column - remove $ and convert to float
        tx_df['Amount'] = tx_df['Amount'].str.replace('$', '').str.replace(',', '').astype(float)

        # Map MCC to category
        tx_df['MCC'] = pd.to_numeric(tx_df['MCC'], errors='coerce')

        tx_df["MCC"] = tx_df["MCC"].map(mcc_map).fillna("other")
        tx_data = tx_df.groupby(['Year', 'MCC'])['Amount'].sum()

        points_per_card_per_year = {}
        best_card_per_category_per_year = {}

        # Calculate points for each card
        for rec in rec_info:
            card_info = rec['card_info']
            points_dict = card_info['rewards']['pointsPerDollar']
            card_name = card_info['cardName']

            # logging.debug(f"Processing card: {card_name}")
            # logging.debug(f"Points Per Dollar: {points_dict}")

            for (year, mcc), amount in tx_data.items():
                if amount <= 0:  # Skip negative amounts
                    continue

                category = mcc  # Already a string
                multiplier = points_dict.get(category, points_dict.get('other', 0))
                points_earned = (amount * multiplier)

                # logging.debug(f"Year: {year}, Category: {category}, Amount: {amount}, Multiplier: {multiplier}, Points Earned: {points_earned}")

                # Update points per card per year
                points_per_card_per_year.setdefault(year, {}).setdefault(card_name, 0)
                points_per_card_per_year[year][card_name] += points_earned

                # Update best card per category per year
                if year not in best_card_per_category_per_year:
                    best_card_per_category_per_year[year] = {}

                current_best = best_card_per_category_per_year[year].get(category, {'points': 0})
                if points_earned > current_best['points']:
                    best_card_per_category_per_year[year][category] = {
                        'card_name': card_name,
                        'points': points_earned
                    }

        # Calculate total points per year
        total_points_per_year = {
            year: sum(category_info['points'] for category_info in categories.values())
            for year, categories in best_card_per_category_per_year.items()
        }

        # Log the final calculated points
        # logging.debug(f"Points per card per year: {points_per_card_per_year}")
        # logging.debug(f"Best card per category per year: {best_card_per_category_per_year}")
        # logging.debug(f"Total points per year: {total_points_per_year}")

        return jsonify({
            'points_per_card_per_year': points_per_card_per_year,
            'best_card_per_category_per_year': best_card_per_category_per_year,
            'total_points_per_year': total_points_per_year
        }), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
if __name__ == "__main__":
    app.run(port=8000, debug=True)