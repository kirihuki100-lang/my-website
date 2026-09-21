#!/usr/bin/env python3
"""静的ページ生成（プリレンダリング）。

assets/app.js（データとアプリ本体）を更新したら、リポジトリ直下で
    python3 tools/build.py
を実行すると、各URL用の index.html・sitemap.xml が再生成されます。
必要: pip install playwright（Chromiumが入っていること）
"""
import hashlib, http.server, json, os, re, socketserver, threading, datetime, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://j-reit-hub.com"
os.chdir(ROOT)

def ver(p):
    return hashlib.md5((ROOT / p).read_bytes()).hexdigest()[:8]

SHELL = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jリート・ハブ</title><meta name="description" content="Jリート（不動産投資信託）とは何かをやさしく解説し、銘柄ごとの物件・LTV・分配金・借入金利を数字で見比べられる入門ガイド。">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/assets/style.css?v=%(css)s">
</head><body><header class="top"><div class="top-in"><div class="brand"><a href="/" style="color:inherit;text-decoration:none"><b>Jリート・ハブ</b></a><span>Jリート（不動産投資信託）を、数字でやさしく比べる</span></div><nav class="tabs" id="tabs" aria-label="メニュー"></nav></div></header>
<main id="app"></main>
<script src="/assets/chart.min.js?v=%(chart)s"></script>
<script src="/assets/app.js?v=%(app)s"></script></body></html>
"""

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        # 開発用: どのパスでも shell を返す（SPAフォールバック）
        path = self.path.split("?")[0]
        if path.startswith("/assets/") or path.endswith((".png", ".ico")):
            return super().do_GET()
        body = pathlib.Path("/tmp/_shell.html").read_bytes()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

def main():
    shell = SHELL % dict(css=ver("assets/style.css"), chart=ver("assets/chart.min.js"), app=ver("assets/app.js"))
    pathlib.Path("/tmp/_shell.html").write_text(shell, encoding="utf-8")
    srv = socketserver.TCPServer(("127.0.0.1", 0), Q); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}"
    urls = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium"))
        pg = b.new_page(color_scheme="light")
        pg.goto(base + "/"); pg.wait_for_selector("#app h1")
        ids = pg.evaluate("D.map(r=>r.id)")
        routes = ["/", "/overview/", "/all/", "/compare/", "/props/", "/data/"] + [f"/reit/{i}/" for i in ids]
        for r in routes:
            pg.goto(base + r); pg.wait_for_selector("#app h1")
            pg.evaluate("killCharts()")
            html = "<!DOCTYPE html>\n" + pg.evaluate("document.documentElement.outerHTML")
            out = ROOT / (r.strip("/") or ".") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            urls.append(r); print("wrote", out.relative_to(ROOT))
        b.close()
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = "1.0" if u == "/" else ("0.8" if u.count("/") == 2 else "0.6")
        sm.append(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    srv.shutdown()

if __name__ == "__main__":
    main()
