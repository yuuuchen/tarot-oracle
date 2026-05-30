import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_tarot_reading(question: str, cards: list) -> str:
    """
    cards: list of 3 dicts，每個 dict 包含牌的完整資訊與正逆位
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("未設定 GROQ_API_KEY，請在 .env 檔案中填入您的 API 金鑰。")

    client = Groq(api_key=api_key)

    cards_description = ""
    positions = ["過去（Past）", "現在（Present）", "未來（Future）"]
    for i, (card, position) in enumerate(zip(cards, positions)):
        orientation = "正位" if card["upright"] else "逆位"
        keywords = (
            card["keywords_upright"] if card["upright"] else card["keywords_reversed"]
        )
        cards_description += f"""
        位置 {i + 1}：{position}
        牌名：{card['name_zh']}（{card['name_en']}）— {orientation}
        關鍵詞：{', '.join(keywords)}
        """

    system_prompt = (
        "你是一位深具智慧與洞察力的塔羅解讀師，擅長以溫柔而深刻的方式"
        "幫助人們理解牌面訊息。請務必以繁體中文回應。"
    )

    user_prompt = f"""使用者的問題：{question}

本次抽到的三張牌（過去／現在／未來三牌陣）：
{cards_description}

請提供一段完整、流暢的塔羅解析。解析需：
1. 先簡短說明三牌陣的整體能量走向
2. 依序解讀每張牌在其位置上的意涵，並與使用者問題結合
3. 最後給予一段整合性的建議或啟示，語氣溫暖而不武斷
4. 全文約 400～600 字，不使用條列式，以自然段落呈現
5. 結尾可加上一句鼓勵性的話，但不做任何命運預言或絕對性陳述

請記住：塔羅是引導內在智慧的工具，而非預言機器。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        temperature=0.8,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
