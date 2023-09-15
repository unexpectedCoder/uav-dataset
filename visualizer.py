import seaborn as sns


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import warnings
    
    import uav_parser

    data = uav_parser.proliferated_drones()
    data = data.fillna(0.)
    data = data.where(data["Max takeoff weight"] < 50)

    warnings.filterwarnings("ignore")
    sns.set_theme(style="whitegrid")
    g = sns.relplot(
        data,
        x="Range", y="Endurance",
        hue="Payload cap.", size="Max takeoff weight",
        sizes=(20, 200),
        palette=sns.color_palette("inferno", as_cmap=True),
        facet_kws={"legend_out": True}
    )
    g.set(
        xlabel="Дальность, км",
        ylabel="Продолжительность полёта, ч",
        xscale="log"
    )
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True)
    g.despine(top=False, right=False)
    labels = ["Полезная нагрузка, кг", "Взлётная масса, кг"]
    for t in g._legend.texts:
        try:
            s = float(t.get_text())
        except ValueError:
            t.set_text(labels.pop())
    plt.show()
