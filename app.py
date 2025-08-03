
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {}

    if request.method == 'POST':
        current_stage = request.form['current_stage']
        current_moji = int(request.form['current_moji'])
        current_rate = int(request.form['current_rate'])
        remaining_at_current_rate = int(request.form['remaining_at_current_rate'])
        target_stage = request.form['target_stage']

        form_data = {
            "current_stage": current_stage,
            "current_moji": current_moji,
            "current_rate": current_rate,
            "remaining_at_current_rate": remaining_at_current_rate,
            "target_stage": target_stage
        }

        # 必要な神名文字数
        required_moji_dict = {
            "星1": {"固有1": 30 + 80 + 220, "固有2": 30 + 80 + 340, "固有3": 30 + 80 + 520, "固有4": 30 + 80 + 520 + 200},
            "星2": {"固有1": 80 + 220, "固有2": 80 + 340, "固有3": 80 + 520, "固有4": 80 + 520 + 200},
            "星3": {"固有1": 220, "固有2": 340, "固有3": 520, "固有4": 520 + 200},
            "星4": {"固有1": 120, "固有2": 240, "固有3": 420, "固有4": 420 + 200},
            "固有1": {"固有2": 120, "固有3": 300, "固有4": 300 + 200},
            "固有2": {"固有3": 180, "固有4": 180 + 200},
            "固有3": {"固有4": 200},
        }

        if current_stage not in required_moji_dict or target_stage not in required_moji_dict[current_stage]:
            result = "無効な育成目標です。"
        else:
            required_moji = required_moji_dict[current_stage][target_stage]
            moji_left = required_moji - current_moji

            if moji_left <= 0:
                result = f"すでに{target_stage}に必要な神名文字を所持しています。"
            else:
                total_kakera_needed = 0

                # 現在のレートで処理
                if moji_left > 0:
                    take = min(moji_left, remaining_at_current_rate)
                    total_kakera_needed += take * current_rate
                    moji_left -= take
                    next_rate = current_rate + 1
                else:
                    next_rate = current_rate

                # 残りを次のレートで処理
                while moji_left > 0 and next_rate <= 5:
                    take = min(moji_left, 20)
                    total_kakera_needed += take * next_rate
                    moji_left -= take
                    next_rate += 1

                if moji_left > 0:
                    total_kakera_needed += moji_left * 5

                result = f"{target_stage}までに必要な神名のカケラ:<br><span class='kakera-highlight'>{total_kakera_needed}カケラ</span>"

    return render_template('index.html', result=result, form_data=form_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
