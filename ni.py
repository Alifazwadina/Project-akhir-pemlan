import csv
import os
import threading
import tkinter as tk
from tkinter import messagebox

filename = 'bank-additional.csv'

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Marketing App")

        self.data = self.import_data_from_csv()

        self.choice_var = tk.StringVar()

        self.create_gui_elements()

        # Lock for thread-safe data access
        self.data_lock = threading.Lock()

    def create_gui_elements(self):
        tk.Label(self.root, text="Menu:").pack()

        operations = [
            "Tampilkan Data",
            "Tambah Data",
            "Perbarui Data",
            "Hapus Data",
            "Cari Data",
            "Help",
            "Keluar"
        ]

        for i, operation in enumerate(operations, start=1):
            tk.Radiobutton(
                self.root,
                text=operation,
                variable=self.choice_var,
                value=str(i)
            ).pack(anchor=tk.W)

        tk.Button(self.root, text="Submit", command=self.handle_choice).pack()

    def handle_choice(self):
        choice = self.choice_var.get()

        if choice == '1':
            threading.Thread(target=self.display_data).start()
        elif choice == '2':
            threading.Thread(target=self.add_data).start()
        elif choice == '3':
            threading.Thread(target=self.update_data).start()
        elif choice == '4':
            threading.Thread(target=self.delete_data).start()
        elif choice == '5':
            threading.Thread(target=self.search).start()
        elif choice == '6':
            self.help()
        elif choice == '7':
            print("Terima kasih telah menggunakan Sistem Database Marketing Bank ABC.")
            self.root.destroy()
        else:
            print("Pilihan tidak valid. Silakan pilih operasi yang valid.")

    def import_data_from_csv(self):
        data = []
        if os.path.exists(filename):
            with open(filename, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                data = [row for row in reader]
            print("Data berhasil diimpor dari", filename)
        else:
            print(filename, "tidak ditemukan.")
        return data

    def display_data(self):
        with self.data_lock:
            print("Data Bank Marketing:")
            for entry in self.data:
                for key, value in entry.items():
                    print(f"{key}: {value}")
                print("")

    def add_data(self):
        age = input("Masukkan usia (age): ")
        job = input("Masukkan pekerjaan (job): ")
        marital = input("Masukkan status pernikahan (marital): ")
        education = input("Masukkan riwayat pendidikan (education): ")
        new_data = {'age': age, 'job': job, 'marital': marital, 'education': education}

        with self.data_lock:
            self.data.append(new_data)

            with open(filename, mode='a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(new_data.values())
            print("Data berhasil ditambahkan!\n")

    def update_data(self):
        try:
            row_index = int(input("Masukkan nomor baris yang akan diperbarui: "))
            if 0 < row_index < len(self.data):
                age = input("Masukkan usia baru (age): ")
                job = input("Masukkan pekerjaan baru (job): ")
                marital = input("Masukkan status pernikahan baru (marital): ")
                education = input("Masukkan riwayat pendidikan baru (education): ")

                new_data = {'age': age, 'job': job, 'marital': marital, 'education': education}
                
                with self.data_lock:
                    self.data[row_index] = new_data

                    with open(filename, mode='w', newline='') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerows([entry.values() for entry in self.data])
                    print(f"Data dengan nomor {row_index} berhasil diperbarui.\n")
            else:
                print("Masukkan nomor yang valid.")
        except ValueError:
            print("Masukkan nomor yang valid.")

    def delete_data(self):
        try:
            index = int(input("Pilih nomor data yang ingin dihapus: "))
            if 0 < index < len(self.data):
                with self.data_lock:
                    del self.data[index]

                    with open(filename, mode='w', newline='') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerows([entry.values() for entry in self.data])
                    print(f"Data dengan nomor {index} berhasil dihapus.\n")
            else:
                print("Masukkan nomor yang valid.")
        except ValueError:
            print("Masukkan nomor yang valid.")

    def search(self):
        age = input("Masukkan usia: ")
        with self.data_lock:
            print(f"\nData dengan usia {age} adalah:")
            count = 0
            for row in self.data:
                if age == row['age']:
                    count += 1
                    print(f"Data ke-{count}")
                    for key, value in row.items():
                        print(f"{key}: {value}")
                    print("")
            if count == 0:
                print("Data tidak ditemukan.")
            print("Jumlah data:", count, "\n")

    def help(self):
        print("\nPusat Bantuan")
        print(
            "Pilihan 'Tampilkan data' akan menampilkan seluruh data yang ada pada file."
            "\nPilihan 'Tambah data' akan memberi akses kepada user untuk menambah data pada file."
            "\nPilihan 'Perbarui data' akan memberi akses kepada user untuk memperbarui data yang sudah ada."
            "\nPilihan 'Hapus data' akan memberi akses kepada user untuk menghapus data pada file."
            "\nPilihan 'Cari data' akan memberi akses kepada user untuk mencari data sesuai umur. \n"
        )


def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
