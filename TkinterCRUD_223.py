import sqlite3 # Import modul sqlite3 untuk mengelola database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk # Import modul GUI tkinter

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') # Koneksi ke database (file otomatis dibuat kalau belum ada)
    cursor = conn.cursor() # Membuat cursor untuk eksekusi SQL
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS nilai_siswa ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''') # Buat tabel nilai_siswa kalau belum ada
    conn.commit() # Simpan perubahan ke database
    conn.close() # Tutup koneksi ke database

# Mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db') # Buka koneksi ke database
    cursor = conn.cursor() # Buat cursor untuk eksekusi SQL
    cursor.execute("SELECT * FROM nilai_siswa") # Ambil semua data dari tabel
    rows = cursor.fetchall() # Ambil hasil query
    conn.close() # Tutup koneksi database
    return rows # Kembalikan data sebagai list

# Menyimpan data siswa baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db') # Buka koneksi ke database
    cursor = conn.cursor() # Buat cursor untuk eksekusi SQL
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi)) # Simpan data ke tabel
    conn.commit() # Simpan perubahan
    conn.close() # Tutup koneksi database

# Memperbarui data siswa yang sudah ada di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db') # Buka koneksi ke database
    cursor = conn.cursor() # Buat cursor untuk eksekusi SQL
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Update data berdasarkan ID
    conn.commit() # Simpan perubahan
    conn.close() # Tutup koneksi database

# Menghapus data siswa dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db') # Buka koneksi ke database
    cursor = conn.cursor() # Buat cursor untuk eksekusi SQL
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) # Hapus data berdasarkan ID
    conn.commit() # Simpan perubahan
    conn.close() # Tutup koneksi database

# Menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris: # Jika nilai biologi terbesar
        return "Kedokteran" # Prediksi fakultas Kedokteran
    elif fisika > biologi and fisika > inggris: # Jika nilai fisika terbesar
        return "Teknik" # Prediksi fakultas Teknik
    elif inggris > biologi and inggris > fisika: # Jika nilai inggris terbesar
        return "Bahasa" # Prediksi fakultas Bahasa
    else: 
        return "Tidak Diketahui" # Prediksi tidak jelas

# Fungsi untuk tambah data
def submit():
    try:
        nama = nama_var.get() # Ambil nama dari input
        biologi = int(biologi_var.get()) # Ambil nilai biologi dan ubah ke int
        fisika = int(fisika_var.get()) # Ambil nilai fisika dan ubah ke int
        inggris = int(inggris_var.get()) # Ambil nilai inggris dan ubah ke int
        if not nama: # Kalau nama kosong
            raise Exception("Nama siswa tidak boleh kosong.") # Muncul pesan error
        prediksi = calculate_prediction(biologi, fisika, inggris) # Prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi) # Simpan ke database
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}") # Pesan sukses
        clear_inputs() # Bersihkan input
        populate_table() # Refresh tabel
    except ValueError as e: # Jika input salah format
        messagebox.showerror("Error", f"Input tidak valid: {e}") # Tampilkan pesan error

#  Memperbarui data siswa yang dipilih
def update():
    try:
        if not selected_record_id.get(): # Kalau belum pilih data di tabel
            raise Exception("Pilih data dari tabel untuk di-update!") # Pesan error
        record_id = int(selected_record_id.get()) # Ambil ID dari record yang dipilih
        nama = nama_var.get() # Ambil nama dari input
        biologi = int(biologi_var.get()) # Ambil nilai biologi
        fisika = int(fisika_var.get()) # Ambil nilai fisika
        inggris = int(inggris_var.get()) # Ambil nilai inggris
        if not nama: # Kalau nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.") # Pesan error
        prediksi = calculate_prediction(biologi, fisika, inggris) # Prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi) # Update data di database
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!") # Pesan sukses
        clear_inputs() # Bersihkan input
        populate_table() # Refresh tabel
    except ValueError as e: # Kalau ada error saat input
        messagebox.showerror("Error", f"Kesalahan: {e}") # Tampilkan pesan error

# Menghapus data siswa yang dipilih
def delete():
    try:
        if not selected_record_id.get(): # Kalau belum pilih data di tabel
            raise Exception("Pilih data dari tabel untuk dihapus!") # Pesan error
        record_id = int(selected_record_id.get()) # Ambil ID record
        delete_database(record_id) # Hapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!") # Pesan sukses
        clear_inputs() # Bersihkan input
        populate_table() # Refresh tabel
    except ValueError as e: # Kalau ada error
        messagebox.showerror("Error", f"Kesalahan: {e}") # Tampilkan pesan error

# Membersihkan semua input di form
def clear_inputs():
    nama_var.set("") # Kosongkan input nama
    biologi_var.set("") # Kosongkan input biologi
    fisika_var.set("") # Kosongkan input fisika
    inggris_var.set("") # Kosongkan input inggris
    selected_record_id.set("") # Kosongkan ID yang dipilih

# Mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children(): # Hapus semua isi tabel
        tree.delete(row) # Hapus satu per satu
    for row in fetch_data(): # Ambil data dari database
        tree.insert('', 'end', values=row) # Masukkan data ke tabel

# Mengisi form dengan data dari tabel yang dipilih
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] # Ambil item yang dipilih di tabel
        selected_row = tree.item(selected_item)['values'] # Ambil data dari item
        selected_record_id.set(selected_row[0]) # Set ID record yang dipilih
        nama_var.set(selected_row[1]) # Isi input nama
        biologi_var.set(selected_row[2]) # Isi input biologi
        fisika_var.set(selected_row[3]) # Isi input fisika
        inggris_var.set(selected_row[4]) # Isi input inggris
    except IndexError: # Kalau tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!") # Pesan error

# Inisialisasi database
create_database() # Buat database dan tabel kalau belum ada

# Membuat GUI dengan tkinter
root = Tk() # Buat jendela utama aplikasi
root.title("Prediksi Fakultas Siswa") # Set judul aplikasi

# Variabel tkinter
nama_var = StringVar() # Variabel untuk input nama
biologi_var = StringVar() # Variabel untuk input biologi
fisika_var = StringVar() # Variabel untuk input fisika
inggris_var = StringVar() # Variabel untuk input inggris
selected_record_id = StringVar() # Variabel untuk ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5) # Label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Input nama siswa

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5) # Label untuk nilai biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5) # Input nilai biologi

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5) # Label untuk nilai fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Input nilai fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5) # Label untuk nilai inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5) # Input nilai inggris

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10) # Tombol untuk tambah data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10) # Tombol untuk update data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10) # Tombol untuk hapus data

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas") # Kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings') # Buat tabel

# Mengatur posisi isi tabel di tengah
for col in columns: # Loop untuk semua kolom
    tree.heading(col, text=col.capitalize()) # Set nama kolom
    tree.column(col, anchor='center') # Set teks kolom di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10) # Posisi tabel di GUI

tree.bind('<ButtonRelease-1>', fill_inputs_from_table) # Event klik tabel untuk isi form

populate_table() # Tampilkan data awal di tabel

root.mainloop() # Jalankan aplikasi GUI

