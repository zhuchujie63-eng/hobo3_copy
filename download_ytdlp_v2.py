import urllib.request
import os
import ssl
import sys

def download_yt_dlp():
    url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    target = os.path.join(os.getcwd(), "yt-dlp.exe")
    
    print(f"Downloading yt-dlp.exe from {url}...")
    print(f"Target path: {target}")
    
    try:
        # Create unverified context to avoid SSL errors
        context = ssl._create_unverified_context()
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        with urllib.request.urlopen(req, context=context) as response:
            file_size = int(response.info().get('Content-Length', -1))
            print(f"File size: {file_size} bytes")
            
            downloaded = 0
            block_size = 8192
            
            with open(target, 'wb') as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Simple progress indicator
                    if file_size > 0:
                        percent = downloaded * 100 / file_size
                        sys.stdout.write(f"\rDownloaded: {downloaded} / {file_size} ({percent:.2f}%)")
                        sys.stdout.flush()
            
            print("\nDownload complete!")
            
            if os.path.exists(target):
                print(f"File exists at {target}")
                print(f"Size on disk: {os.path.getsize(target)} bytes")
                return True
            else:
                print("File not found after download!")
                return False
                
    except Exception as e:
        print(f"\nDownload failed: {e}")
        return False

if __name__ == "__main__":
    if download_yt_dlp():
        print("Success")
        sys.exit(0)
    else:
        print("Failure")
        sys.exit(1)
