from flask import Flask, render_template, request
from model import GenerationModel

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("text_input")
        try:
            model = GenerationModel()
            result = model.generate_recipe(user_input)
            return render_template("index.html", result=result, user_input=user_input)
        except Exception as e:
            return render_template(
                "index.html", result=None, user_input=user_input, error=str(e)
            )

    return render_template("index.html", user_input="")


if __name__ == "__main__":
    app.run(debug=True)
