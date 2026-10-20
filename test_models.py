import requests

with open("api_key.txt") as f:
    key = f.read().strip()

payload = {"contents": [{"parts": [{"text": "BNS Section 103 kya hai? Ek line me Hindi me batao."}]}]}

# Stable aur fast models check karenge
candidate_models = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-3.8-flash"]

success = False
for model in candidate_models:
    print(f"Testing model: {model} ...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        print(f"\n--- SUCCESS! Model '{model}' Active Ho Gaya Hai ---")
        print(res.json()['candidates'][0]['content']['parts'][0]['text'])
        with open("active_model.txt", "w") as f:
            f.write(model)
        success = True
        break
    else:
        print(f"-> {model} status: {res.status_code}")

if not success:
    print("\nAccount par available models ki list:")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    r = requests.get(list_url).json()
    available = [m['name'].replace('models/', '') for m in r.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
    print(available)
