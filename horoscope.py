import os
from flask import Flask, Blueprint, Response, json, request
from skyfield.api import load

# BSPファイルのURLとパス
BSP_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp"
BSP_FILE = "de421.bsp"

# BSPファイルをダウンロード（存在しない場合のみ）
def download_bsp_file():
    if not os.path.exists(BSP_FILE):
        from urllib.request import urlretrieve
        print("Downloading de421.bsp...")
        urlretrieve(BSP_URL, BSP_FILE)
        print("Download complete.")

# 必要なファイルをダウンロード
download_bsp_file()

# Flaskアプリケーションの作成
horoscope_bp = Blueprint('horoscope', __name__)

@horoscope_bp.route("/horoscope", methods=["GET"])
def horoscope():
    # クエリパラメータを取得
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = float(request.args.get("hour", 12))  # デフォルト値: 12時

    # Skyfieldのデータをロード
    eph = load(BSP_FILE)  # NASAのデータをロード
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

    # 結果を辞書形式に変換（小数点以下2桁に丸める）
    planet_positions = {
        key: (round(position[0].degrees, 2), round(position[1].degrees, 2))
        for key, position in planets.items()
    }

    # JSONレスポンスを作成
    response_json = json.dumps({"惑星の位置": planet_positions}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")
