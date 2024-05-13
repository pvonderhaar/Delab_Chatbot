from chatbot_functions import generate_answer


def get_context():
    # Replace this with your implementation to get context
    return "Default context"



def main():
    # Get context
    context = get_context()

    # Print context
    print("Context:", context)

    # Get user input
    user_input = input("Your input: ")
    new_context = context + " user: " + user_input

    # Generate answer
    answer = generate_answer(new_context)

    # Print answer
    print("Bot:", answer)


if __name__ == "__main__":
    main()
