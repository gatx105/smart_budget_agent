# 智慧記帳與預算管理 Agent

智慧記帳與預算管理 Agent 是一個以純 Python 開發的自然語言記帳工具。使用者可以透過文字描述消費內容，Agent 使用 OpenAI-compatible LLM 解析消費資訊並呼叫 Tool，最後將資料寫入 SQLite。

本專案目前以指定作業 2 的最小可執行範圍為主：完成 Agent、Tool Calling、自然語言參數解析與 SQLite 記帳功能。預算設定、預算預警、週月統計與長期對話記憶等功能保留至後續階段。

## 主要功能

- 接收口語化記帳文字，例如「今天午餐花了 120 元」
- 使用 GPT-6 Luna 解析品項、金額、分類與消費日期
- 透過 `record_expense` Tool 將消費寫入 SQLite
- 金額為零、負數、非整數或必要欄位缺漏時拒絕寫入並要求補充
- 提供手動 SQLite 檢查工具
- 支援透過 `.env` 設定 OpenAI-compatible API

## 專案結構

```text
smart_budget_agent/
├── agent/
│   ├── core.py          # Agent 主流程
│   ├── llm_client.py    # OpenAI-compatible HTTP Client
│   ├── prompt.py        # System Prompt
│   └── tool.py          # Tool Registry 與 Tool Schema
├── database/
│   ├── db_setup.py      # SQLite 連線與資料表初始化
│   ├── repository.py    # 資料庫存取函式
│   └── smart_budget.db  # 執行後產生的本機資料庫
├── tools/
│   └── expense_tools.py # record_expense Tool
├── tests/
│   ├── test_db_setup.py
│   ├── test_expense_tools.py
│   └── test_llm_client.py
├── check_sql.py         # 手動 SQLite 檢查程式
├── main.py              # 命令列入口
├── requirements.txt
├── .env.example
└── README.md
```

## 執行環境

- Python 3.10 以上
- 可連線至 OpenAI-compatible API
- OpenAI API Key
- SQLite，不需要另外安裝資料庫伺服器

## 安裝方式

進入專案目錄：

```powershell
cd D:\NTPU\Y4S1\AI_agent\phase1\smart_budget_agent
```

安裝相依套件：

```powershell
python -m pip install -r requirements.txt
```

複製環境設定範本：

```powershell
Copy-Item .env.example .env
```

編輯 `.env`：

```dotenv
OPENAI_API_KEY=你的API金鑰
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-6-luna
```

如果不使用 `.env`，也可以在目前工作階段設定環境變數：

```powershell
$env:OPENAI_API_KEY = "你的API金鑰"
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
$env:OPENAI_MODEL = "gpt-6-luna"
```

## 啟動 Agent

```powershell
python main.py
```

輸入 `exit` 可離開程式。

建議測試：

```text
今天午餐花了 120 元
剛剛搭捷運花了 25
下午買咖啡 65 元
我今天買了一些東西
零元測試
exit
```

Agent 預期會：

- 正常消費：執行 `record_expense` 並寫入 SQLite
- 缺少金額：要求使用者補充金額
- 缺少品項或分類：要求使用者補充必要資訊
- 金額小於或等於零：拒絕寫入

- `.env.example` 只保留欄位與預設值
- SQLite 資料庫屬於執行時產生的本機資料，不應混入公開測試資料
