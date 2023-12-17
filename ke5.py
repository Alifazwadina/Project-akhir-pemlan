import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pandastable import Table
import os
import pandas as pd

class BankMarketingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Marketing GUI")

        # Nama file CSV untuk menyimpan data
        self.filename = 'bank-additional-full.csv'

        # Buat file CSV jika tidak ada
        self.create_csv_file()

        # Fungsi untuk mengimpor data dari file CSV
        self.data = self.import_data_from_csv()

        # Membuat tombol-tombol untuk setiap fitur
        buttons = [
            ("Tampilkan Data", self.display_data),
            ("Tambah Data", self.add_data),
            ("Perbarui Data", self.update_data),
            ("Hapus Data", self.delete_data),
            ("Cari Data", self.search_data),
            ("Help", self.show_help),
            ("Keluar", self.exit_app)
        ]

        row = 0
        for text, command in buttons:
            ttk.Button(root, text=text, command=command).grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            row += 1

    def create_csv_file(self):
        if not os.path.exists(self.filename):
            # Membuat file CSV dengan header
            df = pd.DataFrame(columns=["Age", "Job", "Marital", "Education"])
            df.to_csv(self.filename, index=False)

    def import_data_from_csv(self):
        # Mengimpor data CSV ke DataFrame
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df
        return pd.DataFrame()

    def display_data(self):
        # Membuat jendela baru untuk menampilkan data
        new_window = tk.Toplevel(self.root)
        new_window.title("Tampilkan Data")

        # Menggunakan PandasTable untuk menampilkan data dengan lebih baik
        frame = ttk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)
        pt = Table(frame, dataframe=self.data, showtoolbar=True, showstatusbar=True)
        pt.show()

    def add_data(self):
        # Membuat jendela baru untuk menambah data
        new_window = tk.Toplevel(self.root)
        new_window.title("Tambah Data")

        labels = ["Usia (Age):", "Pekerjaan (Job):", "Status Pernikahan (Marital):", "Riwayat Pendidikan (Education):"]
        entries = []

        # Membuat label dan entry untuk setiap kolom
        for i, label in enumerate(labels):
            ttk.Label(new_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(new_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        submit_button = ttk.Button(new_window, text="Tambah Data", command=lambda: self.submit_data(entries))
        submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def submit_data(self, entries):
        # Mengambil nilai dari setiap entry
        data_values = [entry.get() for entry in entries]

        # Menambahkan data ke DataFrame
        new_data = pd.DataFrame([data_values], columns=self.data.columns)
        self.data = pd.concat([self.data, new_data], ignore_index=True)

        # Menyimpan DataFrame ke file CSV
        self.data.to_csv(self.filename, index=False)

        messagebox.showinfo("Info", "Data berhasil ditambahkan!")

    def update_data(self):
        # Membuat jendela baru untuk memperbarui data
        new_window = tk.Toplevel(self.root)
        new_window.title("Perbarui Data")

        # Membuat label dan entry untuk nomor baris yang akan diperbarui
        ttk.Label(new_window, text="Nomor Baris:").grid(row=0, column=0, padx=10, pady=5)
        row_entry = ttk.Entry(new_window)
        row_entry.grid(row=0, column=1, padx=10, pady=5)

        labels = ["Usia Baru (Age):", "Pekerjaan Baru (Job):", "Status Pernikahan Baru (Marital):", "Riwayat Pendidikan Baru (Education):"]
        entries = []

        # Membuat label dan entry untuk setiap kolom baru
        for i, label in enumerate(labels):
            ttk.Label(new_window, text=label).grid(row=i+1, column=0, padx=10, pady=5)
            entry = ttk.Entry(new_window)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
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

        # Membuat label dan entry untuk usia yang akan dicari
        ttk.Label(new_window, text="Usia (Age):").grid(row=0, column=0, padx=10, pady=5)
        age_entry = ttk.Entry(new_window)
        age_entry.grid(row=0, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Cari Data", command=lambda: self.submit_search(age_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def submit_search(self, age):
        # Membuat jendela baru untuk menampilkan hasil pencarian
        new_window = tk.Toplevel(self.root)
        new_window.title("Hasil Pencarian")

        text = tk.Text(new_window)
        text.insert(tk.END, f"Data dengan usia {age} adalah:\n\n")
        count = 0
        for index, row in self.data.iterrows():
            if str(age) == str(row['Age']):
                count += 1
                text.insert(tk.END, f"Data ke-{count}\n")
                for col, value in row.iteritems():
                    text.insert(tk.END, f"{col}: {value}\n")
                text.insert(tk.END, "\n")
        if count == 0:
            text.insert(tk.END, "Data tidak ditemukan.")
        text.insert(tk.END, f"Jumlah data: {count}\n")
        text.config(state=tk.DISABLED)
        text.pack()

    def show_help(self):
        # Membuat jendela baru untuk menampilkan pusat bantuan
        new_window = tk.Toplevel(self.root)
        new_window.title("Pusat Bantuan")

        help_text = (
            "Pilihan 'Tampilkan Data' akan menampilkan seluruh data yang ada pada file.\n"
            "Pilihan 'Tambah Data' akan memberi akses kepada user untuk menambah data pada file.\n"
            "Pilihan 'Perbarui Data' akan memberi akses kepada user untuk memperbarui data yang sudah ada.\n"
            "Pilihan 'Hapus Data' akan memberi akses kepada user untuk menghapus data pada file.\n"
            "Pilihan 'Cari Data' akan memberi akses kepada user untuk mencari data sesuai umur.\n"
            "Pilihan 'Help' akan menampilkan pusat bantuan.\n"
            "Pilihan 'Keluar' akan keluar dari aplikasi."
        )

        text = tk.Text(new_window)
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)
        text.pack()

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankMarketingGUI(root)
    root.mainloop()
