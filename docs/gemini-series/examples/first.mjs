import { GoogleGenAI } from "@google/genai";

if (!process.env.GEMINI_API_KEY) throw new Error("請先設定 GEMINI_API_KEY");
const client = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const reply = await client.interactions.create({
  model: process.env.GEMINI_MODEL || "gemini-3.8-flash",
  input: "請用繁體中文列出整理活動公告時應核對的三個欄位。",
  store: false,
});
if (reply.status !== "completed" || !reply.output_text) throw new Error("回覆未完成或沒有文字");
console.log(reply.output_text);
