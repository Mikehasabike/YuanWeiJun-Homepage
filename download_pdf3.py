import requests
import re
import json

session = requests.Session()

# Set up browser-like headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}

# First visit the preview page to get cookies
preview_url = "https://www.dropbox.com/scl/fi/51e9zlf8v60ox71qy14ur/cv_weijun-yuan_short.pdf?rlkey=0y07ghoshx89e9ls0js6tg4gv&e=1&st=wn84dobl&dl=0"
print("Visiting preview page...")
resp = session.get(preview_url, headers=headers, verify=False)
print(f"Status: {resp.status_code}")
print(f"Cookies: {dict(session.cookies)}")

# Try to find direct download link in the page
# Look for dropboxusercontent URLs
links = re.findall(r'https://dl\.dropboxusercontent\.com[^"\'<>\s]+', resp.text)
print(f"Found {len(links)} dropboxusercontent links:")
for link in links[:5]:
    print(f"  {link}")

# Try direct download with cookie
download_url = "https://www.dropbox.com/scl/fi/51e9zlf8v60ox71qy14ur/cv_weijun-yuan_short.pdf?rlkey=0y07ghoshx89e9ls0js6tg4gv&e=1&st=wn84dobl&dl=1"
download_headers = headers.copy()
download_headers['Referer'] = preview_url
print("\nTrying download...")
dl_resp = session.get(download_url, headers=download_headers, allow_redirects=True, verify=False)
print(f"Download Status: {dl_resp.status_code}")
print(f"Content-Type: {dl_resp.headers.get('Content-Type', '')}")
print(f"Final URL: {dl_resp.url}")
print(f"First bytes: {dl_resp.content[:20]}")

if dl_resp.content[:4] == b'%PDF':
    print("SUCCESS: Got real PDF!")
    with open("cv_final.pdf", "wb") as f:
        f.write(dl_resp.content)
    print(f"Saved {len(dl_resp.content)} bytes")
else:
    print("Still got HTML...")