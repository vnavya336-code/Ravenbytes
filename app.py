from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    student = {
        "name": request.form["name"],
        "level": request.form["level"],
        "category": request.form["category"],
        "income": request.form["income"],
        "marks": request.form["marks"]
    }

    return render_template("results.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)