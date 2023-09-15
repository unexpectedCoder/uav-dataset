from bs4 import BeautifulSoup
from pandas import DataFrame
from tqdm import trange, tqdm
import numpy as np
import requests


def uav_database(pages=99):
    url_list = _get_uavs_url(pages)
    data_list = []
    for url in tqdm(url_list, "Парсинг БПЛА", colour="green"):
        page = requests.get(url)
        if (sc := page.status_code) != 200:
            raise RuntimeError(
                f"не удалось подключиться (status_code = {sc})"
            )
        soup = BeautifulSoup(page.text, "html.parser")
        tables = soup.find_all(
            "table", {"class": "woocommerce-product-attributes shop_attributes"}
        )
        for tab in tables:
            th, p = tab.find_all("th"), tab.find_all("p")
            data_list.append({h.text: p.text for h, p in zip(th, p)})
    return DataFrame(data_list)


def _get_uavs_url(pages=99):
    url_list = []
    for i in trange(pages, desc="Парсинг сайта", colour="blue"):
        url = f"https://drone-catalog.ru/test/page/{i+1}/"
        page = requests.get(url)
        if (sc := page.status_code) != 200:
            raise RuntimeError(
                f"не удалось подключиться (status_code = {sc})"
            )
        soup = BeautifulSoup(page.text, "html.parser")
        names = soup.find_all("div", {"class": "uav-name"})
        for name in names:
            for a in name.find_all("a"):
                url_list.append(a.attrs["href"])
    return url_list


def proliferated_drones():
    """Парсит базу данных с сайта
    [Proliferated Drones](https://drones.cnas.org/drones/).
    """
    url = "https://drones.cnas.org/drones/"
    page = requests.get(url, headers={"User-Agent": "XY"})
    if (sc := page.status_code) != 200:
        raise RuntimeError(
            f"не удалось подключиться (status_code = {sc})"
        )
    soup = BeautifulSoup(page.text, "html.parser")
    details = soup.find_all("div", {"class": "drone-details"})
    data_list = []
    for d in details:
        dl = d.find("dl")
        data = {
            dt.text: dd.text
            for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"))
        }
        _process_proliferated_data(data)
        data_list.append(data)
    return DataFrame(data_list)


def _process_proliferated_data(data: dict):
    # Вспомогательная функция
    for k in data:
        s: str = data[k].split()[0]
        if s == "--":
            data[k] = np.nan
            continue
        try:
            data[k] = float(s)
        except ValueError:
            continue
