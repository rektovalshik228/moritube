import requests
from datetime import datetime, timezone

# ─────────────────── НАСТРОЙКИ ───────────────────
BASE_URL  = "https://scan.layerzero-api.com/v1/messages"
ADDRESS   = "0x8a4e91cc8e1a47b15bf9cfdb34087a1fec35411a"
START_ISO = "2024-06-22T00:00:00.000Z"
END_ISO   = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")
LIMIT     = 100
# ─────────────────────────────────────────────────

def fetch_batch(params):
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    return r.json()

def count_direction(direction_key: str) -> int:
    total     = 0
    nextToken = None

    while True:
        params = {
            "limit":      LIMIT,
            "start":      START_ISO,
            "end":        END_ISO,
            direction_key: ADDRESS,
        }
        if nextToken:
            params["nextToken"] = nextToken

        data = fetch_batch(params)
        batch = data.get("data") or data.get("messages") or []
        if not batch:
            break

        # согласно спеке, поле времени здесь — "created"
        for msg in batch:
            t = msg.get("created")
            if t:
                ts = datetime.fromisoformat(t.replace("Z","+00:00"))
                # все, что строго после 22.06.2024 00:00 UTC
                if ts > datetime(2024,6,22,tzinfo=timezone.utc):
                    total += 1

        nextToken = data.get("nextToken")
        if not nextToken or len(batch) < LIMIT:
            break

    return total

if __name__ == "__main__":
    # считаем исходящие (от srcAddress) и входящие (на dstAddress)
    out_count = count_direction("srcAddress")
    in_count  = count_direction("dstAddress")

    print(f"\nИсходящих сообщений после 2024-06-22: {out_count}")
    print(f"Входящих сообщений  после 2024-06-22: {in_count}")
    print(f"Итого LayerZero-сообщений: {out_count + in_count}")


