import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


plt.style.use("sciart.mplstyle")


def clear_data(data: pd.DataFrame):
    try:
        data = data[data["Тип двигателя"] != "н/д"]
    except KeyError:
        pass
    data = data[~np.isnan(data["Практическая дальность, км"])]
    data = data[~np.isnan(data["Длительность полета, час"])]
    data = data[data["Длительность полета, час"] < 24]
    data = data[~np.isnan(data["Взлетный вес, кг"])]
    return data


def drop_outliers(data: pd.DataFrame):
    d = data["Практическая дальность, км"] / data["Длительность полета, час"]
    q1 = d.quantile(0.25)
    q3 = d.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    out_indeces = np.where((d <= lower) | (d >= upper))[0]
    return data.drop(index=d.iloc[out_indeces].index)


def range_endurance_capacity_weight(data: pd.DataFrame, **kw):
    """Дальность, длительность - полезная нагрузка, общий вес."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Полезная нагрузка, кг", size="Взлетный вес, кг",
        sizes=(50, 250),
        palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полета, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_capacity_weight.__name__ + kw.get("suffix", ""))


def range_endurance_capacity_speed(data, **kw):
    """Дальность, длительность - полезная нагрузка, скорость."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        size="Полезная нагрузка, кг", hue="Макс. скорость, км/ч",
        sizes=(50, 250),
        palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_capacity_speed.__name__ + kw.get("suffix", ""))


def range_endurance_speed_engine(data: pd.DataFrame, **kw):
    """Дальность, длительность - скорость, тип двигателя."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Тип двигателя", size="Макс. скорость, км/ч",
        sizes=(20, 200)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_speed_engine.__name__ + kw.get("suffix", ""))


def range_endurance_capacity_engine(data: pd.DataFrame, **kw):
    """Дальность, длительность - полезная нагрузка, тип двигателя."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Тип двигателя", size="Полезная нагрузка, кг",
        sizes=(50, 250)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_capacity_engine.__name__ + kw.get("suffix", ""))


def range_endurance_speed_kind(data: pd.DataFrame, **kw):
    """Дальность, длительность - скорость, категория."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Категория", size="Макс. скорость, км/ч",
        sizes=(50, 250)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_speed_kind.__name__ + kw.get("suffix", ""))


def range_endurance_capacity_kind(data: pd.DataFrame, **kw):
    """Дальность, длительность - полезная нагрузка, категория."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Категория", size="Полезная нагрузка, кг",
        sizes=(50, 250)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_capacity_kind.__name__ + kw.get("suffix", ""))


def hist_desing_manufactoring(data: pd.DataFrame, limit=-1, **kw):
    """В разработке, производстве и снятые по сранам."""
    cond2 = (data["Статус"] == "В производстве") | (data["Статус"] == "В разработке")
    df = data[cond2]
    df1 = df.groupby(df[df["Статус"] == "В производстве"]["Страна"]).size().sort_values(ascending=False)
    df2 = df.groupby(df[df["Статус"] == "В разработке"]["Страна"]).size().sort_values(ascending=False)
    df1 = df1.to_frame(name="Количество")
    df1["Статус"] = "В производстве"
    df1["Страна"] = df1.index
    df2 = df2.to_frame(name="Количество")
    df2["Статус"] = "В разработке"
    df2["Страна"] = df2.index
    df = pd.concat([df1, df2], ignore_index=True)
    if limit > 0:
        countries = sorted(
            list(set(df["Страна"].tolist())),
            reverse=True,
            key=lambda x: df[df["Страна"] == x]["Количество"].sum()
        )[:limit]
    else:
        countries = sorted(
            list(set(df["Страна"].tolist())),
            reverse=True,
            key=lambda x: df[df["Страна"] == x]["Количество"].sum()
        )

    _, ax = plt.subplots(figsize=(10.2, 6.2))
    sns.barplot(
        df,
        x="Количество", y="Страна", hue="Статус",
        order=countries,
        dodge=False,
        ax=ax
    )
    ax.set_ylabel("")
    ax.legend(loc="lower right")
    plt.savefig(hist_desing_manufactoring.__name__ + kw.get("suffix", ""))


def range_endurance_size(data: pd.DataFrame, **kw):
    """Дальность, продолжительность, размер (площадь)."""
    data = drop_outliers(data)
    g = sns.relplot(
        data,
        x="Практическая дальность, км", y="Длительность полета, час",
        size="Размах крыльев, м",
        sizes=(100, 300)
        # palette=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(False)
    g.ax.yaxis.grid(False)
    g.despine(top=False, right=False)
    plt.savefig(range_endurance_size.__name__ + kw.get("suffix", ""))


def hist_countries(data: pd.DataFrame, limit=-1, **kw):
    """По сранам."""
    d = data.groupby(data["Страна"]).size().sort_values(ascending=False)
    d = d.to_frame(name="Количество")
    d["Страна"] = d.index
    if limit > 0:
        countries = sorted(
            list(set(d["Страна"].tolist())),
            reverse=True,
            key=lambda x: d[d["Страна"] == x]["Количество"].sum()
        )[:limit]
    else:
        countries = sorted(
            list(set(d["Страна"].tolist())),
            reverse=True,
            key=lambda x: d[d["Страна"] == x]["Количество"].sum()
        )

    _, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        d,
        x="Количество", y="Страна",
        color="#3274a1",
        order=countries,
        dodge=False,
        ax=ax
    )
    ax.set_ylabel("")
    plt.savefig(hist_countries.__name__ + kw.get("suffix", ""))


if __name__ == "__main__":
    def uav_dataset(limit=-1, **kw):
        full_data = pd.read_csv("dataset_1.csv")
        data = clear_data(full_data)
        cond = \
            (data["Полезная нагрузка, кг"] < 10) & \
            (
                (data["Статус"] == "В разработке") | \
                (data["Статус"] == "В производстве")
            )
        range_endurance_capacity_weight(data[cond], **kw)
        range_endurance_capacity_speed(data[cond], **kw)
        range_endurance_speed_engine(data[cond], **kw)
        range_endurance_capacity_engine(data[cond], **kw)
        range_endurance_speed_kind(data[cond], **kw)
        range_endurance_size(data[cond], **kw)
        hist_desing_manufactoring(full_data, limit=limit, **kw)

    def proliferated_dataset(limit=-1, **kw):
        full_data = pd.read_csv("dataset_2.csv")
        data = clear_data(full_data)
        cond = data["Полезная нагрузка, кг"] < 10
        range_endurance_capacity_weight(data[cond], **kw)
        range_endurance_capacity_speed(data[cond], **kw)
        range_endurance_size(data[cond], **kw)
        hist_countries(full_data, limit=limit, **kw)
    
    suff = input("Суффикс к именам файлов: ")
    uav_dataset(limit=20, suffix="_1" + suff)
    proliferated_dataset(limit=20, suffix="_2" + suff)
