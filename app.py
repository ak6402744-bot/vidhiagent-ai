from flask import Flask, render_template, request, jsonify
import requests
import time
import os

app = Flask(__name__)

# Key Cloud Environment se lega, agar nahi mila to local file se
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY and os.path.exists("api_key.txt"):
    with open("api_key.txt") as f:
        API_KEY = f.read().strip()

MODELS = ["gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.5-flash", "gemini-flash-lite-latest"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json or {}
    draft_type = data.get('draft_type', '')
    lang = data.get('lang', 'English')
    facts = data.get('facts', '')
    image_data = data.get('image_data', None)

    prompt = f"""
You are VidhiAgent, an elite Indian Legal AI expert in Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA).
Language Preference: {lang}.

Instructions based on service:
1. If "Bail Application" or "Anticipatory Bail": Draft in formal court petition format (Cause Title, Sections, Grounds under BNS/BNSS, Prayer Clause, Verification, and Stamp Paper Affidavit).
2. If "Cross-Examination Questions": Formulate 15-20 sharp, destructive cross-examination questions to expose witness contradictions under BSA principles.
3. If "FIR Analysis & Counter Grounds": Identify police procedural violations (BNSS 35, 105), factual contradictions, and list strong bail/discharge grounds.
4. If "BNS to IPC Section Converter": Map every section between old IPC/CrPC and new BNS/BNSS with essential ingredients.

Task: {draft_type}
Client Input / Facts: {facts}

Provide clear, professional output formatted in clean Markdown.
"""

    parts = [{"text": prompt}]
    if image_data:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_data}})

    payload = {"contents": [{"parts": parts}]}

    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        for _ in range(2):
            try:
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    return jsonify({'result': res.json()['candidates'][0]['content']['parts'][0]['text']})
                elif res.status_code == 503:
                    time.sleep(1.5)
                    continue
                else:
                    break
            except Exception:
                break

    return jsonify({'result': 'AI Server busy hai. Kripya thodi der baad dubara try karein.'})


from flask import send_from_directory

@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def serve_sw():
    resp = send_from_directory("static", "sw.js", mimetype="application/javascript")
    resp.headers["Service-Worker-Allowed"] = "/"
    return resp


@app.route("/privacy")
def privacy_policy():
    return render_template("privacy.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
