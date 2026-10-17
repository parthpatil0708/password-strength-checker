from flask import Flask, render_template, request
import re

app = Flask(__name__)


def check_password(password):
    score = 0
    suggestions = []

    checks = [
        (len(password) >= 8,
         "Use at least 8 characters."),

        (bool(re.search(r"[A-Z]", password)),
         "Add an uppercase letter (A-Z)."),

        (bool(re.search(r"[a-z]", password)),
         "Add a lowercase letter (a-z)."),

        (bool(re.search(r"[0-9]", password)),
         "Add a number (0-9)."),

        (bool(re.search(r"[^A-Za-z0-9]", password)),
         "Add a special character, such as @ or #.")
    ]

    for passed, message in checks:
        if passed:
            score += 1
        else:
            suggestions.append(message)

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions


@app.route("/", methods=["GET", "POST"])
def home():
    strength = None
    suggestions = []

    if request.method == "POST":
        password = request.form.get("password", "")

        if password:
            strength, suggestions = check_password(password)

    return render_template(
        "index.html",
        strength=strength,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)
