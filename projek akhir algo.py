import pandas as pd
import csv

File_user = "users.csv"        
File_menu = "menu.csv"
File_riwayat = "riwayat.csv"

Username_owner = "owner"
Password_owner = "admin123"
Batas_login = 3                 
Lebar_struk = 40
Minimal_transaksi_member = 3        
Persen_diskon = 10  

Kolom_users = ["username", "password"]                  
Kolom_menu = ["kode", "nama", "harga"]
Kolom_riwayat = ["id_transaksi", "username", "detail_pesanan", "total", "bayar", "kembalian"]

Menu_awal = [
    ["M01", "Nasi Putih", 5000],
    ["M02", "Ayam Goreng", 12000],
    ["M03", "Ikan Lele Goreng", 10000],
    ["M04", "Tempe Goreng", 3000],
    ["M05", "Tahu Goreng", 3000],
    ["M06", "Sayur Asem", 5000],
    ["M07", "Sambal Terasi", 2000],
    ["M08", "Es Teh Manis", 4000],
    ["M09", "Es Jeruk", 5000],
    ["M10", "Es Campur", 8000],
    ["M11", "Es Teler", 10000],
]


# =====================================================
#  FILE & DATA HANDLING
# =====================================================
def siapkan_file():
   
    try:
        pd.read_csv(File_user)
    except FileNotFoundError:
        df = pd.DataFrame({"username": [], "password": []})
        df.to_csv(File_user, index=False)

    try:
        pd.read_csv(File_menu)
    except FileNotFoundError:
        df = pd.DataFrame(Menu_awal, columns=Kolom_menu)
        df.to_csv(File_menu, index=False)

    try:
        pd.read_csv(File_riwayat)
    except FileNotFoundError:
        df = pd.DataFrame({"id_transaksi": [], "username": [], "detail_pesanan": [], "total": [], "bayar": [], "kembalian": []})
        df.to_csv(File_riwayat, index=False)


def baca_users():
    df = pd.read_csv(File_user)
    df = df.astype({"username": "str", "password": "str"})
    return df


def baca_menu():
    df = pd.read_csv(File_menu)
    df = df.astype({"kode": "str", "nama": "str", "harga": "int"})
    return df


def baca_riwayat():
    df = pd.read_csv(File_riwayat)
    df = df.astype({"id_transaksi": "str", "username": "str", "detail_pesanan": "str"})
    return df


def rupiah(angka):
    return "Rp %d" % angka


def garis(karakter="=", panjang=Lebar_struk):
    print(karakter * panjang)


def hitung_terjual():
    """Menghitung total porsi terjual tiap menu dari riwayat.csv.
    Mengembalikan dictionary {nama_menu: jumlah_porsi}."""
    df = baca_riwayat()
    terjual = {}
    for i in range(len(df)):
        daftar = df.at[i, "detail_pesanan"].split(" | ")
        for bagian in daftar:
            pisah = bagian.split(" x")
            nama = pisah[0]
            jumlah = int(pisah[-1])
            if nama in terjual:
                terjual[nama] += jumlah
            else:
                terjual[nama] = jumlah
    return terjual


def urutkan_terlaris():
    """Mengembalikan list [nama, jumlah] terurut dari yang paling laris."""
    terjual = hitung_terjual()
    daftar = []
    for nama in terjual:
        daftar.append([nama, terjual[nama]])

    # nested loop: urutkan menurun berdasarkan jumlah terjual
    for i in range(len(daftar)):
        for j in range(i + 1, len(daftar)):
            if daftar[j][1] > daftar[i][1]:
                daftar[i], daftar[j] = daftar[j], daftar[i]
    return daftar


def hitung_transaksi_user(username):
    df = baca_riwayat()
    return len(df[df["username"] == username])


def buat_item(kode, nama, harga, jumlah):
    """Mengembalikan dictionary satu item pesanan."""
    return {"kode": kode, "nama": nama, "harga": harga,
            "jumlah": jumlah, "subtotal": harga * jumlah}


