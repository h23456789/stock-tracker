import requests
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_product_id(url):
    match = re.search(r"prod/([A-Z0-9\-]+)", url)
    return match.group(1) if match else None


def detect_stock(html):
    if "已售完" in html or "補貨中" in html:
        return False
    if "加入購物車" in html or "立即購買" in html:
        return True
    return True  # 避免誤判沒貨


def parse_pchome(url):
    product_id = extract_product_id(url)

    r = requests.get(url, headers=HEADERS, timeout=10)
    html = r.text

    # 🧠 name
    m = re.search(r'<meta property="og:title" content="(.*?)"', html)
    name = m.group(1) if m else "Unknown"

    # 💰 price（只做輔助）
    price = None
    m2 = re.search(r'"price"\s*:\s*"?(\d+)"?', html)
    if m2:
        price = int(m2.group(1))

    # 📦 stock（關鍵改這裡）
    stock = detect_stock(html)

    return {
        "name": name,
        "price": price,
        "stock": stock,
        "product_id": product_id
    }