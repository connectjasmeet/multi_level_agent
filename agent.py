import yfinance as yf
import json
import time
from datetime import datetime

# Load config
with open("config.json") as f:
    config = json.load(f)

stocks = config["stocks"]
buy_thresholds = config["buy_thresholds"]
sell_thresholds = config["sell_thresholds"]
interval = config["check_interval_seconds"]
strategy = config["strategy"]

def fetch_price(ticker):
    stock = yf.Ticker(ticker)
    price = stock.history(period="1m")["Close"].iloc[-1]
    return round(price, 2)

# High-level reasoning
def high_level_reasoning(strategy):
    if strategy == "aggressive":
        return 2  # larger trade scale
    elif strategy == "moderate":
        return 1
    else:
        return 0  # minimal trades

# Mid-level reasoning
def mid_level_reasoning(ticker, price):
    if price <= buy_thresholds[ticker]:
        return "BUY"
    elif price >= sell_thresholds[ticker]:
        return "SELL"
    else:
        return "HOLD"

# Low-level execution
def execute_action(ticker, price, action, trade_scale):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    qty = trade_scale if action in ["BUY", "SELL"] else 0
    log_msg = f"[{timestamp}] {ticker} Price: ${price} → Action: {action} Qty: {qty}"
    print(log_msg)
    with open("agent_log.txt", "a") as f:
        f.write(log_msg + "\n")

# Run agent
def run_agent():
    print("Starting Multi-Level Stock Agent...")
    while True:
        trade_scale = high_level_reasoning(strategy)
        for ticker in stocks:
            try:
                price = fetch_price(ticker)
                action = mid_level_reasoning(ticker, price)
                execute_action(ticker, price, action, trade_scale)
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    run_agent()
