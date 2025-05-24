from google.adk import Agent
from google.adk.tools import FunctionTool
import os
import requests
import pandas as pd
from datetime import datetime

# --- Alpha Vantage API setup ---
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

# --- Free LLM Helper (Zephyr 7B on OpenRouter) ---
def openrouter_zephyr(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "huggingfaceh4/zephyr-7b-beta:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# --- Individual Tool Functions ---
def identify_stock_ticker(company_name: str) -> dict:
    """Finds the stock ticker for a given company name."""
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': company_name,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    best_match = next(
        (item for item in data.get('bestMatches', []) if item['4. region'] == 'United States'),
        None
    )
    if best_match:
        return {
            'ticker': best_match['1. symbol'],
            'name': best_match['2. name'],
            'match_score': float(best_match['9. matchScore'])
        }
    return {'error': 'Ticker not found'}

def get_stock_news(ticker: str) -> dict:
    """Fetches recent news for a ticker."""
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return {
        'news': [{
            'title': item['title'],
            'url': item['url'],
            'sentiment': item['overall_sentiment_score']
        } for item in data.get('feed', [])[:3]]
    }

def get_current_price(ticker: str) -> dict:
    """Gets the current price for a ticker."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': ticker,
        'interval': '5min',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        latest_data = next(iter(data['Time Series (5min)'].values()))
        return {
            'price': float(latest_data['4. close']),
            'currency': 'USD',
            'timestamp': datetime.now().isoformat()
        }
    except Exception:
        return {'error': 'Could not fetch price (API limit or invalid ticker).'}

def get_price_change(ticker: str, days: int) -> dict:
    """Calculates price change over a given number of days."""
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'Time Series (Daily)' not in data:
        return {'error': 'Could not fetch price history.'}
    df = pd.DataFrame(data['Time Series (Daily)']).T.astype(float)
    closes = df['4. close'].sort_index(ascending=False)
    if len(closes) < days + 1:
        return {'error': 'Not enough data.'}
    latest_close = closes.iloc[0]
    prev_close = closes.iloc[days]
    change_pct = round(((latest_close - prev_close) / prev_close) * 100, 2)
    return {
        'change_pct': change_pct,
        'latest_close': latest_close,
        'prev_close': prev_close
    }

def analyze_ticker(company_name: str, days: int = 7) -> dict:
    """AI-powered summary of price and news for a company."""
    ticker_info = identify_stock_ticker(company_name)
    if "ticker" not in ticker_info:
        return {"error": "Could not identify ticker."}
    ticker = ticker_info["ticker"]
    price_info = get_price_change(ticker, days)
    news_info = get_stock_news(ticker)
    prompt = (
        f"Analyze the stock {company_name} ({ticker}) for the last {days} days.\n"
        f"Price change: {price_info}\n"
        f"Recent news: {news_info['news']}\n"
        f"Summarize the main reasons for the price movement."
    )
    summary = openrouter_zephyr(prompt)
    return {
        'summary': summary,
        'price_change': price_info,
        'recent_news': news_info['news']
    }

# --- Register Each Tool as an Agent (or just use root_agent) ---
root_agent = Agent(
    name="StockAnalysisAgent",
    tools=[
        FunctionTool(identify_stock_ticker),
        FunctionTool(get_stock_news),
        FunctionTool(get_current_price),
        FunctionTool(get_price_change),
        FunctionTool(analyze_ticker)
    ],
    description="Stock analysis system with free LLM-powered analysis.",
    instruction="Use the appropriate tool to answer stock queries."
)
