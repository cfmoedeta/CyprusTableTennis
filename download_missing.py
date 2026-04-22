import os
import re
import requests
from urllib.parse import urljoin

def download_missing_assets():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all paths starting with /wp-content or /wp-includes
    paths = re.findall(r'/(wp-content|wp-includes)/[^\s"\'()>?]+', html)
    
    base_url = "https://cytta.net/"
    
    for path in set(paths):
        # Clean path from query strings or fragments
        clean_path = path.split('?')[0].split('#')[0]
        if clean_path.startswith('/'):
            local_path = clean_path.lstrip('/')
        else:
            local_path = clean_path
            
        local_path = local_path.replace('/', os.sep)
        
        if not os.path.exists(local_path):
            print(f"Missing: {local_path}")
            remote_url = urljoin(base_url, clean_path)
            try:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                print(f"Downloading from: {remote_url}")
                r = requests.get(remote_url, stream=True)
                if r.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Successfully downloaded: {local_path}")
                else:
                    print(f"Failed to download (Status {r.status_code}): {remote_url}")
            except Exception as e:
                print(f"Error downloading {remote_url}: {e}")

if __name__ == "__main__":
    download_missing_assets()
