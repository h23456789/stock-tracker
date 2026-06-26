import requests
import re
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_pchome(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # 🧠 商品名稱
        name_tag = soup.select_one("meta[property='og:title']")
        name = name_tag["content"].strip() if name_tag else "Unknown"

        # 💰 價格（更穩：多 fallback）
        price = None

        # fallback 1
        price_tag = soup.select_one(".price, .value")
        if price_tag:
            price_text = re.sub(r"[^0-9]", "", price_tag.text)
            if price_text:
                price = int(price_text)

        # fallback 2（JSON）
        if not price:
            m = re.search(r'"price":\s*"?(\d+)"?', r.text)
            if m:
                price = int(m.group(1))

        # 📦 庫存判斷（更穩）
        stock_keywords = ["已售完", "售完", "無庫存", "補貨中"]
        stock = not any(k in r.text for k in stock_keywords)

        # 🆔 product id
        match = re.search(r"prod/([A-Z0-9\-]+)", url)
        product_id = match.group(1) if match else None

        return {
            "name": name,
            "price": price,
            "stock": stock,
            "product_id": product_id
        }

    except Exception as e:
        return {
            "name": "ERROR",
            "price": None,
            "stock": False,
            "product_id": None,
            "error": str(e)
        }