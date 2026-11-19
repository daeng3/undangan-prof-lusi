# -*- coding: utf-8 -*-
"""Server tiruan Google Apps Script (JSONP) untuk menguji integrasi undangan.
Bukan bagian dari undangan; hanya alat verifikasi lokal.
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DATA = [
    {"nama": "Asep Hidayat", "instansi": "Universitas Bakti Tunas Husada", "kehadiran": "Hadir",
     "jumlah": 2, "waktu": "2026-11-19T03:10:00.000Z"},
    {"nama": "Rina Marlina", "instansi": "SMAN 1 Tasikmalaya", "kehadiran": "Tidak hadir",
     "jumlah": 0, "waktu": "2026-11-18T09:00:00.000Z"},
]
LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _kirim(self, body, ctype):
        raw = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        cb = q.get("callback", "")
        if u.path != "/exec":
            self.send_response(404)
            self.end_headers()
            return
        if q.get("action") == "kirim":
            nama = (q.get("nama") or "").strip()
            if len(nama) < 2:
                hasil = {"ok": False, "pesan": "Nama wajib diisi."}
            else:
                with LOCK:
                    DATA[:] = [d for d in DATA if d["nama"].lower() != nama.lower()]
                    DATA.insert(0, {
                        "nama": nama,
                        "instansi": (q.get("instansi") or "").strip(),
                        "kehadiran": "Hadir" if "tidak" not in (q.get("kehadiran") or "").lower() else "Tidak hadir",
                        "jumlah": int(q.get("jumlah") or 1) if "tidak" not in (q.get("kehadiran") or "").lower() else 0,
                        "waktu": "2026-11-19T06:00:00.000Z",
                    })
                hasil = {"ok": True, "data": {"nama": nama}}
        else:
            with LOCK:
                hasil = {"ok": True, "data": sorted(DATA, key=lambda d: d["waktu"], reverse=True)}
        body = (cb + "(" + json.dumps(hasil) + ");") if cb else json.dumps(hasil)
        self._kirim(body, "application/javascript; charset=utf-8")


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
