import urllib.request
import os
import ssl

def download_yt_dlp():
    url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    target = os.path.join(os.getcwd(), "yt-dlp.exe")
    
    print(f"Downloading yt-dlp.exe from {url}...")
    
    try:
        # Create unverified context to avoid SSL errors
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            with open(target, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        print("Download complete!")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

if __name__ == "__main__":
    download_yt_dlp()
