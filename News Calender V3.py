import asyncio
import aiohttp
import sys
import io
import time
from datetime import datetime, timezone
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from playsound import playsound

#------------------ first vesion doing well on news reslt show in cmd Prompt not in excel -----------------------
# --- UTF-8 STABILITY ---
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
NEWS_QUANTITY =  2 # how much news you want to see   

# --- CONFIGURATION ---
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

class FinancialBot:
    def __init__(self):
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        self.sia = SentimentIntensityAnalyzer()
        self.seen_news = set()

    def format_latency(self, seconds):
        if seconds < 60: return f"{seconds}s ago"
        elif seconds < 3600: return f"{seconds // 60}m ago"
        else: return f"{seconds // 3600}h {(seconds % 3600) // 60}m ago"

    def analyze_sentiment(self, text):
        score = self.sia.polarity_scores(text)
        if score['compound'] >= 0.05: return "BULLISH (Strength)"
        if score['compound'] <= -0.05: return "BEARISH (Weakness)"
        return "NEUTRAL"

    def identify_affected_pairs(self, headline):
        """Maps keywords to specific trading instruments."""
        h = headline.upper()
        pairs = []
        
        # USD / Gold / Safe Havens
        if any(k in h for k in ["FED", "FOMC", "USD", "USA", "WASHINGTON", "YIELD", "TREASURY"]):
            pairs.extend(["EURUSD", "USDJPY", "GBPUSD", "XAUUSD"])
        # EUR / ECB
        if any(k in h for k in ["ECB", "EUR", "EUROZONE", "LAGARDE", "GERMAN", "FRANCE"]):
            pairs.extend(["EURUSD", "EURJPY", "EURGBP"])
        # GBP / UK
        if any(k in h for k in ["BOE", "GBP", "UK ", "POUND", "BRITISH", "LONDON"]):
            pairs.extend(["GBPUSD", "EURGBP", "GBPJPY"])
        # JPY / Japan
        if any(k in h for k in ["BOJ", "YEN", "JAPAN", "TOKYO", "UEDA"]):
            pairs.extend(["USDJPY", "EURJPY", "GBPJPY"])
        # AUD / NZD
        if any(k in h for k in ["RBA", "AUD", "AUSTRALIA", "CHINA"]):
            pairs.extend(["AUDUSD", "AUDJPY"])
        if any(k in h for k in ["RBNZ", "NZD", "NEW ZEALAND"]):
            pairs.extend(["NZDUSD"])
        # CAD / Oil
        if any(k in h for k in ["BOC", "CAD", "CANADA", "OIL", "WTI", "CRUDE"]):
            pairs.extend(["USDCAD", "CADJPY"])
        # Commodities / Metals
        if any(k in h for k in ["GOLD", "XAU", "SILVER", "XAG", "METAL", "MINING"]):
            pairs.extend(["XAUUSD", "XAGUSD"])
        # Geopolitics (Safe Havens)
        if any(k in h for k in ["WAR", "CONFLICT", "ATTACK", "CRISIS", "SANCTION"]):
            pairs.extend(["XAUUSD (Safe Haven)", "USDCHF", "USDJPY"])

        # Deduplicate and return
        unique_pairs = list(set(pairs))
        return ", ".join(unique_pairs) if unique_pairs else "Broad Market Indices (SPX, DXY)"

    def display_news_box(self, headline, latency_seconds, source_type):
        """The UI for the news alert showing the IMPACTED PAIRS clearly."""
        sentiment = self.analyze_sentiment(headline)
        affected_instruments = self.identify_affected_pairs(headline)
        time_str = self.format_latency(latency_seconds)
        
        # Clean headline for display
        display_head = headline.encode('ascii', 'ignore').decode('ascii')
        if len(display_head) > 65: display_head = display_head[:62] + "..."

        print(f"\n╔{'═'*74}╗")
        print(f"║ SOURCE:   {source_type.ljust(61)} ║")
        print(f"║ TIME:     {time_str.ljust(61)} ║")
        print(f"║ SENTIMENT:{sentiment.ljust(61)} ║")
        print(f"╠{'═'*74}╣")
        print(f"║ EFFECTED PAIRS: {affected_instruments.ljust(56)} ║")
        print(f"╠{'═'*74}╣")
        print(f"║ HEADLINE: {display_head.ljust(61)} ║")
        print(f"╚{'═'*74}╝")

    async def fetch_recent_history(self):
        """Fetches the last 5 news items on startup."""
        print("\n[!] INITIALIZING MARKET MEMORY - ANALYZING RECENT IMPACTS...")
        url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        for item in reversed(data[:10]):    # News Count
                            self.seen_news.add(item['id'])
                            latency = int(time.time()) - item['datetime']
                            self.display_news_box(item['headline'], latency, "HISTORICAL IMPACT")
            except:
                print("--- Could not fetch history, skipping to live monitor ---")
        print("\n[!] STARTING LIVE MONITORING [Polling every 15s]\n")

    async def monitor_news(self):
        url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
        async with aiohttp.ClientSession() as session:
            while True:
                print(".", end="", flush=True)
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            for item in data[:3]:
                                if item['id'] not in self.seen_news:
                                    self.seen_news.add(item['id'])
                                    latency = int(time.time()) - item['datetime']
                                    try: playsound('urgent_beep.mp3', block=False)
                                    except: pass
                                    self.display_news_box(item['headline'], latency, "LIVE BREAKING NEWS")
                    await asyncio.sleep(15)
                except: await asyncio.sleep(30)

    async def run(self):
        await self.fetch_recent_history()
        await self.monitor_news()

if __name__ == "__main__":
    bot = FinancialBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n[!] Bot Offline. Trading Session Ended.")