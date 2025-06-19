import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any

class MarketRecapTool:
    def __init__(self):
        pass

    def get_market_recap(self, date: str = None, markets: List[str] = None) -> Dict[str, Any]:
        if not markets:
            markets = ['^GSPC', '^IXIC', '^DJI']  # S&P 500, NASDAQ, Dow Jones

        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        recap = {"date": date, "markets": []}
        for symbol in markets:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")  # Get last 2 days to compare
            if len(hist) < 2:
                continue
            prev_close = hist['Close'].iloc[-2]
            today_close = hist['Close'].iloc[-1]
            change = today_close - prev_close
            pct_change = (change / prev_close) * 100
            recap["markets"].append({
                "symbol": symbol,
                "name": ticker.info.get("shortName", symbol),
                "close": round(today_close, 2),
                "change": round(change, 2),
                "pct_change": round(pct_change, 2)
            })
        return recap

def main(date: str = None, markets: str = None):
    market_list = markets.split(",") if markets else None
    tool = MarketRecapTool()
    return tool.get_market_recap(date=date, markets=market_list)
