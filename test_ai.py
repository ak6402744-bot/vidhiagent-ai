import requests

with open("api_key.txt") as f:
    key = f.read().strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={key}"
payload = {
    "contents": [{"parts": [{"text": "BNS (Bharatiya Nyaya Sanhita) Section 103 kya hai? Sirf do line me Hindi me batao."}]}]
}

res = requests.post(url, json=payload)
if res.status_code == 200:
    print("\n================================")
    print(" LEGAL AI ACTIVE - RESPONSE:")
    print("================================")
    print(res.json()['candidates'][0]['content']['parts'][0]['text'])
    print("================================")
else:
    print(f"Error {res.status_code}: {res.text}")
