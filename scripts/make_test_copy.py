# -*- coding: utf-8 -*-
"""Membuat salinan uji dengan apiUrl diarahkan ke server tiruan lokal."""
import io

src = io.open("undangan.html", encoding="utf-8").read()
out = src.replace('apiUrl: ""', 'apiUrl: "http://127.0.0.1:8765/exec"', 1)
assert out != src, "Placeholder apiUrl tidak ditemukan"
io.open("_test-api.html", "w", encoding="utf-8", newline="\n").write(out)
print("_test-api.html dibuat")
