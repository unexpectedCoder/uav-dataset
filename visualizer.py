import pandas as pd
import seaborn as sns


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings("ignore")

    data = pd.read_csv("uav_dataset.csv")
    cond = \
        (data["Полезная нагрузка, кг"] < 50) & \
        (
            (data["Статус"] == "В разработке") | \
            (data["Статус"] == "В производстве")
        )

    sns.set_theme(style="white")

    # Дальность, длительность - полезная нагрузка, общий вес
    g = sns.relplot(
        data[cond],
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Полезная нагрузка, кг", size="Взлетный вес, кг",
        sizes=(20, 200),
        palette=sns.color_palette("inferno", as_cmap=True)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(True, ls=":", c="k")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, ls=":", c="k")

    # Дальность, длительность - полезная нагрузка, скорость
    g = sns.relplot(
        data[cond],
        x="Практическая дальность, км", y="Длительность полета, час",
        size="Полезная нагрузка, кг", hue="Макс. скорость, км/ч",
        sizes=(20, 200),
        palette=sns.color_palette("inferno", as_cmap=True)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(True, ls=":", c="k")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, ls=":", c="k")
    g.despine(top=False, right=False)

    # Дальность, длительность - скорость, тип двигателя
    g = sns.relplot(
        data[cond],
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Тип двигателя", size="Макс. скорость, км/ч",
        sizes=(20, 200)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(True, ls=":", c="k")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, ls=":", c="k")
    g.despine(top=False, right=False)

    # Дальность, длительность - полезная нагрузка, тип двигателя
    g = sns.relplot(
        data[cond],
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Тип двигателя", size="Полезная нагрузка, кг",
        sizes=(20, 200)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(True, ls=":", c="k")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, ls=":", c="k")
    g.despine(top=False, right=False)

    # Дальность, длительность - скорость, категория
    g = sns.relplot(
        data[cond],
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Категория", size="Макс. скорость, км/ч",
        sizes=(20, 200)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(True, ls=":", c="k")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, ls=":", c="k")
    g.despine(top=False, right=False)

    # Дальность, длительность - полезная нагрузка, категория
    g = sns.relplot(
        data[cond],
        x="Практическая дальность, км", y="Длительность полета, час",
        hue="Категория", size="Полезная нагрузка, кг",
        sizes=(20, 200)
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log",
    )
    g.ax.xaxis.grid(True, ls=":", c="k")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, ls=":", c="k")
    g.despine(top=False, right=False)

    # В разработке, производстве и снятые по сранам
    cond2 = (data["Статус"] == "В производстве") | (data["Статус"] == "В разработке")
    df = data[cond2]
    # df0 = df.groupby(df[df["Статус"] == "Снято с производства"]["Страна"]).size().sort_values(ascending=False)
    df1 = df.groupby(df[df["Статус"] == "В производстве"]["Страна"]).size().sort_values(ascending=False)
    df2 = df.groupby(df[df["Статус"] == "В разработке"]["Страна"]).size().sort_values(ascending=False)
    # df0 = df0.to_frame(name="Количество")
    # df0["Статус"] = "Снято с производства"
    # df0["Страна"] = df0.index
    df1 = df1.to_frame(name="Количество")
    df1["Статус"] = "В производстве"
    df1["Страна"] = df1.index
    df2 = df2.to_frame(name="Количество")
    df2["Статус"] = "В разработке"
    df2["Страна"] = df2.index
    # df = pd.concat([df0, df1, df2], ignore_index=True)
    df = pd.concat([df1, df2], ignore_index=True)

    _, ax = plt.subplots()
    countries = sorted(
        list(set(df["Страна"].tolist())),
        reverse=True,
        key=lambda x: df[df["Страна"] == x]["Количество"].sum()
    )
    sns.barplot(
        df,
        x="Количество", y="Страна", hue="Статус",
        order=countries,
        dodge=False,
        ax=ax
    )
    ax.set_ylabel("")
    ax.xaxis.grid(True, zorder=-1)
    ax.legend(loc="lower right")

    plt.show()
