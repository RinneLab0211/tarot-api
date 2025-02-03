from flask import Blueprint, Response, json, request  # ✅ Blueprintを正しくインポート
from skyfield.api import load
import os
import math

# Flaskアプリケーションの作成
horoscope_bp = Blueprint('horoscope', __name__)

# 12星座（サイン）の定義
ZODIAC_SIGNS = [
    ("牡羊座", 0, 30), ("牡牛座", 30, 60), ("双子座", 60, 90),
    ("蟹座", 90, 120), ("獅子座", 120, 150), ("乙女座", 150, 180),
    ("天秤座", 180, 210), ("蠍座", 210, 240), ("射手座", 240, 270),
    ("山羊座", 270, 300), ("水瓶座", 300, 330), ("魚座", 330, 360)
]

# 星座（サイン）の計算関数
def get_zodiac_sign(degree):
    for sign, start, end in ZODIAC_SIGNS:
        if start <= degree < end:
            return sign
    return "不明"

# アスペクトの判定関数
def get_aspect(angle):
    aspects = {
        "コンジャンクション (0°)": 0,
        "オポジション (180°)": 180,
        "トライン (120°)": 120,
        "スクエア (90°)": 90,
        "セクスタイル (60°)": 60
    }
    orb = 6  # 許容誤差（調整可能）

    for name, aspect_angle in aspects.items():
        if abs(angle - aspect_angle) <= orb:
            return name
    return None  # なしの場合は None を返す

@horoscope_bp.route("/horoscope", methods=["GET"])
def horoscope():
    # クエリパラメータを取得
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = float(request.args.get("hour", 12))  # デフォルト値: 12時
    lat = float(request.args.get("lat", 35.0))  # デフォルト: 東京の緯度
    lon = float(request.args.get("lon", 139.0)) # デフォルト: 東京の経度

    # Skyfieldのデータをロード
    BSP_FILE = "de421.bsp"  # BSPファイルのパス
    eph = load(BSP_FILE)
    ts = load.timescale()

    # ユーザーが指定した日時を計算
    t = ts.utc(year, month, day, int(hour), int((hour % 1) * 60))

    # 🔹 `planets` の定義を関数の中に移動
    planets = {
        "太陽": eph['sun'].at(t).ecliptic_latlon(),
        "月": eph['moon'].at(t).ecliptic_latlon(),
        "水星": eph['mercury'].at(t).ecliptic_latlon(),
        "金星": eph['venus'].at(t).ecliptic_latlon(),
        "火星": eph['mars'].at(t).ecliptic_latlon(),
        "木星": eph['jupiter barycenter'].at(t).ecliptic_latlon(),
        "土星": eph['saturn barycenter'].at(t).ecliptic_latlon(),
        "天王星": eph['uranus barycenter'].at(t).ecliptic_latlon(),
        "海王星": eph['neptune barycenter'].at(t).ecliptic_latlon(),
        "冥王星": eph['pluto barycenter'].at(t).ecliptic_latlon()
    }

    # 🔹 惑星の度数と星座の計算（`planets` の定義の後に移動）
    planet_positions = {}
    for name, position in planets.items():
        degree = position[0].degrees % 360  # 0〜360度に正規化
        degree = round(degree, 2)  # 小数点2桁まで丸める
        zodiac = get_zodiac_sign(degree)  # 12星座の計算
        planet_positions[name] = {"度数": degree, "星座": zodiac}

    # 🔹 ここで `planet_positions` を定義した後に `planet_list` を作成
    planet_list = list(planet_positions.keys())

    # 🔹 惑星間のアスペクトの計算（修正バージョン）
    aspects = []
    for i in range(len(planet_list)):
        for j in range(i + 1, len(planet_list)):
            planet1 = planet_list[i]
            planet2 = planet_list[j]

            # 角度を正しく計算し、0〜180° の範囲に補正
            angle = abs((planet_positions[planet1]["度数"] - planet_positions[planet2]["度数"]) % 360)
            if angle > 180:
                angle = 360 - angle  # 180°を超えないように調整

            # アスペクトを判定
            aspect_name = get_aspect(angle)
            if aspect_name:  # None でなければ追加
                aspects.append(f"{planet1} と {planet2} は {aspect_name}")

    # JSONレスポンスを作成
    response_data = {
        "惑星の位置": planet_positions,
        "アスペクト": aspects
    }
    return Response(json.dumps(response_data, ensure_ascii=False), content_type="application/json; charset=utf-8")
