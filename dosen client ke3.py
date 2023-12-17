import socket
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from pandastable import Table

class BankClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Data Nasabah Bank ABC")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        pastel_blue = "#add8e6"
        self.root.configure(bg=pastel_blue)

        self.host = "10.200.18.137"
        self.port = 5005

        self.create_connection()

        self.setup_gui()

    def create_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_data_to_server(self, data):
        self.client_socket.send(data.encode())

    def receive_data_from_server(self):
        data = self.client_socket.recv(1024).decode()
        return pd.read_json(data, orient='split')
        
    def setup_gui(self):
        ttk.Button(self.root, text="Display Data", command=self.display_data).pack(pady=10)
        ttk.Button(self.root, text="Add Data", command=self.add_data).pack(pady=10)
        ttk.Button(self.root, text="Update Data", command=self.update_data).pack(pady=10)
        ttk.Button(self.root, text="Delete Data", command=self.delete_data).pack(pady=10)
        ttk.Button(self.root, text="Search Data", command=self.search_data).pack(pady=10)
        ttk.Button(self.root, text="Exit App", command=self.exit_app).pack(pady=10)

    def display_data(self):
        self.send_data_to_server("display_data")
        data = self.receive_data_from_server()
        self.show_data_table(data)

    def add_data(self):
        self.send_data_to_server("add_data")
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
        ttk.Button(new_window, text="Tambah Data", command=lambda: self.send_data_to_server(entries)).grid(row=len(columns), column=0, columnspan=2, pady=10)
        
    def update_data(self):
        self.send_data_to_server("update_data")
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
        submit_button = ttk.Button(new_window, text="Perbarui Data", command=lambda: self.send_data_to_server((row_entry.get(), entries)))
        submit_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    def delete_data(self):
        self.send_data_to_server("delete_data")
        new_window = tk.Toplevel(self.root)
        new_window.title("Hapus Data")
        new_window.geometry("280x80")
        new_window.resizable(False, False)

        ttk.Label(new_window, text="Nomor Baris:").grid(row=0, column=0, padx=10, pady=5)
        entries = ttk.Entry(new_window)
        entries.grid(row=0, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Hapus Data", command=lambda: self.send_data_to_server(entries.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def search_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Cari Data")
        new_window.geometry("250x150")
        new_window.resizable(False, False)

        buttons = [
            ("Nama", self.search_about("Name")),
            ("Umur", self.search_about("Age")),
            ("Pekerjaan", self.search_about("Job")),
        ]

        frame = ttk.Frame(new_window)
        frame.pack(expand=True, fill="both", pady=10)

        for text, command in buttons:
            ttk.Button(frame, text=text, command=command).pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

    def search_about(self, type):
        self.send_data_to_server("search_data")
        new_window = tk.Toplevel(self.root)
        new_window.title(f"Cari Data ({type})")
        new_window.geometry("250x100")
        new_window.resizable(False, False)
        
        ttk.Label(new_window, text=f"{type}:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_var = tk.StringVar()
        search_entry = ttk.Entry(new_window, textvariable=entry_var)
        search_entry.grid(row=0, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Cari Data", command=lambda: self.send_data_to_server((type, entry_var.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def exit_app(self):
        self.send_data_to_server("exit_app")
        self.root.destroy()

    def show_data_table(self, data):
        new_window = tk.Toplevel(self.root)
        new_window.title("Data Nasabah")

        frame = ttk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)
        pt = Table(frame, dataframe=data, showtoolbar=False, showstatusbar=True, editable=False)
        pt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankClientGUI(root)
    root.mainloop()
