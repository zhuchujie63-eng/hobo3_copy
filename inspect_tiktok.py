import urllib.request
import re
import json

url = "https://www.tiktok.com/@ellafilm2/video/7518645660669840654?is_from_webapp=1&sender_device=pc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.tiktok.com/"
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html_content = response.read().decode('utf-8')
        
    print(f"HTML Length: {len(html_content)}")
    print(f"Content Preview: {html_content[:500]}")
    
    # Check for subtitleInfos
    matches = re.findall(r'"subtitleInfos":\[(.*?)\]', html_content)
    print(f"subtitleInfos matches: {len(matches)}")
    for i, m in enumerate(matches):
        print(f"Match {i}: {m[:200]}...")
        
    # Check for Universal Data
    uni_match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html_content)
    if uni_match:
        print("Found __UNIVERSAL_DATA_FOR_REHYDRATION__")
        try:
            data = json.loads(uni_match.group(1))
            # Try to find subtitleInfos in data
            print("Parsed JSON successfully")
        except:
            print("Failed to parse JSON")
    else:
        print("No __UNIVERSAL_DATA_FOR_REHYDRATION__ found")

    # Check for SIGI_STATE
    sigi_match = re.search(r'window\.SIGI_STATE\s*=\s*({.*?});', html_content)
    if sigi_match:
        print("Found SIGI_STATE")
    else:
        print("No SIGI_STATE found")
        
except Exception as e:
    print(f"Error: {e}")
