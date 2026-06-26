import { db } from "./supabase.js";

console.log("🔥 app.js loaded");

/**
 * 🔄 讀取列表
 */
async function load() {
  const { data, error } = await db
    .from("products")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    console.error("LOAD ERROR:", error);
    return;
  }

  const list = document.getElementById("list");

  if (!data || data.length === 0) {
    list.innerHTML = "<p>目前沒有追蹤商品</p>";
    return;
  }

  list.innerHTML = data.map(p => `
    <div class="card">
      <h3>${p.name || "（尚未解析商品）"}</h3>

      <p>💰 價格：${p.price ?? "未取得"}</p>

      <p class="${p.stock ? "ok" : "no"}">
        ${p.stock ? "🟢 有貨" : "🔴 無貨"}
      </p>

      <a href="${p.url}" target="_blank">🔗 前往商品</a>

      <button onclick="deleteProduct('${p.id}')">
        🗑 刪除
      </button>
    </div>
  `).join("");
}

/**
 * ➕ 新增商品（先只存 URL）
 */
async function addProduct() {
  const input = document.getElementById("url");
  const url = input.value.trim();

  if (!url) {
    alert("請輸入網址");
    return;
  }

  console.log("➕ add:", url);

  const { data, error } = await db
    .from("products")
    .insert([{ url }])
    .select()
    .single();

  if (error) {
    console.error("INSERT ERROR:", error);
    alert(error.message);
    return;
  }

  input.value = "";

  // 🔄 先重新載入（之後 parser 可補資料）
  load();
}

/**
 * 🗑 刪除商品
 */
async function deleteProduct(id) {
  console.log("🗑 delete:", id);

  const { error } = await db
    .from("products")
    .delete()
    .eq("id", id);

  if (error) {
    console.error("DELETE ERROR:", error);
    alert(error.message);
    return;
  }

  load();
}

/**
 * 🎯 初始化
 */
function init() {
  const btn = document.getElementById("addBtn");

  if (!btn) {
    console.error("❌ 找不到 addBtn");
    return;
  }

  btn.addEventListener("click", addProduct);

  console.log("✅ init done");

  load();
}

/**
 * 🌍 掛到 window（給 onclick 用）
 */
window.deleteProduct = deleteProduct;

/**
 * 🚀 DOM ready
 */
document.addEventListener("DOMContentLoaded", init);