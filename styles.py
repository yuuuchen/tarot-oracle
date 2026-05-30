FONTS = """
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
"""

CUSTOM_CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #12122b 50%, #0d0d1a 100%);
    background-attachment: fixed;
}

.main .block-container {
    max-width: 860px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

h1 {
    font-family: 'Cinzel', serif;
    color: #c9a84c;
    text-align: center;
    letter-spacing: 0.15em;
    text-shadow: 0 0 40px rgba(201,168,76,0.4);
}

h2, h3 {
    font-family: 'Cinzel', serif;
    color: #c9a84c;
}

p, .stMarkdown {
    font-family: 'Crimson Text', serif;
    color: #f0ead6;
}

.tarot-card {
    background: linear-gradient(160deg, #1a1a3e, #0f0f28);
    border: 1px solid #2d2d5e;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(201,168,76,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    min-height: 280px;
}
.tarot-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5), 0 0 20px rgba(201,168,76,0.1);
}

.card-position {
    font-family: 'Cinzel', serif;
    color: #e8c97a;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    margin-bottom: 0.5rem;
}

.card-name-zh {
    font-family: 'Cinzel', serif;
    color: #c9a84c;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0.3rem 0;
}

.card-name-en {
    font-family: 'Crimson Text', serif;
    color: #a89a7a;
    font-size: 0.9rem;
    font-style: italic;
}

.card-orientation {
    font-family: 'Cinzel', serif;
    color: #e8c97a;
    font-size: 0.85rem;
    margin: 0.5rem 0;
}

.card-brief {
    font-family: 'Crimson Text', serif;
    color: #a89a7a;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-top: 0.8rem;
}

.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 2rem 0;
}

.stButton > button {
    font-family: 'Cinzel', serif;
    letter-spacing: 0.1em;
    border: 1px solid #c9a84c !important;
    background: transparent !important;
    color: #c9a84c !important;
    padding: 0.7rem 2rem;
    border-radius: 4px;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background: rgba(201,168,76,0.1) !important;
    box-shadow: 0 0 20px rgba(201,168,76,0.2);
    color: #e8c97a !important;
    border-color: #e8c97a !important;
}

.stTextArea textarea {
    background: #12122b !important;
    border: 1px solid #2d2d5e !important;
    color: #f0ead6 !important;
    font-family: 'Crimson Text', serif;
    font-size: 1.1rem;
    border-radius: 8px;
}
.stTextArea textarea:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 12px rgba(201,168,76,0.15);
}

.reading-text {
    font-family: 'Crimson Text', serif;
    font-size: 1.15rem;
    line-height: 1.9;
    color: #f0ead6;
    background: rgba(201,168,76,0.03);
    border-left: 2px solid #c9a84c;
    padding: 1.5rem 2rem;
    border-radius: 0 8px 8px 0;
}

.keyword-tag {
    display: inline-block;
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.3);
    color: #e8c97a;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.82rem;
    margin: 2px;
    font-family: 'Crimson Text', serif;
}

.disclaimer-box {
    background: rgba(13,13,26,0.8);
    border: 1px solid #2d2d5e;
    border-radius: 8px;
    padding: 1.5rem;
    color: #a89a7a;
    font-family: 'Crimson Text', serif;
    font-size: 0.95rem;
    line-height: 1.7;
}

.ornament {
    text-align: center;
    color: #c9a84c;
    font-size: 1.2rem;
    letter-spacing: 0.5em;
    margin: 1rem 0;
}

.landing-quote {
    font-family: 'Crimson Text', serif;
    font-size: 1.25rem;
    color: #a89a7a;
    text-align: center;
    font-style: italic;
    line-height: 1.8;
    margin: 2rem 0;
}

.question-hint {
    font-family: 'Crimson Text', serif;
    color: #a89a7a;
    font-size: 0.9rem;
}

.user-question {
    font-family: 'Crimson Text', serif;
    color: #a89a7a;
    font-size: 0.95rem;
    text-align: center;
    font-style: italic;
    margin-bottom: 1.5rem;
}

.section-title {
    font-family: 'Cinzel', serif;
    color: #c9a84c;
    font-size: 1rem;
    letter-spacing: 0.1em;
    margin-bottom: 0.8rem;
}

.reading-status {
    font-family: 'Crimson Text', serif;
    color: #e8c97a;
    text-align: center;
    font-size: 1.2rem;
    margin: 3rem 0;
}
</style>
"""
