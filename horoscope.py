# アスペクトの判定（修正バージョン）
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

# 惑星の度数と星座の計算
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

