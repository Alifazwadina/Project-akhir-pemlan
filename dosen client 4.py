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
        new_data_window = tk.Toplevel(self.root)
        new_data_window.title("Add Data")

        # Create GUI elements to get new data
        # Example: Use Entry widgets to get values for each column
        ttk.Label(new_data_window, text="Nama:").grid(row=0, column=0, padx=10, pady=5)
        nama_entry = ttk.Entry(new_data_window)
        nama_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add more Entry widgets for other columns

        ttk.Button(new_data_window, text="Submit", command=lambda: self.submit_add_data(nama_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def submit_add_data(self, nama):
        # Create a DataFrame with the new data
        new_data = pd.DataFrame([[nama]], columns=["Nama"])  # Add more columns and data as needed

        # Send the data to the server
        self.send_data_to_server("add_data")
        self.send_data_to_server(new_data.to_json(orient='split'))

        # Optionally, you can receive and display the updated data
        updated_data = self.receive_data_from_server()
        self.show_data_table(updated_data)

    def update_data(self):
        update_data_window = tk.Toplevel(self.root)
        update_data_window.title("Update Data")

        ttk.Label(update_data_window, text="Row Index:").grid(row=0, column=0, padx=10, pady=5)
        row_index_entry = ttk.Entry(update_data_window)
        row_index_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(update_data_window, text="New Value:").grid(row=1, column=0, padx=10, pady=5)
        new_value_entry = ttk.Entry(update_data_window)
        new_value_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(update_data_window, text="Submit", command=lambda: self.submit_update_data(row_index_entry.get(), new_value_entry.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def submit_update_data(self, row_index, new_value):
        try:
            row_index = int(row_index)
            # Create a DataFrame with the updated data
            updated_data = pd.DataFrame([[new_value]], columns=["Nama"])  # Adjust columns as needed

            # Send the update request to the server
            self.send_data_to_server(f"update_data:{row_index}")
            self.send_data_to_server(updated_data.to_json(orient='split'))

            # Optionally, you can receive and display the updated data
            updated_data = self.receive_data_from_server()
            self.show_data_table(updated_data)
        except ValueError:
            messagebox.showerror("Error", "Invalid row index. Please enter a valid number.")

    def delete_data(self):
        delete_data_window = tk.Toplevel(self.root)
        delete_data_window.title("Delete Data")

        ttk.Label(delete_data_window, text="Row Index:").grid(row=0, column=0, padx=10, pady=5)
        row_index_entry = ttk.Entry(delete_data_window)
        row_index_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(delete_data_window, text="Submit", command=lambda: self.submit_delete_data(row_index_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def submit_delete_data(self, row_index):
        try:
            row_index = int(row_index)

            # Send the delete request to the server
            self.send_data_to_server(f"delete_data:{row_index}")

            # Optionally, you can receive and display the updated data
            updated_data = self.receive_data_from_server()
            self.show_data_table(updated_data)
        except ValueError:
            messagebox.showerror("Error", "Invalid row index. Please enter a valid number.")

    def search_data(self):
        search_data_window = tk.Toplevel(self.root)
        search_data_window.title("Search Data")

        ttk.Label(search_data_window, text="Search Term:").grid(row=0, column=0, padx=10, pady=5)
        search_term_entry = ttk.Entry(search_data_window)
        search_term_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(search_data_window, text="Submit", command=lambda: self.submit_search_data(search_term_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def submit_search_data(self, search_term):
        # Send the search request to the server
        self.send_data_to_server(f"search_data:{search_term}")

        # Receive and display the search results
        search_results = self.receive_data_from_server()
        self.show_data_table(search_results)

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
