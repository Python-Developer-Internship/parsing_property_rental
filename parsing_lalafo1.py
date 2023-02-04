from bs4 import BeautifulSoup
import urllib.parse
# import pandas as pd
import asyncio
import aiohttp
# pd.options.display.max_colwidth = None


URL = "https://lalafo.kg/bishkek/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir/property-host?price[to]=30000&currency=KGS&sort_by=newest"

# это функция получает данные из сайта 
async def get_html(URL: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            return await resp.text()

all_data = {'URL_INTERNAL': None,
            'title': None,
            'adress': None,
            'description': None,
            'userName': None,
            'data_create': None,
            'data_update': None,
            'price': None,
            'phone': None,
            'image_urls': None,
            'gif_name': None,
            }

async def get_content() -> list:
    soup_general = BeautifulSoup(await get_html(URL), "html.parser")
    ads = []
    for el in soup_general.select('article.adTile-wrap'):
        if el.select('.badgePaidFeature'):
            continue
        urls = urllib.parse.urljoin(URL, el.select_one('a.adTile-title')['href'])
        ads.append(urls)

    all_data['URL_INTERNAL'] = ads[0]

    soup = BeautifulSoup(await get_html(all_data['URL_INTERNAL']), "html.parser")
    items = soup.find('div', class_='details-page__wrapper container') # главный класс к которуму мы обращаемся
    all_data['title'] = (items.find('h1', class_='Heading secondary-small')
                                .text
                                )

    try:
        all_data['adress'] = (items.find('a', class_='LinkText primary-black extra-small')
                        .text
                        )
    except:
        all_data['adress'] = None

    if len(items.find('div', class_='description__wrap')
                                            .text
                                            ) == 0:
        all_data['description'] = 'Запися нету'
    else:
        all_data['description'] = (items.find('div', class_='description__wrap')
                                            .text
                                            )
                  
    all_data['userName'] = (items.find('span', class_='userName-text')
                                    .text
                                    )

    all_data['data_create'] = (items.find_all('span', class_='text-inline small')[1]
                                    .text
                                    )

    all_data['data_update'] = (items.find_all('span', class_='text-inline small')[3]
                                        .text
                                        )

    all_data['price'] = (items.find('span', class_='heading')
                                .text
                                )

    try:
        all_data['phone'] = (items.find('a', class_='linkButton medium secondary')
                                    .get('href')
                                    ).split(':')[1]
    except:
        all_data['phone'] = None

    try:
        all_data['image_urls'] = (items.find('div', class_='carousel__img-wrap')
                                    .select('source')[1]
                                    .get('srcset')
                                    )
    except:
        all_data['image_urls'] = None

    all_data['gif_name'] = (items.find('div', class_='about-ad-info__id')
                                    .text
                                    ).split(" ")[1]
    return all_data

async def main():
    data = asyncio.create_task(get_content())
    return await data


