from bs4 import BeautifulSoup
from tqdm import trange, tqdm
from typing import Tuple
import pandas as pd
import numpy as np
import requests


fields_en2ru = {
    "Country": "Страна",
    "Company": "Производитель",
    # "Platform": "Платформа",
    "Endurance": "Длительность полета, час",
    "Range": "Практическая дальность, км",
    "Payload cap.": "Полезная нагрузка, кг",
    "Max speed": "Макс. скорость, км/ч",
    "Ceiling": "Практический потолок, м",
    "Max takeoff weight": "Взлетный вес, кг",
    "Width (wingspan or rotor)": "Размах крыльев, м",
    "Length": "Длина, м"
}


countries = {
    "China": "Китай",
    "Russia": "Россия",
    "Israel": "Израиль",
    "USA": "США",
    "Canada": "Канада",
    "Brazil": "Бразилия",
    "Chile": "Чили",
    "Argentina": "Аргентина",
    "Belgium": "Бельгия",
    "Poland": "Польша",
    "Norway": "Норвегия",
    "Germany": "Германия",
    "Switzerland": "Швейцария",
    "Turkey": "Турция",
    "Austria": "Австрия",
    "Belarus": "Беларусия",
    "Netherlands": "Нидерланды",
    "Australia": "Австралия",
    "Latvia": "Латвия",
    "Czech": "Чехия",
    "Croatia": "Хорватия",
    "Finland": "Финляндия",
    "Estonia": "Эстония",
    "France": "Франция",
    "Greece": "Греция",
    "India": "Индия",
    "Iran": "Иран",
    "Italy": "Италия",
    "Japan": "Япония",
    "Malaysia": "Малайзия",
    "Mexico": "Мексика",
    "Pakistan": "Пакистан",
    "Portugal": "Португалия",
    "Romania": "Румыния",
    "Singapore": "Сингапур",
    "Sweden": "Швеция",
    "Spain": "Испания",
    "Thailand": "Тайланд",
    "UK": "Великобритания",
    "Taiwan": "Тайвань",
    "Indonesia": "Индонезия",
    "South": "Юж. Корея",
    "Slovenia": "Словения"
}


def uav_database(pages=103):
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
                     thousands: str = None,
                     translate=False):
    # Удаление ненужного
    for k in k_del:
        try:
            del data[k]
        except KeyError:
            continue
    # Обработка числовых данных
    for k in k_num:
        for ns in nan_str:
            data[k].replace(ns, np.nan, inplace=True)
        if thousands is not None:
            data[k] = data[k].str.replace(thousands, "")
        try:
            data[k] = data[k].str.replace(",", ".")
        except ValueError:
            continue
        data[k] = data[k].str.split("-", n=1, expand=True)[0]
        data[k] = data[k].str.split(" ", n=1, expand=True)[0]
        data[k] = data[k].astype(float)
    # Обработка строковых данных
    for k in k_str:
        for ns in nan_str:
            data[k].replace(ns, "н/д", inplace=True)
        data[k].fillna("н/д", inplace=True)
    if "Максимальная скорость полета, км/ч" in data:
        data["Макс. скорость, км/ч"] = data["Максимальная скорость полета, км/ч"]
        del data["Максимальная скорость полета, км/ч"]
    if translate:
        for k, v in fields_en2ru.items():
            data[v] = data[k]
            del data[k]
        for k, v in countries.items():
            d = data[data["Страна"] == k].index
            data.loc[d, "Страна"] = v
    return data


if __name__ == "__main__":
    postprocess_data(
        uav_database(),
        k_del=(
            "Метод запуска",
            "Метод посадки",
            "Навигация",
            "Диаметр несущего винта, м",
            "Диагональ рамы, м"
        ),
        k_num=(
            "Взлетный вес, кг",
            "Длительность полета, час",
            "Практическая дальность, км",
            "Практический потолок, м",
            "Размах крыльев, м",
            "Максимальная скорость полета, км/ч",
            "Полезная нагрузка, кг"
        ),
        k_str=(
            "Тип двигателя",
            "Статус",
            "Диапазон рабочих температур",
            "Производитель"
        ),
        nan_str=("", " ", "Нет данных", "Нетданных", "нет данных")
    ).to_csv("dataset_1.csv")
    
    postprocess_data(
        proliferated_drones(),
        k_del=("Photo Credit", "Platform"),
        k_num=(
            "Endurance",
            "Range",
            "Payload cap.",
            "Max speed",
            "Ceiling",
            "Max takeoff weight",
            "Width (wingspan or rotor)",
            "Length"
        ),
        k_str=("Country", "Company"),
        nan_str=("--",),
        thousands=",",
        translate=True
    ).to_csv("dataset_2.csv")
