from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        name = request.form.get("name")
        age = int(request.form.get("age"))

        if age >= 18:
            result = f"Hello {name}, you are eligible to vote"
        else:
            result = f"Hello {name}, you are NOT eligible to vote"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
