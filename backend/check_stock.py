from supabase_client import supabase
from parser import parse_pchome
from telegram import send


def run():
    products = supabase.table("products").select("*").execute().data

    for p in products:
        data = parse_pchome(p["url"])

        old_stock = p.get("stock", False)
        old_price = p.get("price")

        # 💾 update DB
        supabase.table("products").update({
            "name": data["name"],
            "price": data["price"],
            "stock": data["stock"]
        }).eq("id", p["id"]).execute()

        # 🔔 補貨通知
        if not old_stock and data["stock"]:
            send(f"""🟢 補貨通知
{data['name']}
💰 {data['price']}
🔗 {p['url']}""")

        # 📉 降價通知
        if (
            old_price is not None and
            data["price"] is not None and
            data["price"] < old_price
        ):
            send(f"""📉 降價通知
{data['name']}
{old_price} → {data['price']}
🔗 {p['url']}""")


if __name__ == "__main__":
    run()