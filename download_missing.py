import os
import re
import urllib.request
from urllib.parse import urljoin

def download_missing_assets():
    if not os.path.exists('index.html'):
        return
        
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Corrected regex to get the FULL path
    paths = re.findall(r'/(?:wp-content|wp-includes)/[^\s"\'()>?]+', html)
    
    # Also check CSS files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.css'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        paths.extend(re.findall(r'/(?:wp-content|wp-includes)/[^\s"\'()>?]+', f.read()))
                except: pass

    base_url = "https://cytta.net/"
    downloaded_count = 0
    
    for path in set(paths):
        clean_path = path.split('?')[0].split('#')[0]
        local_path = clean_path.lstrip('/')
        local_fs_path = local_path.replace('/', os.sep)
        
        if not os.path.exists(local_fs_path):
            remote_url = urljoin(base_url, clean_path)
            try:
                os.makedirs(os.path.dirname(local_fs_path), exist_ok=True)
                print(f"Downloading: {clean_path}")
                urllib.request.urlretrieve(remote_url, local_fs_path)
                downloaded_count += 1
            except: pass

    print(f"Total files downloaded: {downloaded_count}")

if __name__ == "__main__":
    download_missing_assets()
