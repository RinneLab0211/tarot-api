import os
from flask import Flask, Blueprint, Response, json, request  # ✅ `request` を追加！
from skyfield.api import load

# BSPファイルを確実にダウンロード
bsp_path = "de421.bsp"
if not os.path.exists(bsp_path):
    from urllib.request import urlretrieve
    urlretrieve("https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de421.bsp", bsp_path)

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
    eph = load(bsp_path)  # 修正: ファイルが確実にあるか確認！
    ts = load.timescale()

    # ユーザーが指定した日時を計算
    t = ts.utc(year, month, day, int(hour), int((hour % 1) * 60))

    # 惑星の位置を計算
    planets = {
        "Mercury": eph['mercury'].at(t).ecliptic_latlon(),
        "Venus": eph['venus'].at(t).ecliptic_latlon(),
        "Mars": eph['mars'].at(t).ecliptic_latlon(),
        "Jupiter": eph['jupiter barycenter'].at(t).ecliptic_latlon(),
        "Saturn": eph['saturn barycenter'].at(t).ecliptic_latlon()
    }

    # 英語名 → 日本語名のマッピング
    planet_names = {
        "Mercury": "水星",
        "Venus": "金星",
        "Mars": "火星",
        "Jupiter": "木星",
        "Saturn": "土星"
    }

    # 結果を辞書形式に変換（日本語名を使用、小数点以下2桁に丸める）
    planet_positions = {
        planet_names[key]: (round(position[0].degrees, 2), round(position[1].degrees, 2))
        for key, position in planets.items()
    }

    # JSONレスポンスを作成
    response_json = json.dumps({"惑星の位置": planet_positions}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")
