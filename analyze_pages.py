import urllib.request, re, json, os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Download and analyze each page to understand which images appear where
pages = {
    'home': 'https://yuan-weijun.com/',
    'research': 'https://yuan-weijun.com/research',
    'datasets': 'https://yuan-weijun.com/datasets',
    'teaching': 'https://yuan-weijun.com/teaching',
    'resources': 'https://yuan-weijun.com/resources',
    'connect': 'https://yuan-weijun.com/connect',
}

# unique image base URLs (without format params)
def get_unique_images(html):
    imgs = set()
    # find all squarespace image base URLs
    all_urls = re.findall(r'https://images\.squarespace-cdn\.com/content/[^\s"\'<>?]+', html)
    for url in all_urls:
        if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            imgs.add(url)
    return imgs

page_data = {}

for name, url in pages.items():
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    imgs = get_unique_images(html)
    page_data[name] = list(imgs)
    print(f"\n=== {name.upper()} ({len(imgs)} images) ===")
    for img in sorted(imgs):
        print(f"  {img}")
    
    # Save HTML snippet around images for context
    img_contexts = []
    for img in imgs:
        idx = html.find(img)
        if idx > 0:
            context = html[max(0,idx-200):idx+200]
            # find alt text
            alt = re.findall(r'alt=["\']([^"\']*)["\']', context)
            title_match = re.findall(r'title=["\']([^"\']*)["\']', context)
            img_contexts.append({
                'url': img,
                'alt': alt,
                'title': title_match,
            })
    
    print(f"  Contexts:")
    for ctx in img_contexts:
        print(f"    alt={ctx['alt']} title={ctx['title']}")
        print(f"    url={ctx['url'][:80]}...")

# Download the unique images to local
print("\n\n=== Downloading images ===")
img_dir = 'c:/Users/xiong/WorkBuddy/20260404152812/images'
os.makedirs(img_dir, exist_ok=True)

downloaded = {}
all_imgs_flat = set()
for imgs in page_data.values():
    all_imgs_flat.update(imgs)

for img_url in sorted(all_imgs_flat):
    fname = img_url.split('/')[-1]
    local_path = f"{img_dir}/{fname}"
    if not os.path.exists(local_path):
        try:
            req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {fname} ({len(data)} bytes)")
            downloaded[img_url] = local_path
        except Exception as e:
            print(f"Failed {img_url}: {e}")
    else:
        print(f"Exists: {fname}")
        downloaded[img_url] = local_path

print("\nDone!")
