import os

files = ['app.py', 'templates/register.html', 'templates/index.html']
BOF = b'\xef\xbb\xbf'

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (not found)")
        continue
        
    with open(file_path, 'rb') as f:
        content = f.read()
        
    if content.startswith(BOF):
        print(f"Removing BOM from {file_path}")
        content = content[3:]
        with open(file_path, 'wb') as f:
            f.write(content)
    else:
        print(f"No BOM in {file_path}")
