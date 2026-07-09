import os
import requests

def download_wakeword():
    url = "https://raw.githubusercontent.com/Picovoice/porcupine/master/resources/keyword_files/windows/jarvis_windows.ppn"
    folder = "wakeword"
    file_path = os.path.join(folder, "jarvis_windows.ppn")

    # Create folder if missing
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Created folder: {folder}")

    print("⬇ Downloading wake word model...")

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {file_path}")
    else:
        print("❌ Failed to download wake word file")
        print("HTTP Status:", response.status_code)

if __name__ == "__main__":
    download_wakeword()
