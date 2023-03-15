import requests
import csv
import json
from datetime import datetime


def collect_data():

    t_date = datetime.now().strftime('%d_%m_%Y')

    response = requests.get(url='https://www.lifetime.plus/api/analysis2')

#    with open(f'info_{t_date}.json', 'w') as file:
#        #json.dump(response.json(), file, indent=4, ensure_ascii=False)

    categories = response.json()['categories']
    result = []

    for c in categories:
        c_name = c.get('name').strip()
        c_items = c.get('items')

        for item in c_items:
            item_name = item.get('name').strip()
            item_price = item.get('price')
            item_desc = item.get('description').strip()

            if 'β' in item_desc:
                item_desc = item_desc.replace('β', 'B')
            if 'γ' in item_desc:
                item_desc = item_desc.replace('γ', 'B')

            item_wt = item.get('days')
            item_bio = item.get('biomaterial')

            result.append(
                [c_name, item_name, item_wt, item_bio, item_price, item_desc, c_items]
            )

    with open(f'result_{t_date}.xls', 'a') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Категория',
                'Анализ',
                'Биоматериал',
                'Описание',
                'Стоимость',
                'Готовность в течении',

            )
        )

        writer.writerows(
            result
        )


def main():
    collect_data()


if __name__ == '__main__':
    main()