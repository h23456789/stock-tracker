import { db } from "./supabase.js";

/**
 * 🔥 讀取商品列表
 */
async function load() {
  const { data, error } = await db.from("products").select("*");

  if (error) {
    console.error("LOAD ERROR:", error);
    alert("載入失敗：" + error.message);
    return;
  }

  const list = document.getElementById("list");

  if (!data || data.length === 0) {
    list.innerHTML = "<p>目前沒有追蹤商品</p>";
    return;
  }

  list.innerHTML = data.map(p => `
    <div class="card">
      <h3>${p.name || "（尚未解析）"}</h3>

      <p class="stock ${p.stock ? "ok" : "no"}">
        ${p.stock ? "🟢 有貨" : "🔴 缺貨"}
      </p>

      <p>💰 ${p.price ?? "-"}</p>

      <a href="${p.url}" target="_blank">🔗 前往商品</a>
    </div>
  `).join("");
}


/**
 * 🔥 新增商品
 */
async function addProduct() {
  const urlInput = document.getElementById("url");
  const url = urlInput.value.trim();

  if (!url) {
    alert("請輸入商品網址");
    return;
  }

  console.log("🚀 新增商品:", url);

  const { data, error } = await db.from("products").insert([
    { url }
  ]);

  if (error) {
    console.error("INSERT ERROR:", error);
    alert("新增失敗：" + error.message);
    return;
  }

  console.log("✅ 新增成功:", data);

  urlInput.value = "";

  await load();
}


/**
 * 🔥 初始化
 */
function init() {
  const btn = document.getElementById("addBtn");

  if (!btn) {
    console.error("❌ 找不到 addBtn（HTML 有問題）");
    return;
  }

  btn.addEventListener("click", addProduct);

  console.log("✅ app.js 初始化完成");
  load();
}

init();