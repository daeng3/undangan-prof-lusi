# -*- coding: utf-8 -*-
"""Menyisipkan potret (base64) ke templat dan menulis index.html final."""
import base64
import os

TEMPLATE = os.path.join("scripts", "template.html")
OUT = "index.html"

with open("assets/potret.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")

with open(TEMPLATE, encoding="utf-8") as f:
    html = f.read()

if "__FOTO__" not in html:
    raise SystemExit("Placeholder __FOTO__ tidak ditemukan.")

html = html.replace("__FOTO__", "data:image/jpeg;base64," + b64)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print(OUT + ":", round(os.path.getsize(OUT) / 1024, 1), "KB")
