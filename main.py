import csv
from datetime import datetime

CSV_FILE = "menu.csv"
CSV_FILE_LAPORAN = "laporan.csv"

menu = {}
antrian = []

def load_minuman():
    try:
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                menu[row['id']] = {'nama': row['nama'], 'harga': int(row['harga'])}
    except FileNotFoundError:
        pass

def save_minuman():
    with open(CSV_FILE, mode='w', newline='') as csv_file:
        fieldnames = ['id', 'nama', 'harga']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for id, data in menu.items():
            writer.writerow({'id': id, 'nama': data['nama'], 'harga': data['harga']})

def save_laporan(pesanan, total):
    with open(CSV_FILE_LAPORAN, mode='w', newline='') as file:
        fieldnames = ['tanggal', 'nama_pelanggan', 'minuman', 'total']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'tanggal' : datetime.now().strftime('%Y-%m-%d %H:%M'),
            'nama_pelanggan' : pesanan['nama_pelanggan'],
            'minuman' : menu[pesanan['id_minuman']]['nama'],
            'total' : total
            
        })

def read_laporan():
    with open('laporan.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        print("TANGGAL \t\t NAMA PELANGGAN \t MINUMAN \t TOTAL")
        print("-" * 72)

        for data in csv_reader:
            print(f"{data['tanggal']} \t {data['nama_pelanggan']} \t\t {data['minuman']} \t Rp{int(data['total']):.2f}")
        print("-" * 72)



def read_minuman():
    with open('menu.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        print("ID \t NAMA \t\t HARGA")
        print("-" * 32)

        for data in csv_reader:
            print(f"{data['id']} \t {data['nama']} \t Rp{int(data['harga']):.2f}")
        print("-" * 32)


def add_minuman():
    id = len(menu) + 1
    nama = input("Nama Minuman: ")
    harga = int(input("Harga Minuman: "))
    menu[id] = {'nama': nama, 'harga': harga}
    save_minuman()
    print("Minuman berhasil ditambah")

def edit_minuman():
    id = input("ID Minuman yang ingin di ubah: ")
    if id in menu:
        nama = input("Minuman baru: ")
        harga = int(input("Harga baru: "))
        menu[id] = {'nama': nama, 'harga': harga}
        save_minuman()
        print("Minuman berhasil diubah.")
    else:
        print("ID tidak ada.")

def hapus_minuman():
    id = int(input("ID Minuman yang dihapus: "))
    if id in menu:
        del menu[id]
        save_minuman()
        print("Minuman berhasil dihapus")
    else:
        print("ID Minuman tidak ada.")

def pengaturan_minuman():
    print("PENGATURAN MENU")
    print("1. Tambah Menu \t 2. Edit Menu \t 3. Hapus Menu")

    pilihan = input('Pilih Menu Pengaturan: ')

    if pilihan == '1':
        add_minuman()
    elif pilihan == '2':
        edit_minuman()
    elif pilihan == '3':
        hapus_minuman()
    else:
        print("Pilihan tersebut tidak ada.")

def tambah_antrian():
    read_minuman()
    nama_pelanggan = input("Nama Pelanggan: ")
    id_minuman = input("ID Minuman yang dipesan: ")
    if id_minuman not in menu:
        print("Minuman tidak ditemukan.")
        return
    jumlah = int(input("Jumlah Pesanan: "))
    antrian.append({"nama_pelanggan": nama_pelanggan, "id_minuman": id_minuman, "jumlah": jumlah})
    print("Pesanan berhasil ditambahkan ke antrian.")

def lihat_antrian():
    if not antrian:
        print("Tidak ada antrian.")
    else:
        print("Daftar Antrian:")
        for i, pesanan in enumerate(antrian):
            minum = menu[pesanan["id_minuman"]]
            total = pesanan["jumlah"] * minum["harga"]
            print(f"{i+1}. {pesanan['nama_pelanggan']} - {minum['nama']} ({pesanan['jumlah']}x) = Rp{total:.2f}")

def proses_antrian():
    if not antrian:
        print("Tidak ada antrian.")
    else:
        pesanan = antrian.pop(0)
        minum = menu[pesanan["id_minuman"]]
        total = pesanan["jumlah"] * minum["harga"]
        print(f"Pesanan {pesanan['nama_pelanggan']} sedang diproses: {minum['nama']} ({pesanan['jumlah']}x), Total: Rp{total:.2f}")
        save_laporan(pesanan, total)


def main():
    load_minuman()
    while True:
        print("\n=== APLIKASI PEMESANAN MINUMAN ===")
        read_minuman()
        print("1. Tambah Antrian Pesanan")
        print("2. Lihat Antrian")
        print("3. Proses Antrian")
        print("4. Pengaturan Menu")
        print("5. Laporan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            tambah_antrian()
        elif pilihan == '2':
            lihat_antrian()
        elif pilihan == '3':
            proses_antrian()
        elif pilihan == '4':
            pengaturan_minuman()
        elif pilihan == '5':
            read_laporan()
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()


