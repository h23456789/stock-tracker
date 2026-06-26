import { db } from "./supabase.js";

console.log("🔥 app.js loaded");

/**
 * 📦 載入商品
 */
async function load() {
  const { data, error } = await db
    .from("products")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    console.error(error);
    return;
  }

  const list = document.getElementById("list");

  list.innerHTML = data.map(p => `
    <div class="card">
      <h3>${p.name || "（未解析）"}</h3>
      <p>💰 ${p.price ?? "-"}</p>
      <p class="${p.stock ? "ok" : "no"}">
        ${p.stock ? "🟢 有貨" : "🔴 缺貨"}
      </p>

      <a href="${p.url}" target="_blank">開啟商品</a>

      <button onclick="deleteProduct('${p.id}')">
        刪除
      </button>
    </div>
  `).join("");
}

/**
 * ➕ 新增商品
 */
async function addProduct() {
  const url = document.getElementById("url").value.trim();

  if (!url) return alert("請輸入網址");

  const { error } = await db
    .from("products")
    .insert([{ url }]);

  if (error) {
    alert(error.message);
    return;
  }

  document.getElementById("url").value = "";
  load();
}

/**
 * 🗑 刪除商品
 */
async function deleteProduct(id) {
  const { error } = await db
    .from("products")
    .delete()
    .eq("id", id);

  if (error) {
    alert(error.message);
    return;
  }

  load();
}

/**
 * 🚀 初始化
 */
function init() {
  document.getElementById("addBtn")
    .addEventListener("click", addProduct);

  load();
}

window.deleteProduct = deleteProduct;

document.addEventListener("DOMContentLoaded", init);