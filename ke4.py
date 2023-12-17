import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

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
            with open(self.filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Age", "Job", "Marital", "Education"])

    def import_data_from_csv(self):
        data = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                data = [row for row in reader]
        return data

    def display_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Tampilkan Data")

        text = tk.Text(new_window)
        text.insert(tk.END, "Data Bank Marketing:\n\n")
        for entry in self.data:
            for key, value in entry.items():
                text.insert(tk.END, f"{key}: {value}\n")
            text.insert(tk.END, "\n")
        text.config(state=tk.DISABLED)
        text.pack()

    def add_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Tambah Data")

        age_label = ttk.Label(new_window, text="Usia (Age):")
        age_label.grid(row=0, column=0, padx=10, pady=5)
        age_entry = ttk.Entry(new_window)
        age_entry.grid(row=0, column=1, padx=10, pady=5)

        job_label = ttk.Label(new_window, text="Pekerjaan (Job):")
        job_label.grid(row=1, column=0, padx=10, pady=5)
        job_entry = ttk.Entry(new_window)
        job_entry.grid(row=1, column=1, padx=10, pady=5)

        marital_label = ttk.Label(new_window, text="Status Pernikahan (Marital):")
        marital_label.grid(row=2, column=0, padx=10, pady=5)
        marital_entry = ttk.Entry(new_window)
        marital_entry.grid(row=2, column=1, padx=10, pady=5)

        education_label = ttk.Label(new_window, text="Riwayat Pendidikan (Education):")
        education_label.grid(row=3, column=0, padx=10, pady=5)
        education_entry = ttk.Entry(new_window)
        education_entry.grid(row=3, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Tambah Data", command=lambda: self.submit_data(
            age_entry.get(), job_entry.get(), marital_entry.get(), education_entry.get()))
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_data(self, age, job, marital, education):
        with open(self.filename, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([age, job, marital, education])
        messagebox.showinfo("Info", "Data berhasil ditambahkan!")

    def update_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Perbarui Data")

        row_label = ttk.Label(new_window, text="Nomor Baris:")
        row_label.grid(row=0, column=0, padx=10, pady=5)
        row_entry = ttk.Entry(new_window)
        row_entry.grid(row=0, column=1, padx=10, pady=5)

        age_label = ttk.Label(new_window, text="Usia Baru (Age):")
        age_label.grid(row=1, column=0, padx=10, pady=5)
        age_entry = ttk.Entry(new_window)
        age_entry.grid(row=1, column=1, padx=10, pady=5)

        job_label = ttk.Label(new_window, text="Pekerjaan Baru (Job):")
        job_label.grid(row=2, column=0, padx=10, pady=5)
        job_entry = ttk.Entry(new_window)
        job_entry.grid(row=2, column=1, padx=10, pady=5)

        marital_label = ttk.Label(new_window, text="Status Pernikahan Baru (Marital):")
        marital_label.grid(row=3, column=0, padx=10, pady=5)
        marital_entry = ttk.Entry(new_window)
        marital_entry.grid(row=3, column=1, padx=10, pady=5)

        education_label = ttk.Label(new_window, text="Riwayat Pendidikan Baru (Education):")
        education_label.grid(row=4, column=0, padx=10, pady=5)
        education_entry = ttk.Entry(new_window)
        education_entry.grid(row=4, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Perbarui Data", command=lambda: self.submit_update(
            row_entry.get(), age_entry.get(), job_entry.get(), marital_entry.get(), education_entry.get()))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_update(self, row, age, job, marital, education):
        try:
            row_index = int(row)
            if 0 < row_index < len(self.data) + 1:
                self.data[row_index - 1] = {'Age': age, 'Job': job, 'Marital': marital, 'Education': education}
                with open(self.filename, mode='w', newline='') as file:
                    csv_writer = csv.DictWriter(file, fieldnames=["Age", "Job", "Marital", "Education"])
                    csv_writer.writeheader()
                    csv_writer.writerows(self.data)
                messagebox.showinfo("Info", f"Data dengan nomor {row_index} berhasil diperbarui!")
            else:
                messagebox.showerror("Error", "Nomor baris tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nomor yang valid.")

    def delete_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Hapus Data")

        row_label = ttk.Label(new_window, text="Nomor Baris:")
        row_label.grid(row=0, column=0, padx=10, pady=5)
        row_entry = ttk.Entry(new_window)
        row_entry.grid(row=0, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Hapus Data", command=lambda: self.submit_delete(row_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def submit_delete(self, row):
        try:
            row_index = int(row)
            if 0 < row_index < len(self.data) + 1:
                del self.data[row_index - 1]
                with open(self.filename, mode='w', newline='') as file:
                    csv_writer = csv.DictWriter(file, fieldnames=["Age", "Job", "Marital", "Education"])
                    csv_writer.writeheader()
                    csv_writer.writerows(self.data)
                messagebox.showinfo("Info", f"Data dengan nomor {row_index} berhasil dihapus!")
            else:
                messagebox.showerror("Error", "Nomor baris tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nomor yang valid.")

    def search_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Cari Data")

        age_label = ttk.Label(new_window, text="Usia (Age):")
        age_label.grid(row=0, column=0, padx=10, pady=5)
        age_entry = ttk.Entry(new_window)
        age_entry.grid(row=0, column=1, padx=10, pady=5)

        submit_button = ttk.Button(new_window, text="Cari Data", command=lambda: self.submit_search(age_entry.get()))
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def submit_search(self, age):
        new_window = tk.Toplevel(self.root)
        new_window.title("Hasil Pencarian")

        text = tk.Text(new_window)
        text.insert(tk.END, f"Data dengan usia {age} adalah:\n\n")
        count = 0
        for row in self.data:
            if age == row['Age']:
                count += 1
                text.insert(tk.END, f"Data ke-{count}\n")
                for key, value in row.items():
                    text.insert(tk.END, f"{key}: {value}\n")
                text.insert(tk.END, "\n")
        if count == 0:
            text.insert(tk.END, "Data tidak ditemukan.")
        text.insert(tk.END, f"Jumlah data: {count}\n")
        text.config(state=tk.DISABLED)
        text.pack()

    def show_help(self):
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
