import pytz
from datetime import datetime

tz = pytz.timezone('Europe/Kiev')

MONTHS = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря',
]

NUMBER_OF_MONTH = {}
for i, name in enumerate(MONTHS):
    NUMBER_OF_MONTH[name] = f"{i+1:02}"


def parse_human_datetime(human_time_str):
    if human_time_str.startswith('Сегодня '):
        timestr = human_time_str.split(' в ')[1]
        now = datetime.now().astimezone(tz)
        return now.strftime(f'%Y-%m-%dT{timestr}:00%z')[:-2] + ':00'
    else:
        human_time_str = human_time_str.replace(' г.', '')
        parts = human_time_str.split(' ')
        month_name = parts[1]
        month_number = NUMBER_OF_MONTH[month_name]
        year = parts[2]
        day = parts[0]
        return f"{year}-{month_number}-{day}"


def parse_card(soup):
    a = soup.select_one('a')

    url = "{}{}".format('https://www.olx.ua', a['href'])

    ps = soup.select('p')

    title = ps[0].text
    price = ps[1].text
    district = ps[2].text
    human_datetime = ps[3].text
    datetime = parse_human_datetime(human_datetime)
    area = ps[4].text

    is_ad = soup.select_one('a > div > div > div').text.strip() == 'ТОП'

    return dict(
        url=url,
        title=title,
        price=price,
        district=district,
        human_datetime=human_datetime,
        datetime=datetime,
        area=area,
        is_ad=is_ad,
    )


def parse_image_src(img):
    if 'src' in img.attrs:
        return img.attrs['src']

    if 'data-src' in img.attrs:
        return img.attrs['data-src']

    return None


def parse_flat_page(soup):
    images = soup.select('.swiper-slide img')
    description = soup.select_one('[data-cy="ad_description"] div').text

    return dict(
        images=[parse_image_src(img) for img in images],
        description=description
    )

