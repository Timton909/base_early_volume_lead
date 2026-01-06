import requests, time

def volume_lead():
    print("Base — Volume Leads Price (volume spike before price move)")
    history = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            now = time.time()

            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                vol5 = pair.get("volume", {}).get("m5", 0) or 0
                change5 = pair.get("priceChange", {}).get("m5", 0) or 0
                age = now - pair.get("pairCreatedAt", 0) / 1000

                if age > 600: continue

                if addr not in history:
                    history[addr] = (now, vol5)
                    continue

                last_t, last_vol = history[addr]
                vol_spike = vol5 / last_vol if last_vol > 0 else 0

                if vol_spike > 10 and abs(change5) < 30:
                    token = pair["baseToken"]["symbol"]
                    print(f"VOLUME LEADS PRICE\n"
                          f"{token} volume ×{vol_spike:.0f} — price only {change5:+.0f}%\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Volume screaming — price sleeping\n"
                          f"→ Pump incoming in seconds\n"
                          f"{'LEAD'*30}")
                    del history[addr]

                history[addr] = (now, vol5)

        except:
            pass
        time.sleep(5.1)

if __name__ == "__main__":
    volume_lead()
