# -*- coding: utf-8 -*-
"""Pemeriksaan akhir index.html: sintaks JS, referensi id, dan sisa placeholder."""
import re
import subprocess
import sys
import tempfile
import os

html = open("index.html", encoding="utf-8").read()
masalah = []

# 1. placeholder / alamat uji
for token in ("__FOTO__", "127.0.0.1", "localhost", "GANTI-DENGAN"):
    if token in html:
        masalah.append("Masih ada token: " + token)

# 2. ambil blok script terakhir (aplikasi)
scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
if not scripts:
    masalah.append("Tidak menemukan blok <script>")
app = scripts[-1]

# 3. sintaks JS via node --check
tmp = os.path.join(tempfile.gettempdir(), "undangan_check.js")
open(tmp, "w", encoding="utf-8").write(app)
try:
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True, shell=True)
    if r.returncode != 0:
        masalah.append("node --check gagal: " + (r.stderr or r.stdout).strip()[:400])
except Exception as e:
    masalah.append("Tidak dapat menjalankan node --check: " + str(e))

# 4. semua id yang dirujuk JS harus ada di HTML
ids = set(re.findall(r"id=\"([^\"]+)\"", html))
dirujuk = set(re.findall(r"\$\('([^']+)'\)", app)) | set(re.findall(r"getElementById\('([^']+)'\)", app))
hilang = sorted(i for i in dirujuk if i not in ids)
if hilang:
    masalah.append("id dirujuk tetapi tidak ada: " + ", ".join(hilang))

# 5. panjang & jumlah elemen penting
info = {
    "ukuran_KB": round(len(html.encode()) / 1024, 1),
    "jumlah_id": len(ids),
    "jumlah_rundown": len(re.findall(r"<li[^>]*><span class=\"no\">", html)),
    "ada_og_image": 'property="og:image"' in html,
}

print("INFO:", info)
if masalah:
    print("MASALAH:")
    for m in masalah:
        print(" -", m)
    sys.exit(1)
print("LULUS: tidak ada masalah terdeteksi.")
