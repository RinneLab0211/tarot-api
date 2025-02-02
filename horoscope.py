from flask import Blueprint, Response, request, json
from skyfield.api import load

# 占星術API用のBlueprint
horoscope_bp = Blueprint("horoscope", __name__)

@horoscope_bp.route("/horoscope", methods=["GET"])
def horoscope():
    # クエリパラメータを取得
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = float(request.args.get("hour", 12))  # デフォルト値: 12時

    # Skyfieldのデータをロード
    eph = load('de421.bsp')  # JPL DE421天体暦を使用
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

    # 結果を辞書形式に変換
    planet_positions = {key: (str(position[0].degrees), str(position[1].degrees))
                        for key, position in planets.items()}

    response_json = json.dumps({"planets": planet_positions}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")
