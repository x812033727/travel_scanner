import subprocess, sys, tempfile, pathlib
svg = pathlib.Path(sys.argv[1]); png = sys.argv[2]
page = "<!doctype html><meta charset='utf-8'><style>html,body{margin:0;padding:0;background:#fff}svg{display:block;width:1600px;height:900px}</style>" + svg.read_text(encoding="utf-8")
with tempfile.TemporaryDirectory() as d:
    h = pathlib.Path(d) / "r.html"; h.write_text(page, encoding="utf-8")
    r = subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome","--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1","--window-size=1600,1000",f"--screenshot={png}",h.as_uri()],capture_output=True,text=True,timeout=120)
    print(r.returncode, r.stderr[-200:])
