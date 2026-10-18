// Minimal local license server for the NoteVault "fixed" demo.
// The signing secret lives ONLY here, never in the client binary.
// Runs on 127.0.0.1 only. Fake test secret.
import { createServer } from "node:http";
import { createHmac } from "node:crypto";

const SERVER_SECRET = "nv-server-secret-only-on-the-server";
const PORT = Number(process.argv[2] || 8799);

// A legit key is NV-<6 digit id>-<first 8 hex of HMAC(SERVER_SECRET, id)>
function approve(key) {
  const parts = String(key).split("-");
  if (parts.length !== 3 || parts[0] !== "NV" || parts[1].length !== 6) return false;
  const mac = createHmac("sha256", SERVER_SECRET).update(parts[1]).digest("hex").slice(0, 8).toUpperCase();
  return mac === parts[2].toUpperCase();
}

const server = createServer((req, res) => {
  if (req.method === "POST" && req.url === "/license/verify") {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", () => {
      let key = "";
      try { key = JSON.parse(body).key; } catch { /* ignore */ }
      const ok = approve(key);
      res.writeHead(200, { "content-type": "application/json" });
      res.end(JSON.stringify({ approved: ok }));
    });
    return;
  }
  res.writeHead(404);
  res.end();
});
server.listen(PORT, "127.0.0.1", () => console.log(`license server on 127.0.0.1:${PORT}`));
