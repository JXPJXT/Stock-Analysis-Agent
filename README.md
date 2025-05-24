# 🚀 StockAnalysisAgent: AI-Powered Stock Insights with OpenRouter & ADK

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![ADK](https://img.shields.io/badge/google--adk-powered-brightgreen)
![OpenRouter](https://img.shields.io/badge/openrouter-gpt--3.5--turbo-orange)
![Alpha Vantage](https://img.shields.io/badge/alpha%20vantage-free%20stock%20API-yellow)

---

## 📖 Overview

**StockAnalysisAgent** is a multi-tool, AI-enabled stock analysis system built using [Google ADK](https://github.com/google/agent-development-kit), [OpenRouter](https://openrouter.ai/), and [Alpha Vantage](https://www.alphavantage.co/).  
It provides ticker lookup, real-time news, price data, price change analytics, and summary analysis—all accessible via a conversational chat interface or individual tools.

---

## ✨ Features

- **Chat with your agent** about stocks, tickers, news, and analytics
- **5 powerful tools**:
  1. Identify ticker from company name
  2. Get latest news for a ticker
  3. Fetch current price
  4. Calculate price change over time
  5. Summarize price movement & news (AI-powered)
- **Powered by OpenRouter’s GPT-3.5-turbo** (tool use enabled)
- **Free stock data via Alpha Vantage**
- **Easy to deploy, extend, and customize**

---

## 🚦 Requirements

- Python 3.10+
- [Google ADK](https://github.com/google/agent-development-kit)
- [OpenRouter API key](https://openrouter.ai/)
- [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)
- `requests`, `pandas`, `google-adk`, `litellm`

---

## ⚡️ Quickstart

### 1. **Clone this repository**

### 2. **Install dependencies**
pip install -r requirements.txt

### 3. **Set up your environment variables**
Create a `.env` file (or export in your shell):
OPENROUTER_API_KEY=sk-...your_openrouter_key...
ALPHA_VANTAGE_API_KEY=...your_alpha_vantage_key...

### 4. **Run the agent**
adk web

### 5. **Open the ADK UI**
Go to [http://localhost:8000](http://localhost:8000) in your browser.

---

## 💡 Usage

### **Chat Examples**
- “What’s the ticker for Tesla?”
- “Give me the latest news for AAPL.”
- “What is the current price of MSFT?”
- “How has GOOGL changed in the last 5 days?”
- “Analyze TSLA stock for the past week.”

### **Tools Tab**
Each tool is also available individually for direct API-style use.

---

## 🛠️ Project Structure

your-repo/
├── multi_tool_agent/
│ ├── agent.py
│ └── init.py
├── requirements.txt
├── .env
└── README.md

---

## 🧩 How It Works

- **OpenRouter GPT-3.5-turbo** is used as the LLM for chat and tool orchestration (via LiteLlm).
- **Alpha Vantage** provides real-time and historical stock data and news.
- **FunctionTools** wrap each capability, so you can use them in chat or directly.

---

## 🛡️ Troubleshooting

- **No model found error:**  
  Ensure your `OPENROUTER_API_KEY` is valid and you have credits for GPT-3.5-turbo.
- **Alpha Vantage errors:**  
  Check your API key and usage limits.
- **Quota/token errors:**  
  Lower `max_tokens` in the LiteLlm config (`model_kwargs={"max_tokens": 512}`).
- **Tools not working in chat:**  
  Only GPT-3.5-turbo and GPT-4o on OpenRouter support tool use.

---

## 🌍 Credits & Links

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [OpenRouter Models](https://openrouter.ai/models)
- [Alpha Vantage API](https://www.alphavantage.co/documentation/)
- [Project Author: Japjot Singh](bhatiajapjotjpr@gmail.com)

---

## 🤝 Contributing

Pull requests and issues are welcome!  
If you use this for a project or internship, let me know—I’d love to see it in action.

---
