from flask import Flask
from app import app  # タロットAPI
from horoscope import horoscope_bp  # 占星術API

# Flaskアプリケーションの作成
main_app = Flask(__name__)

# タロットAPIを登録
main_app.register_blueprint(app)

# 占星術APIを登録
main_app.register_blueprint(horoscope_bp)

if __name__ == "__main__":
    main_app.run(host="0.0.0.0", port=5000)
