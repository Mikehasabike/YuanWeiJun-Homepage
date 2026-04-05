import requests

# Dropbox URL 
url = "https://www.dropbox.com/scl/fi/51e9zlf8v60ox71qy14ur/cv_weijun-yuan_short.pdf"
params = {
    "rlkey": "0y07ghoshx89e9ls0js6tg4gv",
    "st": "wn84dobl",
    "dl": "1"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.dropbox.com/',
    'Connection': 'keep-alive',
}

print("Sending request...")
session = requests.Session()
response = session.get(url, params=params, headers=headers, allow_redirects=True, verify=False)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type', '')}")
print(f"Content-Length: {response.headers.get('Content-Length', 'unknown')}")
print(f"First 20 bytes: {response.content[:20]}")
print(f"URL: {response.url}")

if response.content[:4] == b'%PDF':
    print("SUCCESS: Got real PDF!")
    with open("cv_direct.pdf", "wb") as f:
        f.write(response.content)
    print("Saved to cv_direct.pdf")
else:
    print("Got HTML. Looking for download link in response...")
    import re
    links = re.findall(r'https://dl\.dropboxusercontent\.com[^"\'<>\s]+', response.text)
    if links:
        print("Found download links:")
        for link in links[:5]:
            print(" -", link)
    else:
        print("No direct download links found")
        # Print first 500 chars of response for debugging
        print("Response preview:")
        print(response.text[:500])