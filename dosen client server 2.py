import socket
import tkinter as tk
from tkinter import ttk, messagebox

class BankClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank GUI Client")
        self.root.geometry("400x300")

        self.host = "10.200.18.137"
        self.port = 5005

        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.root, text="Enter data:").pack(pady=10)
        self.data_entry = ttk.Entry(self.root)
        self.data_entry.pack(pady=10)

        send_button = ttk.Button(self.root, text="Send Data", command=self.send_data)
        send_button.pack(pady=10)

    def send_data(self):
        # Get data from the entry
        data_to_send = self.data_entry.get()

        try:
            # Create a socket and connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))

                # Send data to the server
                client_socket.sendall(data_to_send.encode())

                # Receive and display the server's response
                response = client_socket.recv(1024).decode()
                messagebox.showinfo("Server Response", response)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankClientGUI(root)
    root.mainloop()
