from bs4 import BeautifulSoup
from pandas import DataFrame
import numpy as np
import requests


def proliferated_drones():
    """Парсит базу данных с сайта
    [Proliferated Drones](https://drones.cnas.org/drones/).
    """
    url = "https://drones.cnas.org/drones/"
    page = requests.get(url, headers={"User-Agent": "XY"})
    if page.status_code != 200:
        raise RuntimeError(
            f"не удалось подключиться (status_code = {page.status_code})"
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


if __name__ == "__main__":
    data = proliferated_drones()
    data.to_csv("data.csv")
