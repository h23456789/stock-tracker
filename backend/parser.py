from playwright.sync_api import sync_playwright
import re

def parse_pchome(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 🚨 關鍵1：不要用 networkidle
        page.goto(url, wait_until="domcontentloaded")

        # 🚨 關鍵2：強制等 UI render
        page.wait_for_timeout(6000)

        html = page.content()

        # 🧠 name
        name_match = re.search(
            r'<meta property="og:title" content="(.*?)"',
            html
        )
        name = name_match.group(1) if name_match else page.title()

        # 💰 price（從整頁抓）
        price = None
        m = re.search(r'NT\\$\\s?([0-9,]+)', html)
        if m:
            price = int(m.group(1).replace(",", ""))

        # 📦 stock（🔥核心修正）
        stock = False

        # ✔ 正確判斷（看「按鈕是否存在 + 沒 disabled」）
        try:
            btn = page.locator("text=加入購物車")

            if btn.count() > 0:
                disabled = btn.first.get_attribute("disabled")
                stock = disabled is None
        except:
            stock = False

        # fallback（避免漏判）
        if "已售完" in html or "補貨中" in html:
            stock = False

        return {
            "name": name,
            "price": price,
            "stock": stock
        }