import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
from config import Config

SOUNDCLOUD_URL = "https://soundcloud.com"
SOUNDCLOUD_LIKES_URL = "https://soundcloud.com/" + Config.username + "/likes"


def get_recent_likes():
    recent_likes = []

    with requests.Session() as sess:
        response = sess.get(SOUNDCLOUD_LIKES_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        like_container = soup.find_all('article')
        for like in like_container:
            if like.h2.a is not None:
                recent_likes.append(SOUNDCLOUD_URL + like.h2.a['href'])

    return recent_likes


def send_embed(song_data):
    webhook = DiscordWebhook(Config.webhook_url)

    try:
        embed = DiscordEmbed(title=song_data['title'], description=song_data['description'], color="c0c4c4")
    except:
        embed = DiscordEmbed(title=song_data['title'], description=None, color="c0c4c4")

    embed.add_embed_field(name="Artist", value=song_data['user']['username'], inline=False)
    embed.add_embed_field(name="URL", value=str(song_data['permalink_url']), inline=False)

    embed.add_embed_field(name="Duration (ms)", value=song_data['duration'], inline=True)
    embed.add_embed_field(name="Upload Date", value=song_data['display_date'], inline=True)

    embed.set_image(url=song_data['artwork_url'].replace('-large', '-t500x500'))
    webhook.add_embed(embed)

    return webhook.execute()
