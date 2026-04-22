import os
import re
import urllib.request
from urllib.parse import urljoin

def download_missing_assets():
    if not os.path.exists('index.html'):
        print("index.html not found!")
        return
        
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all paths starting with /wp-content or /wp-includes
    # This regex is a bit more robust for standard HTML attributes
    paths = re.findall(r'/(wp-content|wp-includes)/[^\s"\'()>?]+', html)
    
    base_url = "https://cytta.net/"
    
    # Also look for things in CSS files
    css_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.join(root, file))
    
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                paths.extend(re.findall(r'/(wp-content|wp-includes)/[^\s"\'()>?]+', css_content))
        except:
            pass

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
                urllib.request.urlretrieve(remote_url, local_path)
                print(f"Successfully downloaded: {local_path}")
            except Exception as e:
                print(f"Failed to download {remote_url}: {e}")

if __name__ == "__main__":
    download_missing_assets()
