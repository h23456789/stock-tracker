import { db } from "./supabase.js";

// 🔥 讀取商品
async function load() {
  const { data, error } = await db.from("products").select("*");

  if (error) {
    console.error(error);
    return;
  }

  document.getElementById("list").innerHTML =
    data.map(p => `
      <div style="padding:10px;margin:10px;background:#fff">
        <h3>${p.name || "未解析"}</h3>
        <p>${p.stock ? "🟢 有貨" : "🔴 缺貨"}</p>
        <p>💰 ${p.price || "-"}</p>
        <a href="${p.url}" target="_blank">前往商品</a>
      </div>
    `).join("");
}

// 🔥 新增商品（重點修復）
window.addProduct = async function () {
  const url = document.getElementById("url").value;

  console.log("新增商品:", url);

  const { data, error } = await db.from("products").insert([
    { url }
  ]);

  if (error) {
    console.error("新增失敗:", error);
    alert(error.message);
    return;
  }

  console.log("新增成功:", data);

  document.getElementById("url").value = "";

  load();
};

// 初始化
load();