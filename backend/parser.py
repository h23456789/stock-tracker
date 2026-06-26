import re
from bs4 import BeautifulSoup
from crawler import fetch_page


def parse_pchome(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")

    # 🧠 name（穩）
    name_tag = soup.select_one("meta[property='og:title']")
    name = name_tag["content"].strip() if name_tag else "Unknown"

    # 💰 price（從全文抓）
    price = None
    text = soup.get_text()

    m = re.search(r"NT\\$\\s?([0-9,]+)", text)
    if m:
        price = int(m.group(1).replace(",", ""))

    # 📦 stock（真正穩定版）
    html_lower = html.lower()

    if "已售完" in html_lower:
        stock = False
    elif "補貨中" in html_lower:
        stock = False
    elif "加入購物車" in html:
        stock = True
    elif "立即購買" in html:
        stock = True
    else:
        stock = False  # 保守避免誤判

    return {
        "name": name,
        "price": price,
        "stock": stock
    }