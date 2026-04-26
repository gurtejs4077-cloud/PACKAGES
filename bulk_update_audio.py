import os
import re

directory = '/home/gurtej-singh/Desktop/All Folders/main page '
files = [f for f in os.listdir(directory) if f.endswith('.html')]

# The tags to inject
inject_tags = '<link rel="stylesheet" href="background-audio.css">\n    <script src="background-audio.js" defer></script>\n</head>'

# Pattern to find </head>
head_pattern = re.compile(r'</head>', re.IGNORECASE)

# Pattern to find old audio/script block
old_audio_pattern = re.compile(r'<audio id="bgMusic" loop>.*?</script>', re.DOTALL | re.IGNORECASE)

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Skip if already injected
    if 'background-audio.js' in content:
        print(f"Skipping {filename} - already updated.")
        continue
    
    # 2. Inject new tags before </head>
    if head_pattern.search(content):
        content = head_pattern.sub(inject_tags, content)
    
    # 3. Remove old audio blocks if they exist
    content = old_audio_pattern.sub('', content)
    
    # 4. Save
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {filename}")

print("Done updating all HTML files.")