# =====================================================
#  F-01  REGISTRASI & LOGIN CUSTOMER
# =====================================================
def registrasi():
    print("\n=== REGISTRASI PELANGGAN ===")
    df = baca_users()

    username = input("Username baru : ").lower()
    if username == "" or not username.isalnum():
        print("Username tidak valid! Gunakan huruf/angka tanpa spasi.")
        return
    if username in list(df["username"]) or username == Username_owner:
        print("Username sudah dipakai, coba yang lain.")
        return

    password = input("Password     : ")
    if password == "" or "," in password or " " in password:
        print("Password tidak boleh kosong, tanpa spasi dan tanpa koma!")
        return

    file = open(File_user, "a")
    file.write(f"{username},{password}\n")
    file.close()
    print(f"Registrasi berhasil! Silakan login, {username.capitalize()}.")


def login_customer():
    """Mengembalikan username kalau berhasil, None kalau gagal.
    Kalau username belum ada di users.csv, akun otomatis dibuat dan langsung masuk."""
    print("\n=== LOGIN CUSTOMER ===")
    percobaan = 1

    while percobaan <= Batas_login:
        df = baca_users()
        username = input("Username : ").lower()
        password = input("Password : ")

        # tidak boleh kosong (tidak dihitung sebagai percobaan)
        if username == "" or password == "":
            print("Username dan password tidak boleh kosong!")
            continue

        # username hanya huruf/angka, password tanpa spasi/koma
        if not username.isalnum() or username == Username_owner or "," in password or " " in password:
            print("Username dan password tidak valid (tanpa spasi, tanpa koma).")
            continue

        terdaftar = df[df["username"] == username]

        if len(terdaftar) == 0:
            # username baru -> otomatis tersimpan ke users.csv lalu langsung masuk
            file = open(File_user, "a")
            file.write(f"{username},{password}\n")
            file.close()
            print(f"Akun baru '{username}' otomatis dibuat. Selamat datang, {username.capitalize()}!")
            return username

        if terdaftar.iloc[0]["password"] == password:
            print(f"Login berhasil. Selamat datang, {username.capitalize()}!")
            return username

        print(f"Password salah. Sisa percobaan: {Batas_login - percobaan}")
        percobaan += 1

    print("Terlalu banyak percobaan gagal. Kembali ke menu utama.")
    return None


# =====================================================
#  F-02  LOGIN OWNER
# =====================================================
def login_owner():
    print("\n=== LOGIN OWNER / ADMIN ===")
    percobaan = 1

    while percobaan <= Batas_login:
        username = input("Username owner : ").lower()
        password = input("Password owner : ")

        if username == Username_owner and password == Password_owner:
            print("Login owner berhasil.")
            return True

        print(f"Akses ditolak. Sisa percobaan: {Batas_login - percobaan}")
        percobaan += 1

    print("Terlalu banyak percobaan gagal. Kembali ke menu utama.")
    return False


# =====================================================
#  F-03  TAMPILKAN DAFTAR MENU
# =====================================================
def tampilkan_menu():
    df = baca_menu()
    terlaris = urutkan_terlaris()
    nama_terlaris = ""
    if len(terlaris) > 0:
            nama_terlaris = terlaris[0][0]
    
    garis("=", 50)
    print("DAFTAR MENU PRASMANAN")
    garis("=", 50)
    print("Kode".ljust(8) + "Nama Menu".ljust(26) + "Harga".rjust(16))
    garis("-", 50)

    if len(df) == 0:
        print("Menu masih kosong.")
    else:
        for i in range(len(df)):
            nama = df.at[i, "nama"]
            if nama == nama_terlaris:
                nama = nama + "*" 
            print(df.at[i, "kode"].ljust(8) + nama.ljust(26) + rupiah(df.at[i, "harga"]).rjust(16))
        if nama_terlaris != "":
            print("* = Menu Terlaris")
    garis("=", 50)
    return df


# =====================================================
#  F-04  PEMESANAN   &   F-05  PEMBAYARAN & CETAK STRUK
# =====================================================
def cetak_struk(id_transaksi, username, keranjang, total, bayar, kembalian, diskon=0):
    print()
    garis("=")
    print("STRUK PEMBAYARAN")
    print("WARUNG PRASMANAN")
    garis("=")
    print(f"No. Transaksi : {id_transaksi}")
    print(f"Pelanggan     : {username.capitalize()}")
    garis("-")
    for item in keranjang:
        print(item["nama"])
        rincian = f"  {item['jumlah']} x {rupiah(item['harga'])}"
        print(rincian.ljust(24) + rupiah(item["subtotal"]).rjust(Lebar_struk - 24))
    garis("-")
    if diskon > 0:
        print("SUBTOTAL".ljust(20) + rupiah(total + diskon).rjust(Lebar_struk - 20))
        print(f"DISKON MEMBER {Persen_diskon}%".ljust(20) + ("-" + rupiah(diskon)).rjust(Lebar_struk - 20))
    print("TOTAL".ljust(20) + rupiah(total).rjust(Lebar_struk - 20))
    print("BAYAR".ljust(20) + rupiah(bayar).rjust(Lebar_struk - 20))
    print("KEMBALIAN".ljust(20) + rupiah(kembalian).rjust(Lebar_struk - 20))
    garis("=")
    print("Terima kasih, selamat menikmati!")
    garis("=")


