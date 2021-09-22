from telegram import Bot, InputMediaPhoto
import logging

from api import Api
from config import TOKEN, CHATS, DISTRICTS, MAX_PRICE

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def send_photos(bot, chat_id, urls):
    media_group = [InputMediaPhoto(u) for u in urls[:4]]
    bot.sendMediaGroup(chat_id, media_group)


def read_seen():
    seen = set()

    try:
        with open('seen.txt') as f:
            for line in f.readlines():
                seen.add(line.strip())
    except:
        print("seen.txt not found")
    return seen


def append_to_seen(urls):
    try:
        with open('seen.txt', 'a+') as f:
            for u in urls:
                f.write(f"{u}\n")
    except:
        print("Error while writing to seen")


def check_district(district_id):
    seen = read_seen()

    api = Api()
    flats = api.get_list(district_id, MAX_PRICE)

    bot = Bot(TOKEN)

    not_seen = [f for f in flats if f['url'] not in seen]
    for f in not_seen:
        try:
            ff = api.get_flat(f['url'])
            f['images'] = ff['images']
        except:
            print(f"error while getting flat info {f['url']}")

    for f in not_seen:
        for chat_id in CHATS:
            try:
                send_photos(bot, chat_id, f['images'])
            except:
                print(f"Error while trying to send photos for {f['url']}")

            bot.send_message(chat_id, f"{f['price']} {f['district']} \n "
                                      f"{f['title']} \n "
                                      f"{f['area']} -- {f['human_datetime']} \n"
                                      f"{f['url']}")

    append_to_seen([f['url'] for f in not_seen])


def main() -> None:
    """Start the bot."""

    for district_id in DISTRICTS:
        check_district(district_id)


if __name__ == '__main__':
    main()
