from supabase_client import supabase
from parser import parse_pchome
from telegram import send

def run():
    products = supabase.table("products").select("*").execute().data

    for p in products:
        if not p["enabled"]:
            continue

        data = parse_pchome(p["url"])

        old_stock = p["stock"]
        old_price = p["price"]

        # 更新 DB
        supabase.table("products").update({
            "name": data["name"],
            "price": data["price"],
            "last_price": old_price,
            "stock": data["stock"],
            "product_id": data["product_id"]
        }).eq("id", p["id"]).execute()

        # 🔔 補貨
        if not old_stock and data["stock"]:
            send(f"""🟢 補貨通知

{data['name']}

💰 NT${data['price']}
📦 現在有貨

🔗 {p['url']}""")

        # 📉 降價
        if old_price and data["price"] and data["price"] < old_price:
            send(f"""📉 降價通知

{data['name']}

{old_price} → {data['price']}

🔗 {p['url']}""")

if __name__ == "__main__":
    run()