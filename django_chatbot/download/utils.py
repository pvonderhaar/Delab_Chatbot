import sys
import os
from delab_trees import TreeManager
from delab_trees.delab_post import DelabPost
from delab_trees.delab_tree import DelabTree
from delab_trees.util import get_root
import networkx as nx
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..' ,'delab-socialmedia')))

from connection_util import get_praw, create_mastodon
from socialmedia import PLATFORM, LANGUAGE, download_conversations, download_daily_sample_conversations


def download(user_input):
    if user_input == "mastodon":
        download_mastodon()
    if user_input == "reddit":
        download_reddit()


def download_mastodon():
    # TODO: Mastodon App erstellen
    relative_path = '../../secret/mastodon_secret.yaml'

    # Der absolute Pfad relativ zum aktuellen Skript
    absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))

    mastodon = create_mastodon()

    conversations = download_daily_sample_conversations(platform=PLATFORM.MASTODON,
                                                        language=LANGUAGE.ENGLISH,
                                                        min_results=5,
                                                        connector=mastodon)

    return trees_to_file(conversations)


def download_reddit():
    # TODO: Julians Zugangsdaten finden/ nachfragen
    reddit = get_praw(
        use_yaml=True,
        yaml_path='../../secret/reddit_secret.yaml'
    )
    conversations = download_conversations(query_string="Politics",
                                           platform=PLATFORM.REDDIT,
                                           language=LANGUAGE.ENGLISH,
                                           recent=True,
                                           max_conversations=30,
                                           connector=reddit)
    return trees_to_file(conversations)


def trees_to_file(conversations):
    # TODO: nochmal delab_trees anschauen und schauen was kommt
    posts_dict = {"post_id": [], "parent_id": [], "text": [], "tree_id": [], "author_id": [], "created_at": []}
    for conversation in conversations:
        for post in conversation:
            posts_dict["post_id"].append(post.post_id)
            posts_dict["parent_id"].append(post.parent_id)
            posts_dict["text"].append(post.text)
            posts_dict["tree_id"].append(post.tree_id)
            posts_dict["author_id"].append(post.author_id)
            posts_dict["created_at"].append(post.created_at)

    posts_df = pd.DataFrame(posts_dict)
    treemanger = TreeManager(posts_df)
    trees = treemanger.trees
    paths_dict = {'conv_id': [], 'conv_path': [], 'conv_seqid': [], 'text': [], 'author_id': []}
    trees_paths = []
    for tree in trees.values():
        paths = []
        tree_as_tree = tree.as_tree()
        root = get_root(tree_as_tree)
        for node in tree_as_tree:
            if tree_as_tree.out_degree(node) == 0:  # it's a leaf
                path = list(nx.shortest_path(tree_as_tree, root, node))
                paths.append(list(path))
        trees_paths.append(paths)

    i = 0
    cur_tree_id = None
    for path in trees_paths:
        j=1
        for post in path:
            row = posts_df.loc[posts_df['post_id']==post]
            tree_id = row['tree_id']

        if cur_tree_id == tree_id:
            i+=1
        else:
            i = 1
            cur_tree_id = tree_id







    print("Downloaded conversations!")
    return False
