# server code (unfinished)
# kalo mau lgsg edit disini aja pencet gambar pensil di kanan atas

import socket
import threading
import pandas as pd

class BankServer:
    def __init__(self):
        self.data = pd.DataFrame(columns=["Nama", "Umur", "Pekerjaan", "No_Telp", "Status", "Alamat"])
        self.address = (socket.gethostname(), 5000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.address)
        self.s.listen(5)
        self.export_lock = threading.Lock()
        self.import_lock = threading.Lock()

        self.filename = 'new-bank.csv'

    def run_server(self):
        print("Server is running.")
        while True:
            c_socket, c_address = self.s.accept()
            threading.Thread(target=self.handle_client, args=(c_socket,)).start()

    def handle_client(self, c_socket):
        with c_socket:
            print(f"Conection from {str(self.c_address)}")

        data = c_socket.recv(1024).decode()

        if data == 'add_data':
            self.add_data(c_socket)
        elif data == 'update_data':
            self.update_data(c_socket)
        elif data == 'delete_data':
            self.delete_data(c_socket)

    def add_data(self, c_socket):
        data = c_socket.recv(1024).decode()
        value = [data.split(',')]

        new_data = pd.DataFrame([value], columns = self.data.columns)
        self.data = pd.concat([self.data, new_data], ignore_index=True)

        data = c_socket.sendall(b'Data berhasil ditambahkan.')

    def update_data(self, c_socket):
        data = c_socket.recv(1024).decode()
        try:
            row_index = int(row) # masih perlu dibenerin ini error disini
            if 0 < row_index < len(self.data) +1:
                value = [data.split(',')]
                for i, col in enumerate(self.data.columns):
                    self.data.at[row_index - 1, col] = value
                self.data.to_csv(self.filename, index=False)
                data = c_socket.sendall(b'Data berhasil diperbarui.')
            else:
                data = c_socket.sendall(b'Nomor baris tidak valid.')
        except ValueError:
            data = c_socket.sendall(b'Masukkan nomor yang valid.')

    def delete_data(self, c_socket):
        data = c_socket.recv(1024).decode()
        try:
            row = int(data)
            if 0 < row < len(self.data) +1:
                self.data = self.data.drop(index=row-1).reset_index(drop=True)
                self.data.to_csv(self.filename, index=False)
                data = c_socket.sendall(b'Data telah dihapus')
            else:
                data = c_socket.sendall(b'Nomor baris tidak valid.')
        except ValueError:
            data = c_socket.sendall(b'Masukkan nomor yang valid.')

if __name__ == "__main__":
    server = BankServer()
    server.run_server()
