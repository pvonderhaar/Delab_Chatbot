from chatbot_functions import generate_answer, get_context

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'delab_goe' #This is not a sensitive webapp (yet), so the key is just displayed

# TODO: maybe add a db in the backend for a more elegant solution
@app.route("/")
def index():
    session['context'] = get_context()
    return render_template("chat_temp.html", context=session["context"])


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    context = session['context']

    answer = generate_answer(user_input, context)

    return answer


if __name__ == "__main__":
    app.run(debug=True)
