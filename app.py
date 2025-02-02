import os
from flask import Flask
from tarot import tarot_bp
from horoscope import horoscope_bp

app = Flask(__name__)

# APIを登録
app.register_blueprint(tarot_bp)
app.register_blueprint(horoscope_bp)

@app.route('/')
def index():
    return "Welcome to the Tarot and Horoscope API! Use /draw or /horoscope for results."

if __name__ == "__main__":
    # Render用にポート番号を環境変数から取得
    port = int(os.environ.get("PORT", 10000))  # ← ここを変更！
    app.run(host="0.0.0.0", port=port)
