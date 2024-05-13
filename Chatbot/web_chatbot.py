from chatbot_functions import generate_answer, get_context

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    # Get context
    context = get_context()
    return render_template("chat_temp.html", context=context)


@app.route("/ask", methods=["POST"])
def ask():
    # Get user input
    user_input = request.form["user_input"]

    context = get_context()
    # Generate answer
    answer = generate_answer(context, user_input)

    return answer


if __name__ == "__main__":
    app.run(debug=True)
