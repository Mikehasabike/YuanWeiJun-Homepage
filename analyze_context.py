import urllib.request, re, os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Fetch home page and research page with more context
for name, url in [('home', 'https://yuan-weijun.com/'), ('research', 'https://yuan-weijun.com/research'), ('datasets', 'https://yuan-weijun.com/datasets')]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    # Find image positions with surrounding text
    img_ids = re.findall(r'66b1ebb3d2c4363f432ff671/([a-f0-9-]+)/', html)
    seen = set()
    print(f"\n\n========= {name.upper()} PAGE - Image Contexts =========")
    for img_id in img_ids:
        if img_id in seen:
            continue
        seen.add(img_id)
        idx = html.find(img_id)
        if idx >= 0:
            # Get 500 chars before and after
            context_before = html[max(0, idx-800):idx]
            context_after = html[idx:idx+200]
            
            # extract text near image
            text_before = re.sub(r'<[^>]+>', ' ', context_before)
            text_before = re.sub(r'\s+', ' ', text_before).strip()[-300:]
            
            # Find filename
            filename_match = re.search(r'66b1ebb3d2c4363f432ff671/[a-f0-9-]+/([^\s"\'?<>]+)', html[idx:idx+200])
            filename = filename_match.group(1) if filename_match else 'unknown'
            
            print(f"\n--- Image: {img_id[:16]}... ({filename}) ---")
            print(f"Context before: ...{text_before[-200:]}")
