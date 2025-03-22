from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        current_stage = request.form['current_stage']
        current_moji = int(request.form['current_moji'])
        purchased_moji = int(request.form['purchased_moji'])
        purchased_rate = int(request.form['purchased_rate'])
        target_stage = request.form['target_stage']

        required_moji_dict = {
            "星1": {"固有1": 30 + 80 + 220, "固有2": 30 + 80 + 340, "固有3": 30 + 80 + 520},
            "星2": {"固有1": 80 + 220, "固有2": 80 + 340, "固有3": 80 + 520},
            "星3": {"固有1": 220, "固有2": 340, "固有3": 520},
            "星4": {"固有1": 120, "固有2": 240, "固有3": 420},
            "固有1": {"固有2": 120, "固有3": 300},
            "固有2": {"固有3": 180},
        }

        if current_stage not in required_moji_dict or target_stage not in required_moji_dict[current_stage]:
            result = "無効な育成目標です。"
        else:
            required_moji = required_moji_dict[current_stage][target_stage]
            remaining_moji = required_moji - current_moji

            if remaining_moji <= 0:
                result = f"すでに{target_stage}に必要な神名文字を所持しています。"
            else:
                rate_thresholds = [20, 40, 60, 80, 100]
                rates = [1, 2, 3, 4, 5]
                total_kakera_needed = 0
                moji_purchased = purchased_moji

                for i in range(purchased_rate, len(rate_thresholds)):
                    if remaining_moji > 0:
                        purchasable = min(rate_thresholds[i] - moji_purchased, remaining_moji)
                        total_kakera_needed += purchasable * rates[i]
                        moji_purchased += purchasable
                        remaining_moji -= purchasable

                if remaining_moji > 0:
                    total_kakera_needed += remaining_moji * 5

                result = f"{target_stage}までに必要な神名のカケラ: {total_kakera_needed}カケラ"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
