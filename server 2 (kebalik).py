import tkinter as tk
import logging
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from pandastable import Table
import os
import pandas as pd
import socket
import threading

class BankMarketingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Data Nasabah Bank ABC")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        pastel_blue = "#add8e6"
        self.root.configure(bg=pastel_blue)
    
        # Nama file CSV untuk menyimpan data
        self.filename = 'new-bank.csv'

        # Buat file CSV jika tidak ada
        self.create_csv_file()

        # Fungsi untuk mengimpor data dari file CSV
        self.data = self.import_data_from_csv()

        # Inisialisasi login
        self.login_frame()

    def create_csv_file(self):
        if not os.path.exists(self.filename):
            # Membuat file CSV dengan header
            df = pd.DataFrame(columns=["Nama", "Umur", "Pekerjaan", "No_Telp", "Status", "Alamat"])
            df.to_csv(self.filename, index=False)

    def import_data_from_csv(self):
        # Mengimpor data CSV ke DataFrame
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df
        return pd.DataFrame()

    def login_frame(self):
        # Membuat frame untuk login
        login_frame = ttk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Label untuk judul (Welcome!)
        title_label = ttk.Label(login_frame, text="Welcome!", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))
        
        # Label dan entry untuk username
        ttk.Label(login_frame, text="Username:", font=("Helvetica", 10)).grid(row=1, column=0, padx=10, pady=5)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=1, column=1, padx=15, pady=10)

        # Label dan entry untuk password
        ttk.Label(login_frame, text="Password:", font=("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=15, pady=10)

        # Tombol login
        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        # Memeriksa login (contoh sederhana)
        if self.username_entry.get() == "admin" and self.password_entry.get() == "2222":
            # Menampilkan frame utama setelah login sukses
            self.show_main_frame()
        else:
            messagebox.showerror("Login Failed", "Username or password is incorrect.")

    def show_main_frame(self):
        # Hapus frame login
        for widget in self.root.winfo_children():
            widget.destroy()

        # Membuat frame baru
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Membuat tombol-tombol untuk setiap fitur pada frame utama
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

        # Membuat frame agar berada di tengah
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def display_data(self):
        # Membuat jendela baru untuk menampilkan data
        new_window = tk.Toplevel(self.root)
        new_window.title("Tampilkan Data")

        # Menggunakan PandasTable untuk menampilkan data dengan lebih baik
        frame = ttk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)
        pt = Table(frame, dataframe=self.data, showtoolbar=False, showstatusbar=True, editable=False)
        pt.show()

    def add_data(self):
        # Membuat jendela baru untuk menambah data
        new_window = tk.Toplevel(self.root)
        new_window.title("Tambah Data")
        new_window.geometry("250x250")
        new_window.resizable(False, False)

        # Label dan entry untuk setiap kolom
        columns = ["Nama", "Umur", "Pekerjaan", "No.Telepon", "Status", "Alamat"]
        entries = []
        for i, column in enumerate(columns):
            ttk.Label(new_window, text=column, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(new_window)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries.append(entry)

        # Tombol untuk menambah data
        ttk.Button(new_window, text="Tambah Data", command=lambda: self.add_data_to_dataframe(entries)).grid(row=len(columns), column=0, columnspan=2, pady=10)

    def add_data_to_dataframe(self, entries):
        # Mendapatkan nilai dari entry
        values = [entry.get() for entry in entries]

        # Menambahkan data baru ke DataFrame
        new_data = pd.DataFrame([values], columns=self.data.columns)
        self.data = pd.concat([self.data, new_data], ignore_index=True)

        # Menyimpan DataFrame ke file CSV
        self.data.to_csv(self.filename, index=False)
        messagebox.showinfo("Tambah Data", "Data berhasil ditambahkan.")
        
    def update_data(self):
        # Membuat jendela baru untuk memperbarui data
        new_window = tk.Toplevel(self.root)
        new_window.title("Perbarui Data")
        new_window.geometry("300x280")
        new_window.resizable(False, False)

        # Membuat label dan entry untuk nomor baris yang akan diperbarui
        ttk.Label(new_window, text="Nomor Baris:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        row_entry = ttk.Entry(new_window)
        row_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        labels = ["Mengganti Nama:","Umur Baru:", "Mengganti Pekerjaan:", "Mengganti No.Telepon:", "Mengganti Status:","Mengubah Alamat:"]
        entries = []

        # Membuat label dan entry untuk setiap kolom baru
        for i, label in enumerate(labels):
            ttk.Label(new_window, text=label, anchor="w").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(new_window)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
            entries.append(entry)

        submit_button = ttk.Button(new_window, text="Perbarui Data", command=lambda: self.submit_update(row_entry.get(), entries))
        submit_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    def submit_update(self, row, entries):
        try:
            row_index = int(row)
            if 0 < row_index < len(self.data) + 1:
                # Mengambil nilai dari setiap entry baru
                new_values = [entry.get() for entry in entries]
                # Memperbarui data pada DataFrame
                for i, col in enumerate(self.data.columns):
                    self.data.at[row_index - 1, col] = new_values[i]
                # Menyimpan DataFrame ke file CSV
                self.data.to_csv(self.filename, index=False)
                messagebox.showinfo("Info", f"Data dengan nomor {row_index} berhasil diperbarui!")
            else:
                messagebox.showerror("Error", "Nomor baris tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nomor yang valid.")

    def delete_data(self):
        # Membuat jendela baru untuk menghapus data
        new_window = tk.Toplevel(self.root)
        new_window.title("Hapus Data")
        new_window.geometry("280x80")
        new_window.resizable(False, False)

        # Membuat label dan entry untuk nomor baris yang akan dihapus
        ttk.Label(new_window, text="Nomor Baris:").grid(row=0, column=0, padx=10, pady=5)
        row_entry = ttk.Entry(new_window)
        row_entry.grid(row=0, column=1, padx=10, pady=5)
        submit_button = ttk.Button(new_window, text="Hapus Data", command=lambda: self.submit_delete(row_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def submit_delete(self, row):
        try:
            row_index = int(row)
            if 0 < row_index < len(self.data) + 1:
                # Menghapus data dari DataFrame
                self.data = self.data.drop(index=row_index - 1).reset_index(drop=True)
                # Menyimpan DataFrame ke file CSV
                self.data.to_csv(self.filename, index=False)
                messagebox.showinfo("Info", f"Data dengan nomor {row_index} berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Nomor baris tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nomor yang valid.")

    def search_data(self):
        # Membuat jendela baru untuk mencari data
        new_window = tk.Toplevel(self.root)
        new_window.title("Cari Data")
        new_window.geometry("250x150")
        new_window.resizable(False, False)

        buttons = [
            ("Nama", self.search_name),
            ("Umur", self.search_age),
            ("Pekerjaan", self.search_job),
        ]

        frame = ttk.Frame(new_window)
        frame.pack(expand=True, fill="both", pady=10)
        for text, command in buttons:
            ttk.Button(frame, text=text, command=command).pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

    def search_age(self):
        # Membuat jendela baru untuk mencari data
        new_window = tk.Toplevel(self.root)
        new_window.title("Cari Data (Umur)")
        new_window.geometry("250x100")
        new_window.resizable(False, False)

        # Membuat label dan entry untuk usia yang akan dicari
        ttk.Label(new_window, text="Usia:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        age_entry = ttk.Entry(new_window)
        age_entry.grid(row=0, column=1, padx=10, pady=5)
        submit_button = ttk.Button(new_window, text="Cari Data", command=lambda: self.submit_search(age = age_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    def search_name(self):
        # Membuat jendela baru untuk mencari data
        new_window = tk.Toplevel(self.root)
        new_window.title("Cari Data (Nama)")
        new_window.geometry("250x100")
        new_window.resizable(False, False)

        # Membuat label dan entry untuk usia yang akan dicari
        ttk.Label(new_window, text="Nama:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = ttk.Entry(new_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        submit_button = ttk.Button(new_window, text="Cari Data", command=lambda: self.submit_search(name = name_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def search_job(self):
        # Membuat jendela baru untuk mencari data
        new_window = tk.Toplevel(self.root)
        new_window.title("Cari Data (Pekerjaan)")
        new_window.geometry("250x100")
        new_window.resizable(False, False)

        # Membuat label dan entry untuk usia yang akan dicari
        ttk.Label(new_window, text="Pekerjaan:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        job_entry = ttk.Entry(new_window)
        job_entry.grid(row=0, column=1, padx=10, pady=5)
        submit_button = ttk.Button(new_window, text="Cari Data", command=lambda: self.submit_search(job = job_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    def submit_search(self=None, name=None, age=None, job=None):
        eror = 0
        if not age and not name and not job:
            filtered_data = self.data
        elif age is not None:
            try:
                filtered_data = self.data[self.data['umur'] == int(age)]
            except ValueError:
                eror = 1
                messagebox.showerror("Error", "Masukan harus angka")
            print(age)
        elif name is not None:
            filtered_data = self.data[self.data['nama'] == name]
            print(age)
        elif job is not None:
            filtered_data = self.data[self.data['pekerjaan'] == job]
            print(job)
        if eror == 0:
            print(eror == True)
            if filtered_data.empty:
                messagebox.showerror("Error", "Data tidak ditemukan")
            else:
                # Membuat jendela baru untuk menampilkan hasil pencarian
                new_window = tk.Toplevel(self.root)
                new_window.title("Hasil Pencarian")
                
                # Create a frame
                frame = tk.Frame(new_window)
                frame.pack(fill='both', expand=True)
                
                # Create a PandasTable widget
                table = Table(frame, dataframe=filtered_data, showtoolbar=True, showstatusbar=True, editable=False)
                table.show()

    def show_help(self):
        # Membuat jendela baru untuk menampilkan pusat bantuan
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
        # Membuat widget LabelFrame untuk menampilkan teks bantuan dengan lebih baik
        help_frame = ttk.LabelFrame(new_window, text="Help", padding=(10, 10))
        help_frame.pack(padx=20, pady=20)

        # Membuat widget Label untuk menampilkan teks bantuan
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT, font=("Helvetica", 10))
        help_label.grid(row=0, column=0, padx=10, pady=10)

    def exit_app(self):
        msg = messagebox.askquestion("Confirm", "ARE YOU SURE YOU WANT TO EXIT?", icon='warning')
        if msg == "yes":
            self.root.deiconify()  # makes the root window visible again
            self.root.destroy()
            logging.info('Exiting window')
        else:
            logging.info('Window still running')

"""if __name__ == "__main__":
    root = tk.Tk()
    app = BankMarketingGUI(root)
    root.mainloop()"""

class MultiThreadedServer:
    def __init__(self, host, port, bank_gui):
        self.host = host
        self.port = port
        self.bank_gui = bank_gui
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def start_server(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        print("Connection established.")
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                response = self.process_request(data)
                client_socket.send(response.encode())
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()
        print("Connection closed.")

    def process_request(self, request):
    
    # Process the client's request here
    # You may want to call the relevant methods in BankMarketingGUI class
    # and return the response accordingly.

        if request == "DISPLAY_DATA":
            # Example: Display data and send the result back to the client
            response = str(self.bank_gui.data)
        elif request == "ADD_DATA":
            # Example: Add data and send a success message back to the client
            self.bank_gui.add_data_to_dataframe(["John", "25", "Engineer", "123456789", "Single", "123 Main St"])
            response = "Data added successfully"
        else:
            response = "Unknown command"

        return response


if __name__ == '__main__':
    root = tk.Tk()
    app = BankMarketingGUI(root)
    server = MultiThreadedServer("10.200.18.137", 5000, app)
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()
    root.mainloop()
