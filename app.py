import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key and os.path.exists("api_key.txt"):
    with open("api_key.txt") as f:
        api_key = f.read().strip()

if api_key:
    genai.configure(api_key=api_key)

SYSTEM_PROMPT = """You are 'VidhiAgent Pro AI', a senior Indian High Court and Supreme Court drafting advocate and legal procedural expert.
You draft precise court petitions under the Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA).
Always maintain professional court formatting with title, case details, grounds, verification, and affidavits where required."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/sw.js")
def service_worker():
    response = send_from_directory("static", "sw.js")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Content-Type"] = "application/javascript"
    return response

@app.route("/api/draft", methods=["POST"])
def draft():
    try:
        data = request.json or {}
        task = data.get("task", "Bail Petition")
        language = data.get("language", "English")
        facts = data.get("facts", "")

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        prompt = f"Task: {task}\nLanguage: {language}\nDetails/Facts:\n{facts}"
        response = model.generate_content(prompt)
        return jsonify({"success": True, "draft": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
