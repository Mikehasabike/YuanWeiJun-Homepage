import urllib.request, re, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

pages = [
    'https://yuan-weijun.com/',
    'https://yuan-weijun.com/research',
    'https://yuan-weijun.com/datasets',
    'https://yuan-weijun.com/teaching',
    'https://yuan-weijun.com/resources',
    'https://yuan-weijun.com/connect',
]

all_imgs = set()
all_fonts = set()

for url in pages:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode('utf-8', errors='ignore')
        
        # img src
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
        for img in imgs:
            if img.startswith('//'):
                img = 'https:' + img
            all_imgs.add(img)
        
        # data-src
        dsrcs = re.findall(r'data-src=["\']([^"\']+)["\']', html, re.IGNORECASE)
        for d in dsrcs:
            if d.startswith('//'):
                d = 'https:' + d
            all_imgs.add(d)
        
        # squarespace cdn
        cdn = re.findall(r'https://[a-z0-9]+\.squarespace[^\s"\'<>]+', html)
        for c in cdn:
            if any(ext in c.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif', 'image']):
                all_imgs.add(c)
        
        # fonts
        gf = re.findall(r'fonts\.googleapis\.com[^"\']+', html)
        for f in gf:
            all_fonts.add('https://' + f)
        
        ff = re.findall(r"font-family\s*:\s*'?([^;'\"{}]+)'?", html)
        for f in ff:
            all_fonts.add(f.strip())
        
        print(f"Fetched {url} - HTML len: {len(html)}")
        
        # Save first 2000 chars for inspection
        if 'yuan-weijun.com/' == url or url == 'https://yuan-weijun.com/':
            with open('c:/Users/xiong/WorkBuddy/20260404152812/home_html_sample.txt', 'w', encoding='utf-8') as f:
                f.write(html[:5000])
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")

print("\n=== All Images Found ===")
for img in sorted(all_imgs):
    print(img)

print("\n=== All Fonts Found ===")
for f in sorted(all_fonts):
    print(f)
