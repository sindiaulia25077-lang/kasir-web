
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def kasir():
    hasil = None
    error = None

    if request.method == "POST":
        try:
            nama = request.form.getlist("nama[]")
            harga = request.form.getlist("harga[]")
            jumlah = request.form.getlist("jumlah[]")
            uang_bayar = int(request.form["uang_bayar"])

            daftar_barang = []
            subtotal = 0

            for i in range(len(nama)):
                if not nama[i].strip():
                    continue

                h = int(harga[i])
                j = int(jumlah[i])

                if h <= 0 or j <= 0:
                    raise ValueError(
                        "Harga dan jumlah harus lebih dari 0."
                    )

                total_barang = h * j
                subtotal += total_barang

                daftar_barang.append({
                    "nama": nama[i],
                    "harga": h,
                    "jumlah": j,
                    "total": total_barang
                })

            if not daftar_barang:
                raise ValueError(
                    "Masukkan minimal satu barang."
                )

            if uang_bayar < 0:
                raise ValueError(
                    "Uang pembayaran tidak boleh negatif."
                )

            # Diskon 5% jika belanja minimal Rp100.000
            diskon = 0
            if subtotal >= 100000:
                diskon = int(subtotal * 0.05)

            total_bayar = subtotal - diskon
            kembalian = uang_bayar - total_bayar

            hasil = {
                "barang": daftar_barang,
                "subtotal": subtotal,
                "diskon": diskon,
                "total_bayar": total_bayar,
                "uang_bayar": uang_bayar,
                "kembalian": kembalian
            }

            if kembalian < 0:
                error = (
                    "Uang pembayaran kurang Rp"
                    + f"{abs(kembalian):,}".replace(",", ".")
                )
                hasil = None

        except ValueError as e:
            error = str(e) or "Masukkan angka yang valid."
        except (KeyError, TypeError):
            error = "Data transaksi belum diisi dengan benar."

    return render_template(
        "index.html",
        hasil=hasil,
        error=error
    )


import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
