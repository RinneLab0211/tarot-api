git add tarot.py
git commit -m "Add tarot.py"
git push origin main

from flask import Blueprint, Response, json
import random

# タロットAPI用の Blueprint を作成
tarot_bp = Blueprint("tarot", __name__)

# 78枚のタロットカードデッキ
tarot_deck = [
    # 大アルカナ（22枚）
    "愚者", "魔術師", "女教皇", "女帝", "皇帝", "法王", "恋人", "戦車", "力", "隠者",
    "運命の輪", "正義", "吊るされた男", "死神", "節制", "悪魔", "塔", "星", "月", "太陽",
    "審判", "世界",
    
    # 小アルカナ（56枚）
    # ワンド（14枚）
    "ワンドのエース", "ワンドの2", "ワンドの3", "ワンドの4", "ワンドの5", "ワンドの6",
    "ワンドの7", "ワンドの8", "ワンドの9", "ワンドの10",
    "ワンドのペイジ", "ワンドのナイト", "ワンドのクイーン", "ワンドのキング",

    # カップ（14枚）
    "カップのエース", "カップの2", "カップの3", "カップの4", "カップの5", "カップの6",
    "カップの7", "カップの8", "カップの9", "カップの10",
    "カップのペイジ", "カップのナイト", "カップのクイーン", "カップのキング",

    # ソード（14枚）
    "ソードのエース", "ソードの2", "ソードの3", "ソードの4", "ソードの5", "ソードの6",
    "ソードの7", "ソードの8", "ソードの9", "ソードの10",
    "ソードのペイジ", "ソードのナイト", "ソードのクイーン", "ソードのキング",

    # ペンタクル（14枚）
    "ペンタクルのエース", "ペンタクルの2", "ペンタクルの3", "ペンタクルの4", "ペンタクルの5",
    "ペンタクルの6", "ペンタクルの7", "ペンタクルの8", "ペンタクルの9", "ペンタクルの10",
    "ペンタクルのペイジ", "ペンタクルのナイト", "ペンタクルのクイーン", "ペンタクルのキング"
]

# 正位置・逆位置をランダムで決める
positions = ["正位置", "逆位置"]

@tarot_bp.route('/draw', methods=['GET'])
def draw_tarot():
    card = random.choice(tarot_deck)  # ランダムに1枚選ぶ
    position = random.choice(positions)  # 正位置 or 逆位置
    response_data = {"card": card, "position": position}
    response_json = json.dumps(response_data, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")
