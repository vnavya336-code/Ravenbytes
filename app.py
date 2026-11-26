
from flask import Flask, render_template, request, jsonify

from eligibility import check_eligibility
from search_engine import search_online, get_all_schemes
from assistant import ask_ai

app = Flask(__name__)


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# SCHOLARSHIP ELIGIBILITY CHECKER
@app.route("/check", methods=["POST"])
def check():

    student = {
        "name": request.form.get("name", "").strip(),

        "education": request.form.get("education", "").strip(),

        "state": request.form.get("state", "Karnataka").strip(),

        "marks": request.form.get("marks", "").strip(),

        "income": request.form.get("income", "").strip(),

        "category": request.form.get("category", "").strip(),

        "gender": request.form.get("gender", "").strip(),

        "disability": request.form.get("disability", "").strip(),

        "religion": request.form.get("religion", "").strip(),

        "labour_worker": request.form.get("labour_worker", "").strip(),

        "ex_serviceman": request.form.get("ex_serviceman", "").strip(),

        "swanath": request.form.get("swanath", "").strip()
    }

    results = check_eligibility(
        student,
        get_all_schemes()
    )

    return render_template(
        "results.html",
        student=student,
        results=results
    )


# ONLINE SCHOLARSHIP DISCOVERY
@app.route("/discover")
def discover():

    query = request.args.get(
        "q",
        "Karnataka scholarships for SSLC 2nd PUC engineering students"
    )

    found, message = search_online(query)

    return jsonify({
        "results": found,
        "message": message
    })


# APPLICATION HEALTH CHECK
@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "project": "ScholarBridge"
    })


# AI ASSISTANT PAGE
@app.route("/chat")
def chat():

    return render_template("chat.html")


# GEMINI AI CHAT API
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()

    if not question:
        return jsonify({
            "reply": "Please enter a question."
        }), 400

    answer = ask_ai(question)

    return jsonify({
        "reply": answer
    })


# RUN FLASK APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
