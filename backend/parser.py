import requests
import re
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_pchome(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    # 🧠 1. 商品名稱（最穩）
    name_tag = soup.select_one("meta[property='og:title']")
    name = name_tag["content"].strip() if name_tag else "Unknown"

    # 💰 2. 價格（多層 fallback）
    price = None

    # fallback A: JSON price
    m = re.search(r'"price"\s*:\s*"?(\d+)"?', html)
    if m:
        price = int(m.group(1))

    # fallback B: meta description（有時有）
    if not price:
        m2 = re.search(r'(\d{2,8})\s*元', html)
        if m2:
            price = int(m2.group(1))

    # fallback C: fallback class（保留你原本）
    if not price:
        price_tag = soup.select_one(".price, .value")
        if price_tag:
            p = re.sub(r"[^0-9]", "", price_tag.text)
            if p:
                price = int(p)

    # 📦 3. 庫存判斷（稍微升級）
    stock_keywords = ["已售完", "售完", "無庫存", "補貨中", "缺貨"]
    stock = not any(k in html for k in stock_keywords)

    # 🆔 product id
    match = re.search(r"prod/([A-Z0-9\-]+)", url)
    product_id = match.group(1) if match else None

    return {
        "name": name,
        "price": price,
        "stock": stock,
        "product_id": product_id
    }