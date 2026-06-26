import requests
import re
from bs4 import BeautifulSoup

def parse_pchome(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    # 商品名稱
    name_tag = soup.select_one("meta[property='og:title']")
    name = name_tag["content"] if name_tag else "Unknown"

    # 價格
    price = None
    price_tag = soup.select_one(".price, .value")
    if price_tag:
        price = int(re.sub(r"[^0-9]", "", price_tag.text))

    # 判斷庫存
    stock = "售完" not in r.text and "已售完" not in r.text

    # product_id（簡易抓法）
    match = re.search(r"prod/([A-Z0-9\-]+)", url)
    product_id = match.group(1) if match else None

    return {
        "name": name,
        "price": price,
        "stock": stock,
        "product_id": product_id
    }