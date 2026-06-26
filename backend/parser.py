import requests
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_product_id(url):
    match = re.search(r"prod/([A-Z0-9\-]+)", url)
    return match.group(1) if match else None


def parse_pchome(url):
    product_id = extract_product_id(url)

    if not product_id:
        return {
            "name": "Unknown",
            "price": None,
            "stock": False,
            "product_id": None
        }

    # 🔥 嘗試抓 PChome JSON API
    api_url = f"https://24h.pchome.com.tw/prod/api/prod/{product_id}"

    try:
        r = requests.get(api_url, headers=HEADERS, timeout=10)

        # 有些商品會 403 → fallback HTML
        if r.status_code != 200:
            return parse_html_fallback(url)

        data = r.json()

        return {
            "name": data.get("name") or data.get("nick") or "Unknown",
            "price": data.get("price"),
            "stock": data.get("stockQty", 0) > 0,
            "product_id": product_id
        }

    except Exception:
        return parse_html_fallback(url)


def parse_html_fallback(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    html = r.text

    # fallback only name
    m = re.search(r'<meta property="og:title" content="(.*?)"', html)
    name = m.group(1) if m else "Unknown"

    return {
        "name": name,
        "price": None,
        "stock": False,
        "product_id": None
    }