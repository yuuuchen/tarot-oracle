# 🔮 命運之鏡 · Tarot Oracle

以 **Python + Streamlit** 建構的塔羅牌占卜平台，提供三牌陣（過去／現在／未來）解讀，並透過 **Groq API** 生成個人化的 AI 塔羅解析。

## 功能特色

- 完整 **78 張** 標準塔羅牌資料（大阿爾克納 22 張 + 小阿爾克納 56 張）
- 三牌陣占卜：過去、現在、未來
- 每張牌隨機決定**正位**或**逆位**（各 50% 機率）
- 以 Groq LLM（`llama-3.3-70b-versatile`）生成繁體中文綜合解析
- 神秘極簡主義深色 UI，金色點綴與優雅字體
- 五段式引導流程：首頁 → 免責聲明 → 提問 → 抽牌 → 結果

## 安裝步驟

### 1. 克隆或進入專案目錄

```bash
cd tarot-oracle
```

### 2. 建立虛擬環境（建議）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 設定環境變數

複製範例檔案並填入您的 Groq API 金鑰：

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```
GROQ_API_KEY=your_key_here
```

> Groq API 金鑰可至 [console.groq.com](https://console.groq.com) 免費申請。

## 執行方式

```bash
streamlit run app.py
```

瀏覽器將自動開啟本地應用（預設 `http://localhost:8501`）。

## 專案結構

```
tarot-oracle/
├── app.py              # 主程式（Streamlit 頁面與狀態機）
├── tarot_data.py       # 78 張塔羅牌完整資料
├── groq_api.py         # Groq API 呼叫邏輯
├── styles.py           # CSS 樣式字串
├── .env                # API 金鑰（請自行建立，勿提交至版本控制）
├── .env.example        # 環境變數範例
├── requirements.txt    # Python 依賴
└── README.md
```

## 使用流程

1. 點擊「開始占卜」進入免責聲明頁
2. 閱讀使用說明並同意後，輸入您的問題（10～150 字）
3. 點擊「洗牌並抽牌」，系統將隨機抽取 3 張牌並呼叫 AI 解析
4. 查看三牌陣結果與 AI 綜合解讀

## 免責聲明

本平台之塔羅解讀純屬娛樂與心理探索用途，不構成任何醫療、法律、財務或人生建議。所有解讀內容由 AI 生成，僅代表象徵性詮釋。

## 技術規格

- Python 3.10+
- Streamlit
- Groq API（`groq` 套件）
- python-dotenv
