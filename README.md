# Mobile Investigation Tool

A Python-based GUI application that utilizes ADB (Android Debug Bridge) commands to fetch and display various artifacts from an Android device. The tool is designed for forensics, debugging, or general investigation purposes. It is compatible with devices running Android 9 (Pie) or later.

---

## Features

The application includes the following functionalities:

1. **System Artifacts**: Fetch system-level details such as device properties, system logs, and root status.
2. **User Data Artifacts**: Extract call logs, contacts, and SMS messages.
3. **Media and Files**: Retrieve lists of photos, videos, audio files, and documents stored on the device.
4. **App Data**: Display data related to specific applications like social media and email apps.
5. **Network & Location**: Gather network and location details including Wi-Fi and GPS information.
6. **Cloud Data**: Identify packages related to Google services or other cloud integrations.
7. **Deleted Data**: Locate residual or deleted files in specific cache directories.
8. **Specialized Artifacts**: Investigate data related to IoT or other specialized sources.
9. **Analytics & Usage**: Fetch usage and clipboard data.

---

## Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.6 or later
- **ADB**: Installed and added to the system's PATH
- **Tkinter**: Installed (comes pre-installed with most Python distributions)

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/CapitalAbuEssam/mobile-investigation-tool.git
    cd mobile-investigation-tool
    ```

2. Install dependencies (if necessary):
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure ADB is installed and configured on your system. To check, run:
    ```bash
    adb version
    ```
4. ADB (Android Debug Bridge) Tools
The script uses ADB commands to interact with Android devices. Make sure ADB is installed and accessible from your terminal.

You can install ADB if it's not installed:

```bash
Copy code
sudo apt-get install adb  # On Linux (Ubuntu/Debian-based)
brew install android-platform-tools # On macOS with Homebrew
sudo pacman -S android-tools # On Arch Linux
```

5. Connect your Android device via USB and enable **USB Debugging** from Developer Options.

---

## Usage

1. Run the application:
    ```bash
    python mobile_investigation_tool.py
    ```

2. Connect your Android device and ensure it is recognized by ADB:
    ```bash
    adb devices
    ```

3. Use the application interface to explore various tabs and fetch desired data:
    - **System Artifacts**: Click "Fetch System Artifacts" to view device properties, logs, and root status.
    - **User Data Artifacts**: Retrieve call logs, contacts, and SMS messages.
    - **Media and Files**: Browse photos, videos, audio, and document files.
    - **App Data**: Analyze data stored by social media and email apps.
    - **Network & Location**: Inspect Wi-Fi and location information.
    - **Cloud Data**: View details of cloud services used by the device.
    - **Deleted Data**: Locate residual or deleted files.
    - **Specialized Artifacts**: Examine IoT-related data.
    - **Analytics & Usage**: Access clipboard and analytics information.

---

## Compatibility

- **Android Version**: Designed for Android 9 (Pie) and later
- **ADB Permissions**: Some features require elevated permissions or root access on the device.

---

## Screenshots

*(Add screenshots of the application interface showing different tabs)*

---

## Limitations

1. Requires USB Debugging to be enabled on the Android device.
2. Root access is necessary for certain operations.
3. Some commands may vary based on the Android version and device manufacturer.

---

## Reuse

Reuse I don't mind them just pay me hommage


