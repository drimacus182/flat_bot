import requests
from bs4 import BeautifulSoup
from parsers import parse_card, parse_flat_page

LISTING_URL = "https://www.olx.ua/d/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/" \
              "?search%5Bdistrict_id%5D={district_id}" \
              "&search%5Border%5D=created_at%3Adesc" \
              "&search%5Bfilter_float_price%3Ato%5D={max_price}" \
              "&search%5Bfilter_enum_number_of_rooms_string%5D%5B0%5D=odnokomnatnye" \
              "&currency=UAH" \
              "&view=grid"


class Api:
    def get_list(self, district_id, max_price, page=1):
        url = LISTING_URL.format(district_id=district_id, max_price=max_price)

        if page != 1:
            url += '&page=' + str(page)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        main_grid = soup.select_one('[data-testid="listing-grid"]')
        cards = main_grid.select('[data-cy=l-card]')
        return [parse_card(card) for card in cards]

    def get_flat(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return parse_flat_page(soup)


if __name__ == '__main__':
    api = Api()

    flats = api.get_list(19, 1000)
    for f in flats:
        flat = api.get_flat(f['url'])

        print(flat)