def pesan_makanan(username):
    df = tampilkan_menu()
    if len(df) == 0:
        print("Maaf, menu belum tersedia.")
        return

    keranjang = []   # list berisi dictionary tiap item pesanan

    # ----- F-04: pilih lebih dari satu menu -----
    while True:
        kode = input("\nMasukkan kode menu (0 = selesai memilih): ").upper()

        if kode == "0":
            break

        cari = df[df["kode"] == kode]
        if len(cari) == 0:
            print("Kode menu tidak ditemukan!")
            continue

        jumlah_input = input("Jumlah porsi: ")
        if not jumlah_input.isdigit() or int(jumlah_input) <= 0:
            print("Jumlah harus berupa angka lebih dari 0!")
            continue

        jumlah = int(jumlah_input)
        nama = cari.iloc[0]["nama"]
        harga = int(cari.iloc[0]["harga"])

        # kalau menu sudah ada di keranjang, jumlahnya ditambah
        sudah_ada = False
        for item in keranjang:
            if item["kode"] == kode:
                item["jumlah"] += jumlah
                item["subtotal"] = item["jumlah"] * harga
                sudah_ada = True
        if not sudah_ada:
            keranjang.append(buat_item(kode, nama, harga, jumlah))

        print(f"-> {nama} x{jumlah} masuk keranjang.")

    if len(keranjang) == 0:
        print("Keranjang kosong, pesanan dibatalkan.")
        return

    # ----- hitung total otomatis -----
    total = 0
    print("\n--- Keranjang Pesanan ---")
    for nomor, item in enumerate(keranjang):
        print(f"{nomor + 1}. {item['nama'].ljust(20)} {item['jumlah']} x {rupiah(item['harga'])} = {rupiah(item['subtotal'])}")
        total += item["subtotal"]
    print(f"TOTAL BAYAR: {rupiah(total)}")

     # ----- fitur baru: diskon member loyal -----
    diskon = 0
    if hitung_transaksi_user(username) >= Minimal_transaksi_member:
        diskon = total * Persen_diskon // 100
        total = total - diskon
        print(f"Diskon member {Persen_diskon}% : -{rupiah(diskon)}")
    print(f"TOTAL BAYAR : {rupiah(total)}")
    

    # ----- F-05: pembayaran -----
    while True:
        bayar_input = input("Masukkan uang tunai (0 = batalkan pesanan): ")

        if not bayar_input.isdigit():
            print("Masukkan angka saja!")
            continue

        bayar = int(bayar_input)
        if bayar == 0:
            print("Pesanan dibatalkan.")
            return
        if bayar < total:
            print(f"Uang kurang {rupiah(total - bayar)}. Coba lagi.")
            continue
        break

    kembalian = bayar - total

    # ----- simpan ke riwayat.csv -----
    riwayat = baca_riwayat()
    id_transaksi = "PESANAN" + str(len(riwayat) + 1)
    detail = " | ".join([f"{item['nama']} x{item['jumlah']}" for item in keranjang])

    file = open(File_riwayat, "a")
    file.write(f"{id_transaksi},{username},{detail},{total},{bayar},{kembalian}\n")
    file.close()

    cetak_struk(id_transaksi, username, keranjang, total, bayar, kembalian, diskon)


