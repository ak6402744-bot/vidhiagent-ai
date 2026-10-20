import requests

key = input("Apni Gemini API Key paste karein aur Enter dabayein: ").strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={key}"
payload = {
    "contents": [{"parts": [{"text": "BNS Section 103 kya hai? Ek line me Hindi me batao."}]}]
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    print("\n--- SUCCESS! AI RESPONSE ---")
    print(response.json()['candidates'][0]['content']['parts'][0]['text'])
    with open("api_key.txt", "w") as f:
        f.write(key)
    print("\n[OK] API Key successfully save ho gayi hai!")
else:
    print(f"\nError: {response.status_code}")
    print(response.text)
