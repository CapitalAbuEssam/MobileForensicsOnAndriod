import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from pytsk3 import Img_Info, FS_Info

class ForensicTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Mobile Forensics Tool")
        self.root.geometry("900x700")

        # File path variable
        self.file_path = tk.StringVar()

        # GUI Layout
        self.create_gui()

    def create_gui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # File selection
        ttk.Label(frame, text="Select Dump Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        file_entry = ttk.Entry(frame, textvariable=self.file_path, width=60)
        file_entry.grid(row=0, column=1, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_file).grid(row=0, column=2, pady=5)

        # Artifact extraction button
        ttk.Button(frame, text="Extract Artifacts", command=self.extract_artifacts).grid(row=1, column=0, columnspan=3, pady=10)

        # Result area
        self.result_text = tk.Text(frame, wrap=tk.WORD, height=30, width=90)
        self.result_text.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Scrollbar for the result area
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=2, column=3, sticky=tk.NS, pady=10)
        self.result_text["yscrollcommand"] = scrollbar.set

    def browse_file(self):
        folder_name = filedialog.askdirectory(title="Select Dump Image Folder")
        if folder_name:
            self.file_path.set(folder_name)

    def scan_file_system(self, fs, root_path="/"):
        """Recursively scan the file system and collect file paths."""
        paths = []
        try:
            directory = fs.open_dir(root_path)
            for entry in directory:
                name = entry.info.name.name.decode("utf-8")
                if name in [".", ".."]:
                    continue
                full_path = os.path.join(root_path, name)
                if entry.info.meta and entry.info.meta.type == 2:  # Directory
                    paths.extend(self.scan_file_system(fs, full_path))
                else:
                    paths.append(full_path)
        except Exception as e:
            print(f"Error scanning {root_path}: {e}")
        return paths

    def locate_artifacts(self, fs):
        """Search for known artifact files dynamically."""
        artifact_paths = {
            "call_logs": None,
            "sms": None,
            "contacts": None,
            "photos": [],
            "google_services": None,
        }
        all_paths = self.scan_file_system(fs)
        for path in all_paths:
            if "calllog.db" in path:
                artifact_paths["call_logs"] = path
            elif "mmssms.db" in path:
                artifact_paths["sms"] = path
            elif "contacts.db" in path:
                artifact_paths["contacts"] = path
            elif "google_services.db" in path:
                artifact_paths["google_services"] = path
            elif "/DCIM/" in path or path.lower().endswith((".jpg", ".png", ".mp4")):
                artifact_paths["photos"].append(path)
        return artifact_paths

    def extract_artifacts(self):
        image_path = self.file_path.get()
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("Error", "Invalid file path. Please select a valid dump image.")
            return

        try:
            if os.path.isdir(image_path):
                self.result_text.insert(tk.END, f"Loading image folder: {image_path}\n")
                img = Img_Info(image_path)  # This handles the directory
                fs = FS_Info(img)
            
                for root, dirs, files in os.walk(image_path):
                    for file_name in files:
                        full_path = os.path.join(root, file_name)
                        artifacts = self.locate_artifacts(fs)
                        if artifacts["call_logs"]:
                            self.extract_call_logs(fs, artifacts["call_logs"])
                        if artifacts["sms"]:
                            self.extract_messages(fs, artifacts["sms"])
                        if artifacts["contacts"]:
                            self.extract_contacts(fs, artifacts["contacts"])
                        if artifacts["photos"]:
                            for photo_path in artifacts["photos"]:
                                self.result_text.insert(tk.END, f"Photo: {photo_path}\n")
                        if artifacts["google_services"]:
                            self.extract_google_services(fs, artifacts["google_services"])
            else:
                self.result_text.insert(tk.END, f"Loading image: {image_path}\n")
                img = Img_Info(image_path)
                fs = FS_Info(img)
            
                artifacts = self.locate_artifacts(fs)
                if artifacts["call_logs"]:
                    self.extract_call_logs(fs, artifacts["call_logs"])
                if artifacts["sms"]:
                    self.extract_messages(fs, artifacts["sms"])
                if artifacts["contacts"]:
                    self.extract_contacts(fs, artifacts["contacts"])
                if artifacts["photos"]:
                    for photo_path in artifacts["photos"]:
                        self.result_text.insert(tk.END, f"Photo: {photo_path}\n")
                if artifacts["google_services"]:
                    self.extract_google_services(fs, artifacts["google_services"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract artifacts: {str(e)}")

    def extract_call_logs(self, fs, path):
        self.result_text.insert(tk.END, "Call Logs:\n")
        try:
            file_obj = fs.open(path)
            local_path = "calllog.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT number, date, duration, type FROM calls")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: Could not retrieve call logs: {e}\n")

    def extract_messages(self, fs, path):
        self.result_text.insert(tk.END, "Messages:\n")
        try:
            file_obj = fs.open(path)
            local_path = "mmssms.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT address, body, date FROM sms")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"{row[0]}\t{row[1]}\t{row[2]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: Could not retrieve messages: {e}\n")

    def extract_contacts(self, fs, path):
        self.result_text.insert(tk.END, "Contacts:\n")
        try:
            file_obj = fs.open(path)
            local_path = "contacts.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT display_name, phone_number FROM contacts")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"{row[0]}\t{row[1]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: Could not retrieve contacts: {e}\n")

    def extract_google_services(self, fs, path):
        self.result_text.insert(tk.END, "Google Services Data:\n")
        try:
            file_obj = fs.open(path)
            local_path = "google_services.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT service_name, data FROM services")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"Service: {row[0]}, Data: {row[1]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: Could not retrieve Google services data: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ForensicTool(root)
    root.mainloop()
