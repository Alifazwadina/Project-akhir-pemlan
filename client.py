# server code (unfinished)
# kalo mau lgsg edit disini aja pencet gambar pensil di kanan atas

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import logging
from pandastable import Table
import pandas as pd
import socket
import threading

class BankClient:
    host = "address"
    port = 5000
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Data Nasabah Bank ABC")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#add8e6")
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((BankClient.host, BankClient.port))
        self.login_frame()

    def login_frame(self):
        login_frame = ttk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title_label = ttk.Label(login_frame, text="Welcome!", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        ttk.Label(login_frame, text="Username:", font=("Helvetica", 10)).grid(row=1, column=0, padx=10, pady=5)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=1, column=1, padx=15, pady=10)

        ttk.Label(login_frame, text="Password:", font=("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=15, pady=10)

        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "2222":
            self.main_frame()
        else:
            messagebox.showerror("Login Failed", "Username or password is incorrect.")

    def main_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        buttons = [
            ("Tampilkan Data", self.display_data),
            ("Tambah Data", self.add_data),
            ("Perbarui Data", self.update_data),
            ("Hapus Data", self.delete_data),
            ("Cari Data", self.search_data),
            ("Help", self.show_help),
            ("Keluar", self.exit_app)
        ]

        for text, command in buttons:
            button = ttk.Button(frame, text=text, command=command)
            button.pack(side=tk.TOP, anchor=tk.CENTER, pady=10, padx=70, fill=tk.X)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def sync_server(self):
        threading.Thread(target=self.export_data).start()
        threading.Thread(target=self.import_data).start()

    def export_data(self):
        self.c.sendall(b'export_data')
        response = self.c.recv(1024).decode()
        if response == 'ready':
            data = self.c.recv(4096).decode()
            new_data = pd.read_csv(pd.compat.StringIO(data))
            self.data = pd.concat([self.data, new_data])
    
    def import_data(self):
        self.c.sendall(b'import_data')
        response = self.c.recv(1024).decode()
        if response == 'ready':
            self.c.sendall(self.data.to_csv(index=False).encode())
            messagebox.showinfo("import", "data synced.")

    def add_data(self):
        self.c.sendall(b'add_data')
        new_window = tk.Toplevel(self.root)
        new_window.title("Tambah Data")
        new_window.geometry("250x250")
        new_window.resizable(False, False)

        columns = ["Nama", "Umur", "Pekerjaan", "No.Telepon", "Status", "Alamat"]
        entries = []
        for i, column in enumerate(columns):
            ttk.Label(new_window, text=column, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(new_window)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries.append(entry)
        ttk.Button(new_window, text="Tambah Data", command=lambda: self.client_program(entries)).grid(row=len(columns), column=0, columnspan=2, pady=10)

        # response = self.c.recv(1024).decode()
        # messagebox.showinfo("Tambah data", response)

    def update_data(self):
        self.c.sendall(b'update_data')
        new_window = tk.Toplevel(self.root)
        new_window.title("Perbarui Data")
        new_window.geometry("300x280")
        new_window.resizable(False, False)

        ttk.Label(new_window, text="Nomor Baris:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        row_entry = ttk.Entry(new_window)
        row_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        labels = ["Mengganti Nama:","Umur Baru:", "Mengganti Pekerjaan:", "Mengganti No.Telepon:", "Mengganti Status:","Mengubah Alamat:"]
        entries = []
        for i, label in enumerate(labels):
            ttk.Label(new_window, text=label, anchor="w").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(new_window)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
            entries.append(entry)
        submit_button = ttk.Button(new_window, text="Perbarui Data", command=lambda: self.send_to_server(row_entry.get(), entries))
        submit_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        # response = self.c.recv(1024).decode()
        # messagebox.showerror("Perbarui data", response)
    def send_to_server(self, row_entry, entries):
        row = row_entry.get()
        data_parts = [entry.get() for entry in entries]
        data = f"ADD_DATA|{'|'.join(data_parts)}"

        self.c.send(row.encode())
        self.c.send(data.encode())
        response = self.c.recv(1024).decode()
        messagebox.showinfo("Information", response)

    def delete_data(self):
        self.c.sendall(b'delete_data')
        new_window = tk.Toplevel(self.root)
        new_window.title("Hapus Data")
        new_window.geometry("280x80")
        new_window.resizable(False, False)

        ttk.Label(new_window, text="Nomor Baris:").grid(row=0, column=0, padx=10, pady=5)
        entries = ttk.Entry(new_window)
        entries.grid(row=0, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Hapus Data", command=lambda: self.client_program(entries.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def send_server(self, entries):
        data_parts = [entry.get() for entry in entries]
        data = f"ADD_DATA|{'|'.join(data_parts)}"

        self.c.send(data.encode())
        response = self.c.recv(1024).decode()
        messagebox.showinfo("Information", response)
    
    def show_help(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pusat Bantuan")

        help_text = (
            "Pilihan 'Tampilkan Data' akan menampilkan seluruh data nasabah yang ada pada database.\n"
            "Pilihan 'Tambah Data' akan memberi akses kepada admin untuk menambah data nasabah pada database.\n"
            "Pilihan 'Perbarui Data' akan memberi akses kepada admin untuk memperbarui data nasabah yang sudah ada.\n"
            "Pilihan 'Hapus Data' akan memberi akses kepada admin untuk menghapus data nasabah pada database.\n"
            "Pilihan 'Cari Data' akan memberi akses kepada admin untuk mencari data nasabah sesuai nama, umur, dan pekerjaan.\n"
            "Pilihan 'Help' akan menampilkan pusat bantuan.\n"
            "Pilihan 'Keluar' akan keluar dari aplikasi."
        )

        help_frame = ttk.LabelFrame(new_window, text="Help", padding=(10, 10))
        help_frame.pack(padx=20, pady=20)
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT, font=("Helvetica", 10))
        help_label.grid(row=0, column=0, padx=10, pady=10)

    def exit_app(self):
        msg = messagebox.askquestion("Confirm", "Are you sure you want to exit?", icon='warning')
        if msg == "yes":
            self.root.deiconify()
            self.root.destroy()
            logging.info('Exiting window')
        else:
            logging.info('Window still running')

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BankClient(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
