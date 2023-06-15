import os
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n")


product_code = input("Please enter product code:  ")
opinions = pd.read_json(f"./opinions/{product_code}.json")

stats = {
    #'opinions_count': len(opinions),
    #'opinions_count': int(opinions.id.count()),
    "opinions_count": opinions.shape[0],
    #'pros_count':int(opinions.pros_en.count()),
    "pros_count": int(opinions.pros.astype(bool).sum()),
    "cons_count": int(opinions.cons.astype(bool).sum()),
    "average_score": opinions.stars.mean().round(2),
}
if not os.path.exists("./results"):
    os.mkdir("./results")

stars = opinions.stars.value_counts().reindex(
    list(np.arange(0.5, 5.5, 0.5)), fill_value=0
)
stars.plot.bar(color="orange")
for index, value in enumerate(stars):
    plt.text(index, value + 1, str(value), ha="center")
plt.ylim([0, max(stars.values) * 1.1])
plt.xticks(rotation=0)
plt.grid(axis="y", which="major")
plt.xlabel("number of stars")
plt.ylabel("number of opinions")
plt.title("stars frequencies")
plt.savefig(f"./results/{product_code}_barchart.png")
plt.close()
stats["stars"] = stars.to_dict()
recomendations = opinions.recomendation.value_counts(dropna=False).reindex(
    [True, False, np.nan]
)
recomendations.plot.pie(
    label="",
    labels=["Positive", "Negative", "Neutral"],
    colors=["green", "red", "lightblue"],
    autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else "",
    fontsize=10,
)
plt.title("Recomendations share")
plt.savefig(f"./results/{product_code}_piechart.png")
plt.close()
stats["recomendations"] = recomendations.to_dict()
if not os.path.exists("./stats"):
    os.mkdir("./stats")
with open(f"./stats/{product_code}.json", "w", encoding="UTF-8") as file:
    json.dump(stats, file, indent=4, ensure_ascii=False)

