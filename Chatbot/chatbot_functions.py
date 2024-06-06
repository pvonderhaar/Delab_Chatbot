import random
import re
from flask import Flask, render_template_string, send_file
from PIL import Image, ImageDraw
import io
import pandas as pd


def generate_answer(user_input, context=None):
    # TODO: write backend script using a gpt model and our own data to generate the answer of the bot (Wensch)
    bot_answer = 'This will be the answer of the bot'
    # I displayed the context here to check if the right context is given to this function
    answer = f"Context: {context} <br> Your answer: {user_input} <br> {bot_answer}"
    return answer


def get_context(conv_df=None):
    # TODO: Get 3-5 posts from a conversation in Dataset to answer to (Pauline)
    if conv_df is None:
        conv_df = pd.read_pickle("../data/conv_delab.pickle")
        conv_df['checked'] = False
    index_list = conv_df.index.tolist()
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
        if int(conv_seqid) > 3 & int(conv_seqid)>len(context_sequence):
            context_sequence = context_sequence[(context_sequence['conv_seqid']>=conv_seqid - 2)
                                                (context_sequence['conv_seqid']<=conv_seqid + 2)]
        else:
            # der Einfachkeit halber den context ab dem ersten post
            context_sequence = context_sequence.head(5)

    context_dict = {}
    authors = context_sequence['author_id'].unique().tolist()
    for index, row in context_sequence.iterrows():
        typ = type(row)
        author_id = row['author_id']
        author = authors.index(author_id)
        text = row['text']
        cleaned_text = re.sub(r'@\w+', '', text)
        # Remove extra spaces that might be left
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        context_dict[author] = cleaned_text

    return context_dict
