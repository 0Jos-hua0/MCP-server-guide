from mcp.server.fastmcp import FastMCP
from typing import Annotated, Dict, Any

# Requires: yfinance (pip install yfinance)
import yfinance as yf  # type: ignore


mcp = FastMCP(name="MarketData", stateless_http=True)


@mcp.resource("stock://{ticker_symbol}")
def get_stock_info(
    ticker_symbol: Annotated[str, "Ticker symbol, e.g., 'AAPL', 'GOOGL', 'MSFT'"],
) -> Dict[str, Any]:
    """
    Return key stock information for the provided ticker symbol using yfinance.

    Arguments:
        ticker_symbol: The stock ticker symbol.

    Returns:
        A dictionary with basic market information including current price, day high/low,
        and the company's long business summary.

    Raises:
        ValueError: If the ticker symbol is invalid or data is unavailable.
    """
    symbol = (ticker_symbol or "").strip().upper()
    if not symbol:
        raise ValueError("ticker_symbol must be provided")

    ticker = yf.Ticker(symbol)
    info = ticker.info or {}

    current_price = info.get("currentPrice")
    day_high = info.get("dayHigh")
    day_low = info.get("dayLow")
    summary = info.get("longBusinessSummary")

    if current_price is None and day_high is None and day_low is None and not summary:
        raise ValueError(f"No data available for ticker '{symbol}'. Ensure it's a valid symbol.")

    return {
        "symbol": symbol,
        "currentPrice": current_price,
        "dayHigh": day_high,
        "dayLow": day_low,
        "longBusinessSummary": summary,
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")


