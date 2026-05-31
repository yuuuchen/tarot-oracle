import os
import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch

# 指定主程式路徑
APP_PATH = "app.py"

class TestTarotSecuritySDLC:
    
    @pytest.fixture
    def app(self):
        """初始化 Streamlit 測試實例"""
        at = AppTest.from_file(APP_PATH, default_timeout=10)
        return at

    # ==========================================
    # 1. 狀態機與存取控制 (State Machine & Access)
    # ==========================================
    @patch('app.get_tarot_reading', return_value="這是一個模擬的安全測試回應。")
    def test_state_machine_bypass(self, mock_get_tarot_reading, app):
        """資安測試：嘗試繞過免責聲明，直接修改 Session State"""
        app.run()
        app.session_state["page"] = "READING"
        app.run() 
        assert not app.exception, "系統在面臨非預期的狀態跳躍時發生了崩潰"

    # ==========================================
    # 2. 輸入驗證與邊界測試 (Input Validation & Boundary)
    # ==========================================
    def test_input_boundary_too_short_or_empty(self, app):
        """資安測試：測試過短或空白的輸入是否被正確阻擋"""
        app.run()
        app.session_state["page"] = "QUESTION"
        app.run()
        
        # 測試過短字串
        app.text_area[0].input("太短的問題").run()
        app.button[0].click().run()
        assert app.session_state["page"] == "QUESTION"
        assert any("至少需要 10 個字" in w.value for w in app.warning)

        # 測試空白字串
        app.text_area[0].input("          ").run()
        app.button[0].click().run()
        assert app.session_state["page"] == "QUESTION"
        assert any("請先輸入你想詢問的問題" in w.value for w in app.warning)

    @patch('app.get_tarot_reading', return_value="Mock")
    def test_input_boundary_too_long(self, mock_api, app):
        """資安測試：後端是否能承受超出前端 max_chars 的異常超長輸入 (Buffer/Token 消耗)"""
        app.run()
        app.session_state["page"] = "QUESTION"
        app.run()
        
        massive_payload = "A" * 5000
        app.text_area[0].input(massive_payload).run()
        app.button[0].click().run()
        
        assert not app.exception, "系統遭到超長字串攻擊時發生崩潰！"

    # ==========================================
    # 3. 跨網站指令碼防護 (XSS Injection)
    # ==========================================
    @patch('app.get_tarot_reading', return_value="Mock")
    def test_xss_injection_handling(self, mock_api, app):
        """資安測試：XSS 注入。測試系統是否會將使用者的惡意腳本直接渲染成前端 HTML。"""
        app.run()
        app.session_state["page"] = "QUESTION"
        app.run()
        
        xss_payload = "<script>alert('XSS')</script><b>被竄改的文字</b>"
        app.text_area[0].input(xss_payload).run()
        app.button[0].click().run()
        app.run() 
        
        frontend_html = "".join([md.value for md in app.markdown])
        assert "<script>" not in frontend_html, "嚴重漏洞 (XSS)：使用者的惡意 HTML 標籤未經消毒，被直接渲染至前端！"

    # ==========================================
    # 4. 錯誤處理與資訊洩漏 (Error Handling)
    # ==========================================
    @patch('app.get_tarot_reading')
    def test_api_failure_information_disclosure(self, mock_get_tarot_reading, app):
        """資安測試：當 API 發生嚴重錯誤時，系統是否會印出帶有密鑰的 Stack Trace。"""
        sensitive_error_msg = "AuthenticationError: Invalid API key 'gsk_1234567890abcdef' provided."
        mock_get_tarot_reading.side_effect = Exception(sensitive_error_msg)
        
        app.run()
        app.session_state["page"] = "READING"
        app.session_state["question"] = "測試系統發生錯誤時的狀態處理，字數要大於十個字。"
        app.session_state["drawn_cards"] = [] 
        app.run()
        app.run()
        
        frontend_output = "".join([err.value for err in app.error])
        assert "gsk_" not in frontend_output, "嚴重漏洞：前端畫面洩漏了 API Key！"
        assert "AuthenticationError" not in frontend_output, "漏洞：前端畫面洩露了底層例外名稱！"

    # ==========================================
    # 5. 高頻抽牌與唯一性驗證 (High-Frequency & Uniqueness)
    # ==========================================
    def test_high_frequency_draw_uniqueness(self):
        """資安與邏輯測試：連續執行抽牌邏輯 100 次，驗證每一次抽出的 3 張牌是否絕對不重複。"""
        from app import draw_cards
        
        for i in range(100):
            cards = draw_cards()
            assert len(cards) == 3, f"第 {i} 次抽牌數量錯誤！"
            card_names = [card['name_en'] for card in cards]
            assert len(set(card_names)) == 3, f"第 {i} 次抽牌發生重複：{card_names}"

    # ==========================================
    # 6. LLM 系統防護護欄 (Prompt Guardrails)
    # ==========================================
    @patch('groq_api.Groq')
    def test_llm_prompt_guardrails(self, MockGroq, app):
        """資安測試：攔截底層 Groq API 呼叫，驗證 System Prompt 是否包含安全指令。"""
        os.environ["GROQ_API_KEY"] = "fake-test-key"
        
        mock_client_instance = MockGroq.return_value
        mock_message = type('Message', (), {'content': '這是模擬的 AI 占卜結果'})()
        mock_choice = type('Choice', (), {'message': mock_message})()
        mock_client_instance.chat.completions.create.return_value = type('Response', (), {'choices': [mock_choice]})()
        
        app.run()
        app.session_state["page"] = "READING"
        app.session_state["question"] = "這是一個測試問題，字數絕對大於十個字。"
        app.session_state["drawn_cards"] = []
        app.run()
        
        mock_client_instance.chat.completions.create.assert_called_once()
        call_kwargs = mock_client_instance.chat.completions.create.call_args.kwargs
        messages = call_kwargs.get("messages", [])
        system_prompt = next((m["content"] for m in messages if m["role"] == "system"), "")
        
        assert "安全核心指令" in system_prompt, "資安漏洞：發送給 LLM 的 System Prompt 缺少安全核心指令！"
        assert "拒絕" in system_prompt, "資安漏洞：未明確指示 LLM 拒絕使用者的非占卜/惡意要求！"

    # ==========================================
    # 7. 敏感個資與隱私外洩防護 (PII Leakage Prevention)
    # ==========================================
    @patch('groq_api.Groq')
    def test_pii_leakage_prevention(self, MockGroq, app):
        """
        資安測試：測試當使用者輸入包含身分證字號或電話號碼等高敏感個資時，
        系統是否能在送出給第三方 LLM 前進行資料遮蔽 (Data Masking) 或攔截。
        """
        os.environ["GROQ_API_KEY"] = "fake-test-key"
        
        mock_client_instance = MockGroq.return_value
        mock_message = type('Message', (), {'content': '這是模擬的 AI 占卜結果'})()
        mock_choice = type('Choice', (), {'message': mock_message})()
        mock_client_instance.chat.completions.create.return_value = type('Response', (), {'choices': [mock_choice]})()
        
        app.run()
        app.session_state["page"] = "QUESTION"
        app.run()

        # 模擬使用者輸入包含台灣身分證字號 (Taiwan ID) 與電話號碼的危險字串
        pii_payload = "我最近一直被前任騷擾，我的身分證字號是 A123456789，電話是 0912-345-678，我該怎麼辦？"
        app.text_area[0].input(pii_payload).run()
        app.button[0].click().run()

        # 若系統阻擋了提問 (例如顯示警告)，則狀態會停留在 QUESTION，這是安全的
        if app.session_state["page"] == "QUESTION":
            assert any("包含敏感個人資訊" in w.value for w in app.warning), "系統阻擋了提問，但未提供正確的警告訊息。"
            return # 測試成功結束

        # 若系統允許進入抽牌環節，則必須確保送給 API 的字串經過了去識別化遮蔽 (Masking)
        if app.session_state["page"] == "READING":
            app.run() # 觸發 API 呼叫
            
            call_kwargs = mock_client_instance.chat.completions.create.call_args.kwargs
            messages = call_kwargs.get("messages", [])
            user_prompt = next((m["content"] for m in messages if m["role"] == "user"), "")
            
            # 斷言：送給 LLM 的封包中，絕對不能包含明文的機敏資料
            assert "A123456789" not in user_prompt, "嚴重隱私漏洞：使用者的身分證字號被明文傳送給了第三方 API！"
            assert "0912-345-678" not in user_prompt, "嚴重隱私漏洞：使用者的電話號碼被明文傳送給了第三方 API！"