# =====================================================
#  F-06  RIWAYAT PESANAN CUSTOMER
# =====================================================
def riwayat_customer(username):
    df = baca_riwayat()
    pesanan = df[df["username"] == username]
    pesanan.index = range(0, len(pesanan))

    print(f"\n=== RIWAYAT PESANAN {username.upper()} ===")
    if len(pesanan) == 0:
        print("Belum ada riwayat pesanan.")
        return

    for i in range(len(pesanan)):
        garis("-", 50)
        print(f"No. Transaksi : {pesanan.at[i, 'id_transaksi']}")
        print(f"Pesanan       : {pesanan.at[i, 'detail_pesanan']}")
        print(f"Total         : {rupiah(pesanan.at[i, 'total'])}")
    garis("-", 50)
    print(f"Jumlah transaksi: {len(pesanan)}")

    if len(pesanan) >= Minimal_transaksi_member:
            print(f"Status: Member (diskon {Persen_diskon}% setiap pesanan)")
    else:
        sisa = Minimal_transaksi_member - len(pesanan)
        print(f"Status: belum member, {sisa} transaksi lagi untuk diskon {Persen_diskon}%")
    


# =====================================================
#  F-07  PENGELOLAAN DATA MENU (OWNER)
# =====================================================
def tambah_menu():
    while True:
        print("\n--- TAMBAH MENU BARU ---")
        df = baca_menu()

        nama = input("Nama menu : ")
        harga_input = input("Harga     : ")

        if nama == "" or "," in nama:
            print("Nama tidak boleh kosong dan tidak boleh mengandung koma!")
        elif not harga_input.isdigit() or int(harga_input) <= 0:
            print("Harga harus berupa angka lebih dari 0!")
        else:
            # kode otomatis: cari nomor terbesar dari kode yang ada, lalu +1
            nomor_kode = [int(k[1:]) for k in df["kode"] if k[1:].isdigit()]
            terbesar = 0
            for n in nomor_kode:
                if n > terbesar:
                    terbesar = n
            nomor_baru = terbesar + 1

            if nomor_baru < 10:
                kode_baru = "M0" + str(nomor_baru)
            else:
                kode_baru = "M" + str(nomor_baru)

            file = open(File_menu, "a")
            file.write(f"{kode_baru},{nama},{int(harga_input)}\n")
            file.close()
            print(f"Menu '{nama}' berhasil ditambahkan dengan kode {kode_baru}.")

        lagi = input("Tambah menu lagi? (y/n): ").lower()
        if lagi != "y":
            break


def ubah_menu():
    df = tampilkan_menu()
    kode = input("Kode menu yang diubah (kosong = batal): ").upper()
    if kode == "":
        return

    if len(df[df["kode"] == kode]) == 0:
        print("Kode menu tidak ditemukan!")
        return

    lama = df[df["kode"] == kode].iloc[0]
    print(f"Data lama: {lama['nama']} - {rupiah(int(lama['harga']))}")
    nama_baru = input("Nama baru  (Enter = tidak diubah): ")
    harga_baru = input("Harga baru (Enter = tidak diubah): ")

    if nama_baru != "" and "," not in nama_baru:
        df.loc[df["kode"] == kode, "nama"] = nama_baru
    if harga_baru != "":
        if harga_baru.isdigit() and int(harga_baru) > 0:
            df.loc[df["kode"] == kode, "harga"] = int(harga_baru)
        else:
            print("Harga tidak valid, harga tidak diubah.")

    df.to_csv(File_menu, index=False)
    print("Data menu berhasil diperbarui.")


def hapus_menu():
    df = tampilkan_menu()
    kode = input("Kode menu yang dihapus (kosong = batal): ").upper()
    if kode == "":
        return

    if len(df[df["kode"] == kode]) == 0:
        print("Kode menu tidak ditemukan!")
        return

    yakin = input(f"Yakin hapus menu {kode}? (y/n): ").lower()
    if yakin == "y":
        df = df[df["kode"] != kode]
        df.index = range(0, len(df))
        df.to_csv(File_menu, index=False)
        print("Menu berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")


def kelola_menu():
    while True:
        print("\n=== KELOLA DATA MENU ===")
        print("1. Lihat menu")
        print("2. Tambah menu")
        print("3. Ubah menu")
        print("4. Hapus menu")
        print("0. Kembali ke menu owner")
        pilihan = input("Pilih: ")

        match pilihan:
            case "1":
                tampilkan_menu()
            case "2":
                tambah_menu()
            case "3":
                ubah_menu()
            case "4":
                hapus_menu()
            case "0":
                break
            case _:
                print("Pilihan tidak valid!")


