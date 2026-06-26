import re
from bs4 import BeautifulSoup
from crawler import fetch_page


def parse_pchome(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")

    # 🧠 name
    name_tag = soup.select_one("meta[property='og:title']")
    name = name_tag["content"].strip() if name_tag else "Unknown"

    # 💰 price（從畫面抓數字）
    price = None
    text = soup.get_text()

    m = re.search(r"NT\$?\\s?([0-9,]+)", text)
    if m:
        price = int(m.group(1).replace(",", ""))

    # 📦 stock（關鍵：看按鈕）
    stock = False

    if soup.select_one("button:contains('加入購物車')"):
        stock = True
    elif "已售完" in text:
        stock = False
    elif "補貨中" in text:
        stock = False
    else:
        stock = True  # fallback（避免誤判沒貨）

    return {
        "name": name,
        "price": price,
        "stock": stock
    }