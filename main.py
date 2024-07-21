import mysql.connector
import logging

# A. Membuat Kelas Buku di Python
class Buku:
    # Initializer
    def __init__(self, judul, penulis, penerbit, tahun_terbit, konten, ikhtisar):
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.konten = konten
        self.ikhtisar = ikhtisar
    
    # Method Wajib
    def read(self, halaman_awal, halaman_akhir):
        for i in range(halaman_awal, halaman_akhir + 1):
            print(f"Konten halaman {i}: {self.konten[i-1]}")
    
    def __str__(self):
        return f"{self.judul} by {self.penulis}"
    
# B. Membuat table buku yang berisi ketiga atribut pada system basis data
# Query ada dalam file db.sql

# C. Membuat Method GET untuk Mengambil Data dari Basis Data
def get_buku_by_id(buku_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="perpustakaan"
    )
    cursor = conn.cursor()
    query = "SELECT * FROM buku WHERE id = %s"
    cursor.execute(query, (buku_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return Buku(*result[1:])
    return None

# D. Membuat Method POST untuk Menyimpan Kelas Buku
def save_buku(buku):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="perpustakaan"
        )
        cursor = conn.cursor()
        query = "INSERT INTO buku (judul, penulis, penerbit, tahun_terbit, konten, ikhtisar) VALUES (%s, %s, %s, %s, %s, %s)"
        konten_str = ",".join(buku.konten)  
        cursor.execute(query, (buku.judul, buku.penulis, buku.penerbit, buku.tahun_terbit, konten_str, buku.ikhtisar))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        log_error(f"Error: {err}")
        print(f"Error: {err}")

# E. Membuat Logger dan HTTP Exception
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(error_message):
    logging.error(error_message)

class HTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")

# Contoh Penggunaan
buku_sample = Buku(
    judul="Belajar Python",
    penulis="John Doe",
    penerbit="matahari",
    tahun_terbit=2021,
    konten=["Bab 1: Pendahuluan", "Bab 2: Variabel", "Bab 3: Fungsi"],
    ikhtisar="Buku ini memberikan panduan dasar untuk belajar Python."
)

print(buku_sample)  # Output: Belajar Python by John Doe

save_buku(buku_sample)
print("Buku berhasil disimpan ke database.")

buku_dari_db = get_buku_by_id(1)  # Mengambil buku dengan id = 1

if buku_dari_db:
    print(buku_dari_db)  # Output: Belajar Python by John Doe
    buku_dari_db.read(1, 2)  # Output: Konten halaman 1: Bab 1: Pendahuluan
                             #         Konten halaman 2: Bab 2: Variabel
else:
    print("Buku tidak ditemukan di database.")
