from flask import Blueprint, Response, json, request
from skyfield.api import load
import os

# 🔹 グローバル変数として NASA のデータを 1 回ロード（毎回ロードしないようにする）
BSP_FILE = "de421.bsp"
eph = load(BSP_FILE)  # ここで 1 回だけロード
ts = load.timescale()

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

# アスペクトの判定関数（修正）
def get_aspect(angle, orb=6):
    aspects = {
        "コンジャンクション (0°)": 0,
        "オポジション (180°)": 180,
        "トライン (120°)": 120,
        "スクエア (90°)": 90,
        "セクスタイル (60°)": 60
    }

    for name, aspect_angle in aspects.items():
        if abs(angle - aspect_angle) <= orb:
            return name
    return None  # アスペクトなし

@horoscope_bp.route("/horoscope", methods=["GET"])
def horoscope():
    # クエリパラメータを取得
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = float(request.args.get("hour", 12))  # デフォルト値: 12時

    # NASA のデータはグローバル変数から取得
    t = ts.utc(year, month, day, int(hour), int((hour % 1) * 60))

    # 惑星データの取得
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

    # 惑星の度数と星座の計算
    planet_positions = {}
    for name, position in planets.items():
        degree = position[0].degrees % 360  # 0〜360度に正規化
        degree = round(degree, 2)  # 小数点2桁まで丸める
        zodiac = get_zodiac_sign(degree)  # 12星座の計算
        planet_positions[name] = {"度数": degree, "星座": zodiac}

    # 🔹 ここで `planet_positions` を定義した後に `planet_list` を作成
    planet_list = list(planet_positions.keys())

    # 🔹 惑星間のアスペクトの計算（修正）
    aspects = []
    for i in range(len(planet_list)):
        for j in range(i + 1, len(planet_list)):
            planet1 = planet_list[i]
            planet2 = planet_list[j]

            # 🔹 角度を正しく計算し、0〜180° の範囲に補正
            angle = abs(planet_positions[planet1]["度数"] - planet_positions[planet2]["度数"])
            angle = min(angle, 360 - angle)  # 180°を超えないように調整

            # 🔹 アスペクトを判定
            aspect_name = get_aspect(angle, orb=6)  # 許容誤差を 6° に設定
            if aspect_name:  # None でなければ追加
                aspects.append(f"{planet1} と {planet2} は {aspect_name}")

    # JSONレスポンスを作成
    response_data = {
        "惑星の位置": planet_positions,
        "アスペクト": aspects
    }
    return Response(json.dumps(response_data, ensure_ascii=False), content_type="application/json; charset=utf-8")
