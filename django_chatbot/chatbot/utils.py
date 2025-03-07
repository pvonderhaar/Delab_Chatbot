import random
import re
import pandas as pd
import json
import requests
from pathlib import Path


def generate_answer(user_input, context=None):
    # TODO: load answers from docker
    """    bot_answer = 'This will be the answer of the bot'
    # I displayed the context here to check if the right context is given to this function
    answer = f"Context: {context} <br> Your answer: {user_input} <br> {bot_answer}"
    """
    base_url = "http://localhost:8840/analytics"
    headers = {"Content-Type": "application/json"}
    # TODO: Structure payload correctly, so that the api can use it
    payload = {"texts": [user_input]}

    # Send requests to different analytics endpoints
    try:

        response_general = requests.post(base_url, headers=headers, json=payload).json()
        response_sentiment = requests.post(f"{base_url}?analytics=sentiment", headers=headers, json=payload).json()
        response_justification = requests.post(f"{base_url}?analytics=justification", headers=headers,
                                               json=payload).json()
        response_cosine = requests.post(f"{base_url}?analytics=cosine", headers=headers, json=payload).json()

        # Combine the responses into a structured format
        print("Calculating bot anwer")
        bot_answer = {
            "general": response_general,
            "sentiment": response_sentiment,
            "justification": response_justification,
            "cosine": response_cosine
        }

    except requests.exceptions.RequestException as e:
        bot_answer = f"Error connecting to Docker service: {e}"

    # Display context and response
    answer = f"Context: {context} <br> Your input: {user_input} <br> Bot answer: {json.dumps(bot_answer, indent=2)}"
    return answer


def get_context(conv_df=None):
    # TODO: resolve error:TypeError: unsupported operand type(s) for -: 'str' and 'int'
    if conv_df is None:
        folder_path = Path('../data')
        file_name = 'conv_delab.pickle'

        # Construct the full file path
        file_path = folder_path / file_name
        if file_path.exists():
            conv_df = pd.read_pickle("../data/conv_delab.pickle")
            conv_df['checked'] = False
        else:
            file_name = 'downloaded.pickle'
            file_path = folder_path / file_name
            if not file_path.exists():
                return "Go to /download"
            else:
                conv_df = pd.read_pickle("../data/downloaded.pickle")
                conv_df['checked'] = False
    if conv_df['checked'].all():
        return "Go to /download"
    index_list = conv_df[conv_df['checked']==False].index.tolist()
    rndm = random.choice(index_list)
    context_row = conv_df.iloc[rndm].to_frame().T
    conv_id = context_row['conv_id'].iloc[0]
    conv_path = context_row['conv_path'].iloc[0]
    conv_seqid = context_row['conv_seqid'].iloc[0]
    context_sequence = conv_df[(conv_df['conv_id']==conv_id) & (conv_df['conv_path']==conv_path)]
    if len(context_sequence)<3:
        id = context_row.index[0]
        conv_df.loc[id, 'checked']=True
        return get_context(conv_df)
    if len(context_sequence)>=5:
        if (int(conv_seqid) > 3) & (int(conv_seqid)<=len(context_sequence)-2):
            context_sequence = context_sequence[(context_sequence['conv_seqid']>=conv_seqid - 2) &
                                                (context_sequence['conv_seqid']<=conv_seqid + 2)]
        else:
            # der Einfachkeit halber den context ab dem ersten post
            context_sequence = context_sequence.head(5)
    context_dict = {}
    authors = context_sequence['author_id'].unique().tolist()
    for index, row in context_sequence.iterrows():
        author_id = row['author_id']
        author = authors.index(author_id)
        text = row['text']
        cleaned_text = re.sub(r'@\w+', '', text)
        # Remove extra spaces that might be left
        post_dict = {}
        post_dict[author] = cleaned_text
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        context_dict[index] = post_dict

    return context_dict
