import os
import re
import urllib.request
import urllib.parse
from urllib.parse import urljoin
import sys

# Ensure output is UTF-8 to handle Greek characters in console
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def download_missing_assets():
    if not os.path.exists('index.html'):
        return
        
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    paths = re.findall(r'/(?:wp-content|wp-includes)/[^\s"\'()>?]+', html)
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.css'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        paths.extend(re.findall(r'/(?:wp-content|wp-includes)/[^\s"\'()>?]+', f.read()))
                except: pass

    base_url = "https://cytta.net/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    downloaded_count = 0
    
    for path in set(paths):
        try:
            clean_path = path.split('?')[0].split('#')[0]
            local_path = clean_path.lstrip('/')
            
            # Encode URL properly for characters like Greek or spaces
            encoded_path = urllib.parse.quote(local_path)
            remote_url = urljoin(base_url, encoded_path)
            
            local_fs_path = local_path.replace('/', os.sep)
            
            if not os.path.exists(local_fs_path):
                os.makedirs(os.path.dirname(local_fs_path), exist_ok=True)
                print(f"Downloading: {remote_url}")
                req = urllib.request.Request(remote_url, headers=headers)
                with urllib.request.urlopen(req) as response, open(local_fs_path, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"Success: {local_fs_path}")
                downloaded_count += 1
        except Exception as e:
            try:
                print(f"Failed to process a file: {e}")
            except: pass

    print(f"Total files downloaded: {downloaded_count}")

if __name__ == "__main__":
    download_missing_assets()
