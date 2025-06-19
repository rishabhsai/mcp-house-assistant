from market_recap_tool import MarketRecapTool

def main():
    tool = MarketRecapTool()
    # You can specify markets or leave blank for default
    result = tool.get_market_recap(markets=['^GSPC', '^IXIC', '^DJI', 'AAPL'])
    print(result)

if __name__ == "__main__":
    main()
