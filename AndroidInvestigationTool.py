import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from pytsk3 import Img_Info, FS_Info

class ForensicTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Mobile Forensics Tool")
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
        file_name = filedialog.askopenfilename(title="Select Dump Image", filetypes=[("All Files", "*.*")])
        if file_name:
            self.file_path.set(file_name)

    def extract_artifacts(self):
        image_path = self.file_path.get()
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("Error", "Invalid file path. Please select a valid dump image.")
            return

        try:
            # Load the image
            self.result_text.insert(tk.END, f"Loading image: {image_path}\n")
            img = Img_Info(image_path)
            fs = FS_Info(img)
            
            # System-Level Artifacts
            self.result_text.insert(tk.END, "\n[Extracting System-Level Artifacts]\n")
            self.extract_device_info(fs)
            self.extract_system_logs(fs)
            self.extract_root_status(fs)

            # User Data Artifacts
            self.result_text.insert(tk.END, "\n[Extracting User Data Artifacts]\n")
            self.extract_call_logs(fs)
            self.extract_contacts(fs)
            self.extract_messages(fs)

            # Media and Files
            self.result_text.insert(tk.END, "\n[Extracting Media and Files]\n")
            self.extract_photos(fs)
            self.extract_audio_files(fs)

            # App Data
            self.result_text.insert(tk.END, "\n[Extracting App Data]\n")
            self.extract_social_media_data(fs)

            # Network and Location
            self.result_text.insert(tk.END, "\n[Extracting Network and Location Data]\n")
            self.extract_location_data(fs)

            # Cloud and Synced Data
            self.result_text.insert(tk.END, "\n[Extracting Cloud and Synced Data]\n")
            self.extract_google_services_data(fs)

            # Deleted and Residual Data
            self.result_text.insert(tk.END, "\n[Extracting Deleted and Residual Data]\n")
            self.extract_deleted_files(fs)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract artifacts: {str(e)}")

    def extract_device_info(self, fs):
        self.result_text.insert(tk.END, "Device Information:\n")
        try:
            info_path = "/data/system/device_info.txt"
            file_obj = fs.open(info_path)
            data = file_obj.read_random(0, file_obj.info.meta.size).decode("utf-8")
            self.result_text.insert(tk.END, f"{data}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_system_logs(self, fs):
        self.result_text.insert(tk.END, "System Logs:\n")
        try:
            log_path = "/data/system/logs/system_log.txt"
            file_obj = fs.open(log_path)
            data = file_obj.read_random(0, file_obj.info.meta.size).decode("utf-8")
            self.result_text.insert(tk.END, f"{data}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_root_status(self, fs):
        self.result_text.insert(tk.END, "Root Status and Modifications:\n")
        try:
            root_path = "/data/system/root_status.txt"
            file_obj = fs.open(root_path)
            data = file_obj.read_random(0, file_obj.info.meta.size).decode("utf-8")
            self.result_text.insert(tk.END, f"{data}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_call_logs(self, fs):
        self.result_text.insert(tk.END, "Call Logs:\n")
        try:
            call_log_path = "/data/data/com.android.providers.contacts/databases/calllog.db"
            file_obj = fs.open(call_log_path)
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
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_contacts(self, fs):
        self.result_text.insert(tk.END, "Contacts:\n")
        try:
            contact_path = "/data/data/com.android.providers.contacts/databases/contacts.db"
            file_obj = fs.open(contact_path)
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
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_messages(self, fs):
        self.result_text.insert(tk.END, "Messages:\n")
        try:
            sms_path = "/data/data/com.android.providers.telephony/databases/mmssms.db"
            file_obj = fs.open(sms_path)
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
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_photos(self, fs):
        self.result_text.insert(tk.END, "Photos and Videos:\n")
        try:
            media_path = "/data/media/0/DCIM"
            directory = fs.open_dir(media_path)
            for entry in directory:
                self.result_text.insert(tk.END, f"{entry.info.name.name.decode('utf-8')}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_audio_files(self, fs):
        self.result_text.insert(tk.END, "Audio Files:\n")
        try:
            audio_path = "/data/media/0/Music"
            directory = fs.open_dir(audio_path)
            for entry in directory:
                self.result_text.insert(tk.END, f"{entry.info.name.name.decode('utf-8')}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_social_media_data(self, fs):
        self.result_text.insert(tk.END, "Social Media and Communication Apps:\n")
        try:
            social_path = "/data/data/com.social.app/databases/messages.db"
            file_obj = fs.open(social_path)
            local_path = "social_messages.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT sender, content, timestamp FROM messages")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"{row[0]}\t{row[1]}\t{row[2]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_location_data(self, fs):
        self.result_text.insert(tk.END, "Location Data:\n")
        try:
            loc_path = "/data/data/com.android.location/databases/location.db"
            file_obj = fs.open(loc_path)
            local_path = "location.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT latitude, longitude, timestamp FROM locations")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"{row[0]}\t{row[1]}\t{row[2]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

    def extract_google_services(self, fs):
        self.result_text.insert(tk.END, "Google Services Data:\n")
        try:
            # Assuming there's a database or file path for Google services data
            google_path = "/data/data/com.google.android/databases/google_services.db"
            file_obj = fs.open(google_path)
            local_path = "google_services.db"
            with open(local_path, "wb") as f:
                f.write(file_obj.read_random(0, file_obj.info.meta.size))
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            cursor.execute("SELECT service_name, data FROM google_services_table")
            rows = cursor.fetchall()
            for row in rows:
                self.result_text.insert(tk.END, f"{row[0]}\t{row[1]}\n")
            conn.close()
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
