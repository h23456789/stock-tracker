from playwright.sync_api import sync_playwright

def parse_pchome(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)  # ⭐關鍵：讓 API 跑完

        # 🧠 強制抓「按鈕是否可用」
        buy_btn = page.query_selector("text=加入購物車")

        stock = False
        if buy_btn:
            disabled = buy_btn.get_attribute("disabled")
            stock = disabled is None

        # fallback（避免漏判）
        if "已售完" in page.content():
            stock = False

        # name
        name = page.title()

        return {
            "name": name,
            "stock": stock
        }