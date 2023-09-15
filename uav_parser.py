from bs4 import BeautifulSoup
from tqdm import trange, tqdm
from typing import Tuple
import pandas as pd
import numpy as np
import requests


def uav_database(pages=99):
    """Парсит данные с сайта [Drone Catalog](https://drone-catalog.ru/)."""
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
    return pd.DataFrame(data_list)


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
    for d in tqdm(details, "Парсинг", colour="yellow"):
        dl = d.find("dl")
        data = {
            dt.text: dd.text
            for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"))
        }
        for k in data:
            data[k] = data[k].split()[0]
        data_list.append(data)
    return pd.DataFrame(data_list)


def postprocess_data(data: pd.DataFrame,
                     k_del: Tuple[str, ...] = tuple(),
                     k_num: Tuple[str, ...] = tuple(),
                     k_str: Tuple[str, ...] = tuple(),
                     nan_str: Tuple[str, ...] = tuple(),
                     thousands: str = None):
    # Удаление ненужного
    for k in k_del:
        del data[k]
    # Обработка числовых данных
    for k in k_num:
        for ns in nan_str:
            data[k].replace(ns, np.nan, inplace=True)
        if thousands is not None:
            data[k] = data[k].str.replace(thousands, "").astype(float)
        if data[k].dtype == "str":
            data[k] = data[k].str.replace(",", ".").astype(float)
    # Обработка строковых данных
    for k in k_str:
        for ns in nan_str:
            data[k].replace(ns, "н/д", inplace=True)
        data[k].fillna("н/д", inplace=True)
    return data
