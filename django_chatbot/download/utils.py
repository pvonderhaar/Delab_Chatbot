import delab_trees
from connection_util import get_praw
from connection_util import create_mastodon
from socialmedia import download_conversations, PLATFORM, LANGUAGE, download_daily_sample_conversations


def download(user_input):
    if user_input == "mastodon":
        download_mastodon()
    if user_input == "reddit":
        download_reddit()


def download_mastodon():
    # TODO: Mastodon App erstellen
    mastodon = create_mastodon(
        use_yaml=True,
        yaml_path='path/to/your/social_media_credentials.yml'
    )
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
    return False
