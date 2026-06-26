import { db } from "./supabase.js";

console.log("🔥 app.js loaded");

async function addProduct() {
  const url = document.getElementById("url").value;

  console.log("addProduct:", url);

  const { error } = await db.from("products").insert([{ url }]);

  if (error) {
    alert(error.message);
    return;
  }

  load();
}

async function load() {
  const { data } = await db.from("products").select("*");

  document.getElementById("list").innerHTML =
    data.map(p => `
      <div>
        <h3>${p.name || "未解析"}</h3>
        <a href="${p.url}" target="_blank">開啟</a>
      </div>
    `).join("");
}

/**
 * ⭐ 關鍵：用 DOM 綁定，不用 onclick
 */
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("addBtn");

  console.log("btn =", btn);

  btn.addEventListener("click", addProduct);

  load();
});