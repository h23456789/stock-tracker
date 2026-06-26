from supabase_client import supabase
from parser import parse_pchome
from telegram import send

def run():
    products = supabase.table("products").select("*").execute().data

    for p in products:
        if not p.get("enabled", True):
            continue

        data = parse_pchome(p["url"])

        old_stock = bool(p.get("stock", False))
        old_price = p.get("price")

        # 🧠 update DB
        res = supabase.table("products").update({
            "name": data["name"],
            "price": data["price"],
            "last_price": old_price,
            "stock": data["stock"],
            "product_id": data["product_id"]
        }).eq("id", p["id"]).execute()

        if hasattr(res, "error") and res.error:
            print("UPDATE ERROR:", res.error)

        # 🔔 補貨通知
        if (not old_stock) and data["stock"]:
            send(f"""🟢 補貨通知

{data['name']}

💰 NT${data['price']}
📦 現在有貨

🔗 {p['url']}""")

        # 📉 降價通知（安全版）
        if (
            old_price is not None and
            data["price"] is not None and
            isinstance(data["price"], int) and
            data["price"] < old_price
        ):
            send(f"""📉 降價通知

{data['name']}

{old_price} → {data['price']}

🔗 {p['url']}""")

if __name__ == "__main__":
    run()