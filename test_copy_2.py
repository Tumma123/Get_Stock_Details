import datetime
import pyttsx3
import yfinance as yf
import pandas as pd

# Hardcoded list of NIFTY 50 tickers (Yahoo Finance format)
NIFTY_50_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "HDFC.NS",
    "ITC.NS", "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "MARUTI.NS",
    "ASIANPAINT.NS", "ONGC.NS", "DIVISLAB.NS", "NESTLEIND.NS", "TITAN.NS",
    "ULTRACEMCO.NS", "WIPRO.NS", "TATASTEEL.NS", "JSWSTEEL.NS", "BAJAJFINSV.NS",
    "POWERGRID.NS", "ADANIGREEN.NS", "HCLTECH.NS", "DRREDDY.NS", "GRASIM.NS",
    "COALINDIA.NS", "TECHM.NS", "IOC.NS", "HINDALCO.NS", "EICHERMOT.NS",
    "CIPLA.NS", "TATAMOTORS.NS", "SHREECEM.NS", "BRITANNIA.NS", "HEROMOTOCO.NS",
    "M&M.NS", "BAJAJ-AUTO.NS", "SBILIFE.NS", "VEDL.NS", "TATACONSUM.NS",
    "UPL.NS", "ADANIPORTS.NS", "NTPC.NS", "HDFCLIFE.NS", "ICICIPRULI.NS"
]

def fetch_indices_for_date(date):
    indices = {}
    tickers = {
        "NIFTY 50": "^NSEI",
        "NIFTY BANK": "^NSEBANK"
    }
    for name, ticker in tickers.items():
        print(f"[DEBUG] Fetching data for {name} ({ticker}) on {date}...")
        try:
            start_date = date.strftime("%Y-%m-%d")
            end_date = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if data.empty:
                print(f"[ERROR] No data returned for {name} on {date}")
                indices[name] = None
            else:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                indices[name] = data.iloc[0]
        except Exception as e:
            print(f"[ERROR] Failed to fetch {name} data: {e}")
            indices[name] = None
    return indices

def fetch_top_gainers_and_losers(date, tickers, top_n=5):
    print(f"[DEBUG] Fetching data for {len(tickers)} tickers to calculate top gainers/losers...")
    start_date = date.strftime("%Y-%m-%d")
    end_date = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    records = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if data.empty:
                continue
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            open_price = data['Open'].iloc[0]
            close_price = data['Close'].iloc[0]
            pct_change = ((close_price - open_price) / open_price) * 100 if open_price != 0 else 0
            records.append({
                "Ticker": ticker,
                "Open": open_price,
                "Close": close_price,
                "Percent Change": pct_change
            })
        except Exception as e:
            print(f"[WARNING] Failed to fetch data for {ticker}: {e}")
            continue

    df = pd.DataFrame(records)
    if df.empty:
        print("[ERROR] No data available for gainers/losers calculation.")
        return [], []

    top_gainers = df.sort_values(by="Percent Change", ascending=False).head(top_n)
    top_losers = df.sort_values(by="Percent Change").head(top_n)

    return top_gainers, top_losers

def make_text_report(indices, date, top_gainers, top_losers):
    date_str = date.strftime("%d %b, %Y")
    text = f"Market Summary for {date_str}:\n\n"
    for name, data in indices.items():
        if data is not None:
            open_price = data['Open']
            close_price = data['Close']
            change = close_price - open_price
            pct_change = (change / open_price) * 100 if open_price != 0 else 0
            text += (f"{name}: Last Close: {close_price:.2f}, "
                     f"Change: {change:.2f}, "
                     f"Percent Change: {pct_change:.2f}%\n")
        else:
            text += f"{name}: Data not available.\n"

    text += "\nTop Gainers:\n"
    if len(top_gainers) == 0:
        text += "Data not available.\n"
    else:
        for _, row in top_gainers.iterrows():
            text += (f"{row['Ticker']}: Close {row['Close']:.2f}, "
                     f"Change {row['Percent Change']:.2f}%\n")

    text += "\nTop Losers:\n"
    if len(top_losers) == 0:
        text += "Data not available.\n"
    else:
        for _, row in top_losers.iterrows():
            text += (f"{row['Ticker']}: Close {row['Close']:.2f}, "
                     f"Change {row['Percent Change']:.2f}%\n")

    return text

def text_to_audio(text, filename="market_report.mp3"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.save_to_file(text, filename)
    engine.runAndWait()

def main():
    print("[DEBUG] Script started.")
    date_input = input("Enter the date for the market report (YYYY-MM-DD): ")
    print(f"[DEBUG] Raw input: '{date_input}'")
    try:
        date_stripped = date_input.strip()
        date = datetime.datetime.strptime(date_stripped, "%Y-%m-%d").date()
        print(f"[DEBUG] Parsed date: {date}")
        print("[INFO] Fetching index data...")
        indices = fetch_indices_for_date(date)

        print("[INFO] Fetching top gainers and losers...")
        top_gainers, top_losers = fetch_top_gainers_and_losers(date, NIFTY_50_TICKERS, top_n=5)

        print("[DEBUG] Generating report text...")
        report_text = make_text_report(indices, date, top_gainers, top_losers)

        print("\n=== Report Text ===")
        print(report_text)

        text_to_audio(report_text)
        print("[INFO] Audio saved to market_report.mp3")

    except ValueError:
        print("[ERROR] Invalid date format. Please use YYYY-MM-DD.")

if __name__ == "__main__":
    main()
