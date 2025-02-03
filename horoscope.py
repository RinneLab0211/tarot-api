# アスペクトの計算（修正バージョン）
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
    return "なし"

# 惑星間のアスペクトの計算（修正バージョン）
aspects = []
planet_list = list(planet_positions.keys())

for i in range(len(planet_list)):
    for j in range(i + 1, len(planet_list)):
        planet1 = planet_list[i]
        planet2 = planet_list[j]

        # 角度を正しく計算し、0〜180° の範囲に補正
        angle = abs((planet_positions[planet1]["度数"] - planet_positions[planet2]["度数"]) % 360)
        if angle > 180:
            angle = 360 - angle  # 180°を超えないように調整

        # アスペクトを判定
        aspect = get_aspect(angle)
        if aspect != "なし":
            aspects.append(f"{planet1} と {planet2} は {aspect}")