# =====================================================
#  F-08  REKAP RIWAYAT & PENDAPATAN (OWNER)
# =====================================================
def rekap_riwayat():
    df = baca_riwayat()
    print("\n=== REKAP RIWAYAT & PENDAPATAN ===")

    if len(df) == 0:
        print("Belum ada transaksi.")
        return

    # kumpulkan nama pelanggan tanpa duplikat
    daftar_pelanggan = []
    for i in range(len(df)):
        if df.at[i, "username"] not in daftar_pelanggan:
            daftar_pelanggan.append(df.at[i, "username"])

    total_pendapatan = 0

    # nested loop: luar = tiap pelanggan, dalam = tiap transaksi pelanggan itu
    for pelanggan in daftar_pelanggan:
        garis("=", 50)
        print(f"Pelanggan: {pelanggan.upper()}")
        garis("-", 50)
        subtotal = 0

        for i in range(len(df)):
            if df.at[i, "username"] == pelanggan:
                print(f"{df.at[i, 'id_transaksi']}")
                print(f"   {df.at[i, 'detail_pesanan']}")
                print(f"   Total: {rupiah(int(df.at[i, 'total']))}")
                subtotal += int(df.at[i, "total"])

        print(f"Subtotal {pelanggan}: {rupiah(subtotal)}")
        total_pendapatan += subtotal

    garis("=", 50)
    rata_rata = total_pendapatan / len(df)   # hasil pembagian bertipe float
    print(f"Jumlah transaksi         : {len(df)}")
    print(f"Rata-rata per transaksi  : Rp {rata_rata}")
    print(f"Total Seluruh Pendapatan : {rupiah(total_pendapatan)}")
    garis("=", 50)


# =====================================================
#  F-09  MENU TERLARIS (CUSTOMER & OWNER)
# =====================================================
def tampilkan_terlaris():
    daftar = urutkan_terlaris()
    print("\n=== MENU TERLARIS ===")

    if len(daftar) == 0:
        print("Belum ada data penjualan.")
        return

    garis("=", 50)
    batas = 5
    if len(daftar) < batas:
        batas = len(daftar)

    for i in range(batas):
        nama = daftar[i][0]
        jumlah = daftar[i][1]
        print(f"{i + 1}. {nama.ljust(22)} {str(jumlah).rjust(3)} porsi  " + "#" * jumlah)
    garis("=", 50)


# =====================================================
#  MENU CUSTOMER, MENU OWNER, MENU UTAMA
# =====================================================
def menu_customer(username):
    while True:
        print(f"\n=== MENU CUSTOMER ({username.capitalize()}) ===")
        print("1. Lihat daftar menu")
        print("2. Pesan makanan")
        print("3. Riwayat pesanan saya")
        print("4. Menu terlaris")
        print("0. Logout")
        pilihan = input("Pilih: ")

        match pilihan:
            case "1":
                tampilkan_menu()
            case "2":
                lanjut = "y"
                while lanjut == "y":
                    pesan_makanan(username)
                    lanjut = input("\nLanjut pesan lagi? (y = lanjut, n = kembali ke login): ").lower()
                print("Kembali ke menu login...")
                break
            case "3":
                riwayat_customer(username)
            case "4":
                tampilkan_terlaris()
            case "0":
                print("Logout berhasil.")
                break
            case _:
                print("Pilihan tidak valid!")


def menu_owner():
    while True:
        print("\n=== MENU OWNER / ADMIN ===")
        print("1. Kelola data menu")
        print("2. Rekap riwayat & pendapatan")
        print("3. Menu terlaris")
        print("0. Logout")
        pilihan = input("Pilih: ")

        match pilihan:
            case "1":
                kelola_menu()
            case "2":
                rekap_riwayat()
            case "3":
                tampilkan_terlaris()
            case "0":
                print("Logout owner berhasil.")
                break
            case _:
                print("Pilihan tidak valid!")


# =====================================================
#  PROGRAM UTAMA
# =====================================================
siapkan_file()

while True:
    print("\n" + "=" * 40)
    print("  APLIKASI PEMESANAN MAKANAN PRASMANAN")
    print("=" * 40)
    print("1. Login Customer")
    print("2. Registrasi Customer")
    print("3. Login Owner")
    print("0. Keluar")
    pilihan = input("Pilih: ")

    match pilihan:
        case "1":
            user = login_customer()
            if user != None:
                menu_customer(user)
        case "2":
            registrasi()
        case "3":
            if login_owner():
                menu_owner()
        case "0":
            print("Terima kasih, sampai jumpa!")
            break
        case _:
            print("Pilihan tidak valid!")