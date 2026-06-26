import requests
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_product_id(url):
    match = re.search(r"prod/([A-Z0-9\-]+)", url)
    return match.group(1) if match else None


def parse_pchome(url):
    product_id = extract_product_id(url)

    if not product_id:
        return fallback(url)

    # 🔥 1. 嘗試 API
    api_url = f"https://24h.pchome.com.tw/prod/api/prod/{product_id}"

    try:
        r = requests.get(api_url, headers=HEADERS, timeout=10)

        # ❌ API 不穩就 fallback
        if r.status_code != 200:
            return fallback(url)

        # ❌ 有些回 HTML（不是 JSON）
        try:
            data = r.json()
        except:
            return fallback(url)

        name = data.get("name") or data.get("nick") or "Unknown"

        # ⚠️ stock 強化（避免 None）
        stock_qty = data.get("stockQty")
        stock = True if (isinstance(stock_qty, int) and stock_qty > 0) else False

        price = data.get("price")

        return {
            "name": name,
            "price": price,
            "stock": stock,
            "product_id": product_id
        }

    except Exception:
        return fallback(url)


def fallback(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        html = r.text

        # 🧠 name
        m = re.search(r'<meta property="og:title" content="(.*?)"', html)
        name = m.group(1) if m else "Unknown"

        # ⚠️ fallback stock（只當參考，不準）
        stock = (
            "已售完" not in html and
            "補貨中" not in html
        )

        return {
            "name": name,
            "price": None,
            "stock": stock,
            "product_id": None
        }

    except Exception:
        return {
            "name": "ERROR",
            "price": None,
            "stock": False,
            "product_id": None
        }