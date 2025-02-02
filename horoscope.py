from flask import Blueprint, Response, request, json
import swisseph as swe

# 占星術API用のBlueprint
horoscope_bp = Blueprint("horoscope", __name__)

@horoscope_bp.route("/horoscope", methods=["GET"])
def horoscope():
    # クエリパラメータを取得
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = float(request.args.get("hour", 12))  # デフォルト値: 12時
    longitude = float(request.args.get("longitude", 0))  # 経度
    latitude = float(request.args.get("latitude", 0))  # 緯度

    # ユリウス日を計算
    julian_day = swe.julday(year, month, day, hour)

    # 惑星の位置を計算
    planet_positions = {
        swe.get_planet_name(planet): swe.calc_ut(julian_day, planet)[0]
        for planet in range(swe.SUN, swe.PLUTO + 1)
    }

    return Response(json.dumps({"planets": planet_positions}), mimetype="application/json")
