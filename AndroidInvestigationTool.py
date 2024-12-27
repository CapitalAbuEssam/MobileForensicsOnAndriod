import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class MobileInvestigationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile Investigation Tool")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_tabs()

    def create_tabs(self):
        self.system_tab = ttk.Frame(self.notebook)
        self.user_data_tab = ttk.Frame(self.notebook)
        self.media_tab = ttk.Frame(self.notebook)
        self.app_data_tab = ttk.Frame(self.notebook)
        self.network_tab = ttk.Frame(self.notebook)
        self.cloud_tab = ttk.Frame(self.notebook)
        self.deleted_tab = ttk.Frame(self.notebook)
        self.specialized_tab = ttk.Frame(self.notebook)
        self.analytics_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.system_tab, text="System Artifacts")
        self.notebook.add(self.user_data_tab, text="User Data Artifacts")
        self.notebook.add(self.media_tab, text="Media and Files")
        self.notebook.add(self.app_data_tab, text="App Data")
        self.notebook.add(self.network_tab, text="Network & Location")
        self.notebook.add(self.cloud_tab, text="Cloud Data")
        self.notebook.add(self.deleted_tab, text="Deleted Data")
        self.notebook.add(self.specialized_tab, text="Specialized Artifacts")
        self.notebook.add(self.analytics_tab, text="Analytics & Usage")

        # Initialize each tab
        self.init_system_tab()
        self.init_user_data_tab()
        self.init_media_tab()
        self.init_app_data_tab()
        self.init_network_tab()
        self.init_cloud_tab()
        self.init_deleted_tab()
        self.init_specialized_tab()
        self.init_analytics_tab()

    def run_adb_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    def display_output(self, text_widget, data):
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, data)

    def init_system_tab(self):
        label = ttk.Label(self.system_tab, text="System-Level Artifacts", font=("Arial", 14))
        label.pack()

        self.system_output = scrolledtext.ScrolledText(self.system_tab, wrap=tk.WORD, height=20)
        self.system_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.system_tab, text="Fetch System Artifacts", command=self.fetch_system_artifacts)
        btn_fetch.pack()

    def fetch_system_artifacts(self):
        device_info = self.run_adb_command("adb shell getprop")
        system_logs = self.run_adb_command("adb logcat -d")
        root_status = self.run_adb_command("adb shell su -c 'echo Root Access' || echo 'No Root Access'")

        output = f"Device Information:\n{device_info}\n\nSystem Logs:\n{system_logs}\n\nRoot Status:\n{root_status}"
        self.display_output(self.system_output, output)

    def init_user_data_tab(self):
        label = ttk.Label(self.user_data_tab, text="User Data Artifacts", font=("Arial", 14))
        label.pack()

        self.user_data_output = scrolledtext.ScrolledText(self.user_data_tab, wrap=tk.WORD, height=20)
        self.user_data_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.user_data_tab, text="Fetch User Data", command=self.fetch_user_data)
        btn_fetch.pack()

    def fetch_user_data(self):
        call_logs = self.run_adb_command("adb shell content query --uri content://call_log/calls")
        contacts = self.run_adb_command("adb shell content query --uri content://contacts/phones")
        messages = self.run_adb_command("adb shell content query --uri content://sms")

        output = f"Call Logs:\n{call_logs}\n\nContacts:\n{contacts}\n\nMessages:\n{messages}"
        self.display_output(self.user_data_output, output)

    def init_media_tab(self):
        label = ttk.Label(self.media_tab, text="Media and Files", font=("Arial", 14))
        label.pack()

        self.media_output = scrolledtext.ScrolledText(self.media_tab, wrap=tk.WORD, height=20)
        self.media_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.media_tab, text="Fetch Media", command=self.fetch_media)
        btn_fetch.pack()

    def fetch_media(self):
        photos_videos = self.run_adb_command("adb shell ls /sdcard/DCIM")
        audio_files = self.run_adb_command("adb shell ls /sdcard/Music")
        documents = self.run_adb_command("adb shell ls /sdcard/Documents")

        output = f"Photos & Videos:\n{photos_videos}\n\nAudio Files:\n{audio_files}\n\nDocuments:\n{documents}"
        self.display_output(self.media_output, output)

    def init_app_data_tab(self):
        label = ttk.Label(self.app_data_tab, text="App Data", font=("Arial", 14))
        label.pack()

        self.app_data_output = scrolledtext.ScrolledText(self.app_data_tab, wrap=tk.WORD, height=20)
        self.app_data_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.app_data_tab, text="Fetch App Data", command=self.fetch_app_data)
        btn_fetch.pack()

    def fetch_app_data(self):
        social_media = self.run_adb_command("adb shell ls /sdcard/Android/data/com.facebook.katana")
        email_apps = self.run_adb_command("adb shell ls /sdcard/Android/data/com.google.android.gm")

        output = f"Social Media Data:\n{social_media}\n\nEmail Apps Data:\n{email_apps}"
        self.display_output(self.app_data_output, output)

    def init_network_tab(self):
        label = ttk.Label(self.network_tab, text="Network and Location", font=("Arial", 14))
        label.pack()

        self.network_output = scrolledtext.ScrolledText(self.network_tab, wrap=tk.WORD, height=20)
        self.network_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.network_tab, text="Fetch Network Data", command=self.fetch_network_data)
        btn_fetch.pack()

    def fetch_network_data(self):
        wifi_data = self.run_adb_command("adb shell dumpsys wifi")
        location_data = self.run_adb_command("adb shell dumpsys location")

        output = f"Wi-Fi Data:\n{wifi_data}\n\nLocation Data:\n{location_data}"
        self.display_output(self.network_output, output)

    def init_cloud_tab(self):
        label = ttk.Label(self.cloud_tab, text="Cloud and Synced Data", font=("Arial", 14))
        label.pack()

        self.cloud_output = scrolledtext.ScrolledText(self.cloud_tab, wrap=tk.WORD, height=20)
        self.cloud_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.cloud_tab, text="Fetch Cloud Data", command=self.fetch_cloud_data)
        btn_fetch.pack()

    def fetch_cloud_data(self):
        google_services = self.run_adb_command("adb shell pm list packages | grep google")

        output = f"Google Services:\n{google_services}"
        self.display_output(self.cloud_output, output)

    def init_deleted_tab(self):
        label = ttk.Label(self.deleted_tab, text="Deleted and Residual Data", font=("Arial", 14))
        label.pack()

        self.deleted_output = scrolledtext.ScrolledText(self.deleted_tab, wrap=tk.WORD, height=20)
        self.deleted_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.deleted_tab, text="Fetch Deleted Data", command=self.fetch_deleted_data)
        btn_fetch.pack()

    def fetch_deleted_data(self):
        deleted_files = self.run_adb_command("adb shell ls /data/data/com.android.providers.downloads/cache")

        output = f"Deleted Files:\n{deleted_files}"
        self.display_output(self.deleted_output, output)

    def init_specialized_tab(self):
        label = ttk.Label(self.specialized_tab, text="Specialized Artifacts", font=("Arial", 14))
        label.pack()

        self.specialized_output = scrolledtext.ScrolledText(self.specialized_tab, wrap=tk.WORD, height=20)
        self.specialized_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.specialized_tab, text="Fetch Specialized Data", command=self.fetch_specialized_data)
        btn_fetch.pack()

    def fetch_specialized_data(self):
        iot_data = self.run_adb_command("adb shell ls /data/data/com.iot")

        output = f"IoT Data:\n{iot_data}"
        self.display_output(self.specialized_output, output)

    def init_analytics_tab(self):
        label = ttk.Label(self.analytics_tab, text="Analytics and Usage", font=("Arial", 14))
        label.pack()

        self.analytics_output = scrolledtext.ScrolledText(self.analytics_tab, wrap=tk.WORD, height=20)
        self.analytics_output.pack(fill='both', expand=True)

        btn_fetch = ttk.Button(self.analytics_tab, text="Fetch Analytics Data", command=self.fetch_analytics_data)
        btn_fetch.pack()

    def fetch_analytics_data(self):
        clipboard_data = self.run_adb_command("adb shell dumpsys clipboard")

        output = f"Clipboard Data:\n{clipboard_data}"
        self.display_output(self.analytics_output, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = MobileInvestigationTool(root)
    root.mainloop()
