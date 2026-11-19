# -*- coding: utf-8 -*-
"""Membuat salinan uji dengan apiUrl diarahkan ke server tiruan lokal."""
import io

REAL = "https://script.google.com/macros/s/AKfycbzRLBbteJKeCzuDuY3tVBOKeGJaNJYFfggu2KhD9vazrR6seYX7cAxPBuLI2ego_mhL/exec"
MOCK = "http://127.0.0.1:8765/exec"

src = io.open("index.html", encoding="utf-8").read()
out = src.replace(REAL, MOCK, 1)
assert out != src, "URL apiUrl tidak ditemukan"
io.open("_test-api.html", "w", encoding="utf-8", newline="\n").write(out)
print("_test-api.html dibuat")
