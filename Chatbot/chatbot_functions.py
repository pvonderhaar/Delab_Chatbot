import pandas as pd


def generate_answer(context, user_input):
    # TODO: write backend script using a gpt model and our own data to generate the answer of the bot (Wensch)
    bot_answer = 'This will be the answer of the bot'
    answer = f"Context: {context} <br> Your answer: {user_input} <br> {bot_answer}"
    return answer


def get_context():
    # TODO: Get 3-5 posts from a conversation in Dataset to answer to (Pauline)
    context = 'the posts before this'
    return context
