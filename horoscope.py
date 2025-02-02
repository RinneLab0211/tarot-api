import os
from flask import Flask, Blueprint, Response, json, request
from skyfield.api import load, Topos
import math

# NASAの惑星データ（BSPファイル）
BSP_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp"
BSP_FILE = "de421.bsp"

# BSPファイルをダウンロード（存在しない場合のみ）
def download_bsp_file():
    if not os.path.exists(BSP_FILE):
        from urllib.request import urlretrieve
        print("Downloading de421.bsp...")
        urlretrieve(BSP_URL, BSP_FILE)
        print("Download complete.")

download_bsp_file()

# 12星座（サイン）の定義
ZODIAC_SIGNS = [
    ("牡羊座", 0, 30), ("牡牛座", 30, 60), ("双子座", 60, 90),
    ("蟹座", 90, 120), ("獅子座", 120, 150), ("乙女座", 150, 180),
    ("天秤座", 180, 210), ("蠍座", 210, 240), ("射手座", 240, 270),
    ("山羊座", 270, 300), ("水瓶座", 300, 330), ("魚座", 330, 360)
]

# 星座（サイン）の計算
def get_zodiac_sign(degree):
    for sign, start, end in ZODIAC_SIGNS:
        if start <= degree < end:
            return sign
    return "不明"

# アスペクトの計算
def get_aspect(angle):
    aspects = {
        "コンジャンクション (0°)": 0,
        "オポジション (180°)": 180,
        "トライン (120°)": 120,
        "スクエア (90°)": 90,
        "セクスタイル (60°)": 60
    }
    for name, aspect_angle in aspects.items():
        if abs(angle - aspect_angle) <= 6:  # 許容誤差 ±6°
            return name
    return "なし"

# Flaskアプリケーションの作成
horoscope_bp = Blueprint('horoscope', __name__)

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
    eph = load(BSP_FILE)
    ts = load.timescale()

    # ユーザーが指定した日時を計算
    t = ts.utc(year, month, day, int(hour), int((hour % 1) * 60))

    # 惑星の位置を計算（太陽・月・全惑星）
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

    # 惑星の度数と星座
    planet_positions = {}
    for name, position in planets.items():
        degree = round(position[0].degrees, 2)  # 黄経の度数
        zodiac = get_zodiac_sign(degree)  # 12星座の計算
        planet_positions[name] = {"度数": degree, "星座": zodiac}

    # 惑星間のアスペクトの計算
    aspects = []
    planet_list = list(planet_positions.keys())
    for i in range(len(planet_list)):
        for j in range(i + 1, len(planet_list)):
            planet1 = planet_list[i]
            planet2 = planet_list[j]
            angle = abs(planet_positions[planet1]["度数"] - planet_positions[planet2]["度数"])
            if angle > 180:
                angle = 360 - angle  # 0°〜180°の範囲に調整
            aspect = get_aspect(angle)
            if aspect != "なし":
                aspects.append(f"{planet1} と {planet2} は {aspect}")

    # JSONレスポンスを作成
    response_data = {
        "惑星の位置": planet_positions,
        "アスペクト": aspects
    }
    return Response(json.dumps(response_data, ensure_ascii=False), content_type="application/json; charset=utf-8")
