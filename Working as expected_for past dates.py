import datetime
import pyttsx3
import yfinance as yf
import pandas as pd  # Added import

def fetch_indices_for_date(date):
    """
    Fetch NIFTY 50 and NIFTY BANK data for the given date from Yahoo Finance.
    """
    indices = {}
    tickers = {
        "NIFTY 50": "^NSEI",
        "NIFTY BANK": "^NSEBANK"
    }
    for name, ticker in tickers.items():
        print(f"[DEBUG] Fetching data for {name} ({ticker}) on {date}...")
        try:
            start_date = date.strftime("%Y-%m-%d")
            # Yahoo finance end date is exclusive, so add 1 day
            end_date = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                print(f"[ERROR] No data returned for {name} on {date}")
                indices[name] = None
            else:
                # Fix: Flatten columns if multi-level
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                print(f"[DEBUG] Data fetched for {name}:\n{data}")
                indices[name] = data.iloc[0]
        except Exception as e:
            print(f"[ERROR] Failed to fetch {name} data: {e}")
            indices[name] = None
    return indices

def make_text_report(indices, date):
    """
    Generate a readable market summary text for the indices on the given date.
    """
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
    return text

def text_to_audio(text, filename="market_report.mp3"):
    """
    Convert the given text to speech and save as an mp3 file.
    """
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

        print("[DEBUG] Generating report text...")
        report_text = make_text_report(indices, date)

        print("\n=== Report Text ===")
        print(report_text)

        text_to_audio(report_text)
        print("[INFO] Audio saved to market_report.mp3")

    except ValueError:
        print("[ERROR] Invalid date format. Please use YYYY-MM-DD.")

if __name__ == "__main__":
    main()