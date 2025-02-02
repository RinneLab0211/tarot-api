import os
from flask import Blueprint

horoscope_bp = Blueprint('horoscope', __name__)

from tarot import tarot_bp
from horoscope import horoscope_bp

# Flaskアプリケーションの作成
main_app = Flask(__name__)

# タロットAPIを登録
main_app.register_blueprint(tarot_bp)

# 占星術APIを登録
main_app.register_blueprint(horoscope_bp)

@main_app.route('/')
def index():
    return "Welcome to the Tarot and Horoscope API! Use /draw or /horoscope for results."

if __name__ == "__main__":
    # Render 用にポート番号を環境変数から取得
    port = int(os.environ.get("PORT", 5000))
    main_app.run(host="0.0.0.0", port=port)
