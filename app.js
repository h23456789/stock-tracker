import { db } from "./supabase.js";

async function add() {
  const url = document.getElementById("url").value;

  const { error } = await db.from("products").insert([
    { url }
  ]);

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

// ⭐ 關鍵修復
window.add = add;

load();