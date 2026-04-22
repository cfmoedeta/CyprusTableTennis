import os

def replace_in_files(directory, old_text, new_text):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.css', '.js', '.html')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if old_text in content:
                        print(f"Updating: {path}")
                        new_content = content.replace(old_text, new_text)
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {path}: {e}")

# Replace both normal and escaped slashes
replace_in_files('.', 'https://cytta.net/', './')
replace_in_files('.', 'https:\\/\\/cytta.net\\/', './')
