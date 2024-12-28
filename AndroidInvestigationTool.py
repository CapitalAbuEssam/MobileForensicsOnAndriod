import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3


class ForensicTool:
    def _init_(self, root):
        self.root = root
        self.root.title("Ultimate Mobile Forensics Tool")
        self.root.geometry("900x700")

        # File path variable
        self.folder_path = tk.StringVar()

        # GUI Layout
        self.create_gui()

    def create_gui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Folder selection
        ttk.Label(frame, text="Select Dump Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        folder_entry = ttk.Entry(frame, textvariable=self.folder_path, width=60)
        folder_entry.grid(row=0, column=1, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, pady=5)

        # Artifact extraction button
        ttk.Button(frame, text="Extract Artifacts", command=self.extract_artifacts).grid(row=1, column=0, columnspan=3, pady=10)

        # Result area
        self.result_text = tk.Text(frame, wrap=tk.WORD, height=30, width=90)
        self.result_text.grid(row=2, column=0, columnspan=3, pady=10)

        # Scrollbar for the result area
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=2, column=3, sticky=tk.NS, pady=10)
        self.result_text["yscrollcommand"] = scrollbar.set

    def browse_folder(self):
        folder_name = filedialog.askdirectory(title="Select Dump Folder")
        if folder_name:
            self.folder_path.set(folder_name)

    def extract_artifacts(self):
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Invalid folder path. Please select a valid dump folder.")
            return

        try:
            self.result_text.insert(tk.END, f"Scanning folder: {folder_path}\n")

            # Traverse the folder dynamically
            for root, dirs, files in os.walk(folder_path):
                self.result_text.insert(tk.END, f"Scanning: {root}\n")

                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    self.process_file(file_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract artifacts: {str(e)}")

    def process_file(self, file_path):
        """Process each file and extract relevant artifacts."""
        try:
            if file_path.endswith(".db"):
                self.extract_all_db_info(file_path)
            else:
                self.result_text.insert(tk.END, f"Non-database file skipped: {file_path}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error processing {file_path}: {e}\n")

    def extract_all_db_info(self, file_path):
        """Extract and display all tables and data from a SQLite database."""
        self.result_text.insert(tk.END, f"Database: {file_path}\n")
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            # Fetch all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            if not tables:
                self.result_text.insert(tk.END, "No tables found in this database.\n")
            else:
                for table in tables:
                    table_name = table[0]
                    self.result_text.insert(tk.END, f"\nTable: {table_name}\n")

                    # Fetch all rows from the table
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    # Fetch column names
                    column_names = [description[0] for description in cursor.description]
                    self.result_text.insert(tk.END, f"Columns: {', '.join(column_names)}\n")

                    for row in rows:
                        self.result_text.insert(tk.END, f"{row}\n")

            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: Could not retrieve data from {file_path}: {e}\n")


if _name_ == "_main_":
    root = tk.Tk()
    app = ForensicTool(root)
    root.mainloop()
