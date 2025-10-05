import datetime
from nsetools import Nse
import pyttsx3
import time

def fetch_indices(nse_client):
    """
    Fetch major indices from NSE (Nifty 50, Bank Nifty etc.)
    Returns a dict mapping index name → info dict
    """
    # nse.get_index_list() gives list of index names supported
    idx_list = nse_client.get_index_list()
    indices = {}
    for idx in idx_list:
        try:
            info = nse_client.get_index_quote(idx)
            # info is usually a dict
            if isinstance(info, dict):
                indices[idx] = info
        except Exception as e:
            # skip indices that error
            # print(f"Could not fetch {idx}: {e}")
            continue
    return indices

def fetch_top_movers(nse_client, num=5):
    """
    Fetch top gainers and top losers in market
    Returns two lists of dicts: gainers, losers
    """
    try:
        gainers = nse_client.get_top_gainers()  # returns list of dicts
    except Exception as e:
        gainers = []
    try:
        losers = nse_client.get_top_losers()
    except Exception as e:
        losers = []
    # if the returned list is longer, restrict
    gainers = gainers[:num]
    losers = losers[:num]
    return gainers, losers

def make_text_report(indices, gainers, losers):
    """
    Build a human‑readable summary text string from data
    """
    date_str = datetime.date.today().strftime("%d %b, %Y")
    text = f"Market Summary for {date_str}:\n"
    # Include Nifty 50 and Bank Nifty if available
    for name in ["NIFTY 50", "NIFTY BANK", "Nifty", "Bank Nifty"]:
        if name in indices:
            idx = indices[name]
            last = idx.get("lastPrice") or idx.get("last") or idx.get("value")
            change = idx.get("change")
            pct = idx.get("pChange") or idx.get("percentChange")
            text += f"{name}: {last}  Change: {change} ({pct}%)\n"
    # Top gainers
    text += "\nTop Gainers:\n"
    for g in gainers:
        sym = g.get("symbol")
        ch = g.get("change") or g.get("net_price") or g.get("perChange")
        pct = g.get("pChange") or g.get("perChange")
        text += f"{sym}: {ch} ({pct}%)  "
    # Top losers
    text += "\nTop Losers:\n"
    for l in losers:
        sym = l.get("symbol")
        ch = l.get("change") or l.get("net_price") or l.get("perChange")
        pct = l.get("pChange") or l.get("perChange")
        text += f"{sym}: {ch} ({pct}%)  "
    return text

def text_to_audio(text, filename="market_report.mp3"):
    """
    Convert text to speech and save as audio file
    """
    engine = pyttsx3.init()
    # optional: adjust speech rate, voice
    rate = engine.getProperty("rate")
    engine.setProperty("rate", rate - 20)  # slow down a bit
    engine.save_to_file(text, filename)
    engine.runAndWait()

def main():
    nse = Nse()
    try:
        # Fetch data
        indices = fetch_indices(nse)
        gainers, losers = fetch_top_movers(nse)
        # Generate report text
        report_text = make_text_report(indices, gainers, losers)
        print("=== Report Text ===")
        print(report_text)
        # Convert to audio
        text_to_audio(report_text, filename="market_report.mp3")
        print("Audio saved to market_report.mp3")
    except Exception as e:
        print("Error:", e)
    finally:
        # No special cleanup for nsetools
        pass

if __name__ == "__main__":
    main()
