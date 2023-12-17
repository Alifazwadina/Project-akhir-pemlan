import tkinter as tk
from tkinter import messagebox
import pandas as pd

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Cek jika username dan password sesuai
    if username == "admin" and password == "2222":
        messagebox.showinfo("Login", "Login berhasil!")
        create_main_menu()  # Panggil fungsi pembuatan menu utama setelah login berhasil
    else:
        messagebox.showerror("Login", "Username atau password salah")

def create_main_menu():
    login_frame.pack_forget()  # Sembunyikan frame login setelah login berhasil
    menu_frame = tk.Frame(root, padx=20, pady=20)
    menu_frame.pack()

    # Buat tombol-tombol menu
    tk.Button(menu_frame, text="Tampilkan Data", command=show_data).pack()
    tk.Button(menu_frame, text="Tambah Data").pack()
    tk.Button(menu_frame, text="Perbarui Data").pack()
    tk.Button(menu_frame, text="Hapus Data").pack()
    tk.Button(menu_frame, text="Cari Data").pack()
    tk.Button(menu_frame, text="Bantuan").pack()
    tk.Button(menu_frame, text="Keluar", command=root.destroy).pack()

def show_data():
    # Load data dari file CSV (ganti 'nama_file.csv' dengan nama file CSV yang sesuai)
    try:
        data = pd.read_csv('bank-additional-full.csv')  # Ubah nama_file.csv sesuai dengan nama file CSV Anda
        # Tampilkan data dalam GUI atau buat jendela baru untuk menampilkan data
        data_window = tk.Toplevel(root)
        data_text = tk.Text(data_window)
        data_text.pack()

        # Menampilkan data dalam text widget
        data_text.insert(tk.END, data.to_string(index=False))  # Menampilkan data tanpa index
    except FileNotFoundError:
        messagebox.showerror("File Error", "File CSV tidak ditemukan!")

# Membuat window
root = tk.Tk()
root.title("Sistem Data Marketing")

# Membuat frame untuk login
login_frame = tk.Frame(root, padx=20, pady=20)
login_frame.pack()

# Label dan Entry untuk username
username_label = tk.Label(login_frame, text="Username:")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

# Label dan Entry untuk password
password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

# Tombol Login
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2)

# Menjalankan aplikasi
root.mainloop()
