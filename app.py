import random

import streamlit as st

from groq_api import get_tarot_reading
from styles import CUSTOM_CSS, FONTS
from tarot_data import POSITIONS, TAROT_DECK


def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "LANDING"
    if "question" not in st.session_state:
        st.session_state.question = ""
    if "drawn_cards" not in st.session_state:
        st.session_state.drawn_cards = []
    if "ai_reading" not in st.session_state:
        st.session_state.ai_reading = ""
    if "api_error" not in st.session_state:
        st.session_state.api_error = ""


def reset_all():
    st.session_state.page = "LANDING"
    st.session_state.question = ""
    st.session_state.drawn_cards = []
    st.session_state.ai_reading = ""
    st.session_state.api_error = ""


def reset_for_new_question():
    st.session_state.page = "QUESTION"
    st.session_state.question = ""
    st.session_state.drawn_cards = []
    st.session_state.ai_reading = ""
    st.session_state.api_error = ""


def draw_cards():
    selected = random.sample(TAROT_DECK, 3)
    drawn = []
    for card in selected:
        card_copy = dict(card)
        card_copy["upright"] = random.random() > 0.5
        drawn.append(card_copy)
    return drawn


def render_ornament():
    st.markdown('<div class="ornament">✦ ✧ ✦</div>', unsafe_allow_html=True)


def render_keywords_html(keywords: list) -> str:
    tags = "".join(f'<span class="keyword-tag">{kw}</span>' for kw in keywords)
    return tags


def render_card_html(card: dict, position: str) -> str:
    orientation = "⬆ 正位" if card["upright"] else "⬇ 逆位"
    keywords = (
        card["keywords_upright"] if card["upright"] else card["keywords_reversed"]
    )
    brief = card["brief_upright"] if card["upright"] else card["brief_reversed"]
    keywords_html = render_keywords_html(keywords)

    return f"""
    <div class="tarot-card">
        <div class="card-position">{position}</div>
        <div class="card-name-zh">{card['name_zh']}</div>
        <div class="card-name-en">{card['name_en']}</div>
        <div class="card-orientation">{orientation}</div>
        <div style="margin: 0.6rem 0;">{keywords_html}</div>
        <div class="card-brief">{brief}</div>
    </div>
    """


def page_landing():
    render_ornament()
    st.markdown("# 命運之鏡 · Tarot Oracle")
    render_ornament()
    st.markdown(
        '<p class="landing-quote">「牌面不言命運，它只是映照你內心深處的聲音。」</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ 開始占卜", use_container_width=True):
            st.session_state.page = "DISCLAIMER"
            st.rerun()


def page_disclaimer():
    render_ornament()
    st.markdown("## 使用說明與免責聲明")
    render_ornament()

    st.markdown('<div class="section-title">【使用說明】</div>', unsafe_allow_html=True)
    st.markdown(
        """
1. 本平台提供塔羅牌三牌陣解讀（過去 / 現在 / 未來）
2. 請在心中或下一頁輸入你想詢問的問題
3. 點擊「抽牌」後，系統將從 78 張塔羅牌中隨機抽出 3 張
4. AI 將根據牌面與你的問題提供解析
5. 解析僅供參考，請以開放心態閱讀
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">【免責聲明】</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="disclaimer-box">
本平台之塔羅解讀純屬娛樂與心理探索用途，不構成任何醫療、法律、財務或人生建議。
所有解讀內容由 AI 生成，僅代表象徵性詮釋，不代表對未來事件之預測或保證。
使用者應自行判斷並承擔相關決策責任。
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 返回", use_container_width=True):
            st.session_state.page = "LANDING"
            st.rerun()
    with col2:
        if st.button("✅ 我已閱讀並同意，開始提問", use_container_width=True):
            st.session_state.page = "QUESTION"
            st.rerun()


def page_question():
    render_ornament()
    st.markdown("## 你想詢問什麼？")
    render_ornament()

    question = st.text_area(
        "問題",
        value=st.session_state.question,
        placeholder="例如：我的感情近況如何？我的事業發展方向是什麼？",
        max_chars=150,
        height=120,
        label_visibility="collapsed",
    )
    char_count = len(question.strip())
    st.markdown(
        f'<p class="question-hint">字數：{char_count} / 150（建議 10～150 字）</p>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🃏 洗牌並抽牌", use_container_width=True):
            trimmed = question.strip()
            if not trimmed:
                st.warning("請先輸入你想詢問的問題。")
            elif len(trimmed) < 10:
                st.warning("問題至少需要 10 個字，請描述得更具體一些。")
            else:
                st.session_state.question = trimmed
                st.session_state.drawn_cards = []
                st.session_state.ai_reading = ""
                st.session_state.api_error = ""
                st.session_state.page = "READING"
                st.rerun()


def page_reading():
    render_ornament()
    st.markdown(
        '<p class="reading-status">正在洗牌，請靜心思考你的問題...</p>',
        unsafe_allow_html=True,
    )
    render_ornament()

    with st.spinner("🔮 正在解讀牌面能量..."):
        try:
            if not st.session_state.drawn_cards:
                st.session_state.drawn_cards = draw_cards()
            if not st.session_state.ai_reading and not st.session_state.api_error:
                st.session_state.ai_reading = get_tarot_reading(
                    st.session_state.question,
                    st.session_state.drawn_cards,
                )
        except Exception as exc:
            st.session_state.api_error = (
                f"解讀過程中發生錯誤：{exc}\n\n"
                "請確認 .env 中的 GROQ_API_KEY 是否正確設定，稍後再試。"
            )

    st.session_state.page = "RESULT"
    st.rerun()


def page_result():
    render_ornament()
    st.markdown("## 你的塔羅解讀")
    render_ornament()

    st.markdown(
        f'<p class="user-question">「{st.session_state.question}」</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, card, position in zip(cols, st.session_state.drawn_cards, POSITIONS):
        with col:
            st.markdown(render_card_html(card, position), unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI 綜合解析</div>', unsafe_allow_html=True)

    if st.session_state.api_error:
        st.error(st.session_state.api_error)
    else:
        st.markdown(
            f'<div class="reading-text">{st.session_state.ai_reading}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 詢問其他問題", use_container_width=True):
            reset_for_new_question()
            st.rerun()
    with col2:
        if st.button("🏠 回到首頁", use_container_width=True):
            reset_all()
            st.rerun()


def main():
    st.set_page_config(
        page_title="命運之鏡 · Tarot Oracle",
        page_icon="🔮",
        layout="centered",
    )
    init_session_state()
    st.markdown(FONTS + CUSTOM_CSS, unsafe_allow_html=True)

    page = st.session_state.page
    if page == "LANDING":
        page_landing()
    elif page == "DISCLAIMER":
        page_disclaimer()
    elif page == "QUESTION":
        page_question()
    elif page == "READING":
        page_reading()
    elif page == "RESULT":
        page_result()


if __name__ == "__main__":
    main()
