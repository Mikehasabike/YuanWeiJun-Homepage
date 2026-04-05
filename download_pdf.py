import urllib.request
import ssl

# Dropbox direct download URL
url = "https://www.dropbox.com/scl/fi/51e9zlf8v60ox71qy14ur/cv_weijun-yuan_short.pdf?rlkey=0y07ghoshx89e9ls0js6tg4gv&st=wn84dobl&dl=1"

# Set up SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Download file
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,application/octet-stream,*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.dropbox.com/',
})

print("Downloading...")
with urllib.request.urlopen(req, context=ctx) as response:
    content_type = response.headers.get('Content-Type', '')
    print(f"Content-Type: {content_type}")
    print(f"Status: {response.status}")
    
    # Read first few bytes
    first_bytes = response.read(10)
    print(f"First bytes: {first_bytes}")
    
    # Check if it's PDF
    if first_bytes.startswith(b'%PDF'):
        print("This IS a PDF file!")
        # Read the rest
        rest = response.read()
        data = first_bytes + rest
        with open("cv_download.pdf", "wb") as f:
            f.write(data)
        print("Saved to cv_download.pdf")
    else:
        print("Not a PDF - HTML content received")