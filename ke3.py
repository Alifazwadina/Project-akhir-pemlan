import csv
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import socket

# Nama file CSV untuk menyimpan data
filename = 'bank-additional.csv'

# Fungsi untuk mengimpor data dari file CSV
def import_data_from_csv():
    data = []
    if os.path.exists(filename):
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            data = [row for row in reader]
        print("Data berhasil diimpor dari", filename)
    else:
        print(filename, "tidak ditemukan.")
    return data

# Fungsi untuk menampilkan data dalam bentuk dictionary dengan header
def display_data_dict():
    for entry in data:
        for key, value in entry.items():
            print(f"{key}: {value}")
        print("")

# Fungsi untuk menambahkan data ke dalam list
def add_data():
    age = entry_age.get()
    job = entry_job.get()
    marital = entry_marital.get()
    education = entry_education.get()
    new_data = [age, job, marital, education]
    
    with open(filename, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_data)
    messagebox.showinfo("Info", "Data berhasil ditambahkan!")

# Fungsi untuk memperbarui data dalam list
def update_data():
    try:
        row_index = int(entry_row.get())
        with open(filename, mode='r') as file:
            rows = list(csv.reader(file))
            if 0 < row_index < len(rows):
                age = entry_age.get()
                job = entry_job.get()
                marital = entry_marital.get()
                education = entry_education.get()
                
                data = [age, job, marital, education]
                rows[row_index] = data

                with open(filename, mode='w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)
                messagebox.showinfo("Info", f"Data dengan nomor {row_index} berhasil diperbarui.")
            else:
                messagebox.showerror("Error", "Masukkan nomor yang valid.")
    except ValueError:
        messagebox.showerror("Error", "Masukkan nomor yang valid.")

# Fungsi untuk menghapus data dalam list
def delete_data():
    try:
        index = int(entry_index.get())
        with open(filename, mode='r') as file:
            rows = list(csv.reader(file))
            if 0 < index < len(rows):
                del rows[index]
                with open(filename, mode='w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)
                    messagebox.showinfo("Info", f"Data dengan nomor {index} berhasil dihapus.")
            else:
                messagebox.showerror("Error", "Masukkan nomor yang valid.")
    except ValueError:
        messagebox.showerror("Error", "Masukkan nomor yang valid.")

# Fungsi untuk mencari data dalam file CSV berdasarkan umur
def search():
    age = entry_search.get()
    result_text.delete(1.0, tk.END)  # Clear existing text
    result_text.insert(tk.END, f"Data dengan usia {age} adalah:\n")
    
    count = 0
    for row in data:
        if age == row['age']:
            count += 1
            result_text.insert(tk.END, f"\nData ke-{count}\n")
            result_text.insert(tk.END, f"Age: {row['age']} \nJob: {row['job']} \nMarital: {row['marital']} \nEducation: {row['education']} \n")
    
    if count == 0:
        result_text.insert(tk.END, "Data tidak ditemukan.")
    result_text.insert(tk.END, f"\nJumlah data: {count}\n")

# Fungsi untuk menampilkan bantuan
def show_help():
    help_text = (
        "\nPusat Bantuan\n"
        "Pilihan 'Tampilkan data' akan menampilkan seluruh data yang ada pada file.\n"
        "Pilihan 'Tambah data' akan memberi akses kepada user untuk menambah data pada file.\n"
        "Pilihan 'Perbarui data' akan memberi akses kepada user untuk memperbarui data yang sudah ada.\n"
        "Pilihan 'Hapus data' akan memberi akses kepada user untuk menghapus data pada file.\n"
        "Pilihan 'Cari data' akan memberi akses kepada user untuk mencari data sesuai umur.\n"
    )
    result_text.delete(1.0, tk.END)  # Clear existing text
    result_text.insert(tk.END, help_text)

# Fungsi untuk memulai server
def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Handling client requests can be implemented here
        # For simplicity, let's just acknowledge the connection for now
        client_socket.sendall(b"Connection established.")

# Fungsi untuk menjalankan GUI
def main():
    global data

    # Inisialisasi data
    data = import_data_from_csv()

    # Inisialisasi GUI
    root = tk.Tk()
    root.title("Bank Marketing Database")

    # Label dan Entry untuk menambah data
    ttk.Label(root, text="Tambah Data").grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Label(root, text="Usia (Age):").grid(row=1, column=0, sticky=tk.W, padx=5)
    ttk.Label(root, text="Pekerjaan (Job):").grid(row=2, column=0, sticky=tk.W, padx=5)
    ttk.Label(root, text="Status Pernikahan (Marital):").grid(row=3, column=0, sticky=tk.W, padx=5)
    ttk.Label(root, text="Pendidikan (Education):").grid(row=4, column=0, sticky=tk.W, padx=5)

    entry_age = ttk.Entry(root)
    entry_job = ttk.Entry(root)
    entry_marital = ttk.Entry(root)
    entry_education = ttk.Entry(root)

    entry_age.grid(row=1, column=1)
    entry_job.grid(row=2, column=1)
    entry_marital.grid(row=3, column=1)
    entry_education.grid(row=4, column=1)

    ttk.Button(root, text="Tambah Data", command=add_data).grid(row=5, column=0, columnspan=2, pady=10)

    # Label dan Entry untuk memperbarui data
    ttk.Label(root, text="Perbarui Data").grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Label(root, text="Nomor Baris:").grid(row=7, column=0, sticky=tk.W, padx=5)

    entry_row = ttk.Entry(root)
    entry_row.grid(row=7, column=1)

    ttk.Button(root, text="Perbarui Data", command=update_data).grid(row=8, column=0, columnspan=2, pady=10)

    # Label dan Entry untuk menghapus data
    ttk.Label(root, text="Hapus Data").grid(row=9, column=0, columnspan=2, pady=10)
    ttk.Label(root, text="Nomor Data:").grid(row=10, column=0, sticky=tk.W, padx=5)

    entry_index = ttk.Entry(root)
    entry_index.grid(row=10, column=1)

    ttk.Button(root, text="Hapus Data", command=delete_data).grid(row=11, column=0, columnspan=2, pady=10)

    # Label dan Entry untuk mencari data
    ttk.Label(root, text="Cari Data").grid(row=12, column=0, columnspan=2, pady=10)
    ttk.Label(root, text="Usia untuk Dicari:").grid(row=13, column=0, sticky=tk.W, padx=5)

    entry_search = ttk.Entry(root)
    entry_search.grid(row=13, column=1)

    ttk.Button(root, text="Cari Data", command=search).grid(row=14, column=0, columnspan=2, pady=10)

    # Button untuk menampilkan bantuan
    ttk.Button(root, text="Bantuan", command=show_help).grid(row=15, column=0, columnspan=2, pady=10)

    # Text untuk menampilkan hasil pencarian dan bantuan
    result_text = tk.Text(root, height=10, width=50)
    result_text.grid(row=16, column=0, columnspan=2, pady=10)

    # Multi-threading untuk menjalankan server
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Menjalankan GUI
    root.mainloop()

if __name__ == "__main__":
    main()
