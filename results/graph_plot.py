import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import stats

prefix = "sk_"
value_to_extract = "Result fitness"
folder = "pop_size"
path = "results/" + folder
confidence = 0.95
save_path = ""
x_label = "Veľkosť populácie"
y_label = "Výsledok"

if prefix == "sk_":
    color = "royalblue"
elif prefix == "eu_":
    color = "darkorange"
elif prefix == "stobga5_":
    color = "green"
else:
    print(f"Prefix {prefix} is not valid.")
    color = "red"

if value_to_extract == "Execution time":
    data_type = "_t"
elif value_to_extract == "Result fitness":
    data_type = "_r"
else:
    data_type = "_uk"


files = [f for f in os.listdir(path) if f.startswith(prefix) and f.endswith(".txt")]

def extract_number(filename):
    number_part = filename.replace(prefix, "").replace(".txt", "")
    try:
        return int(number_part)
    except ValueError:
        return float(number_part)

files = sorted(files, key=extract_number)
data = {}

for filename in files:
    with open(os.path.join(path, filename), "r") as file:
        text = file.read()

    values = [float(m.group(1)) for m in re.finditer(rf"{re.escape(value_to_extract)}: ([\d\.]+)", text)]
    
    if values:
        data[filename] = values
    else:
        print(f"No values found in {filename}.")

labels = []
means = []
errors = []
all_values = []

for filename, values in data.items():
    arr = np.array(values)
    mean = np.mean(arr)
    stdev = np.std(arr, ddof=1)
    stderr = stdev / np.sqrt(len(arr))
    
    t_value = stats.t.ppf((1 + confidence) / 2., len(arr) - 1)
    margin_of_error = t_value * stderr

    labels.append(extract_number(filename))
    means.append(mean)
    errors.append(margin_of_error)
    all_values.append(arr)

labels, means, errors, all_values = zip(*sorted(zip(labels, means, errors, all_values)))
fig, ax = plt.subplots(figsize=(8, 8))
positions = range(len(labels))

ax.boxplot(all_values, positions=positions, widths=0.5, patch_artist=True,
           boxprops=dict(facecolor="azure", color="cornflowerblue", linewidth=2),
           medianprops=dict(color="cornflowerblue", linewidth=4),
           whiskerprops=dict(color="cornflowerblue", linewidth=2),
           capprops=dict(color="cornflowerblue", linewidth=2),
           flierprops=dict(markerfacecolor="azure", markeredgecolor="cornflowerblue", markersize=8, markeredgewidth=2))

ax.errorbar(positions, means, yerr=errors, fmt="o", color="none", ecolor="black", capsize=8, capthick=2, linewidth=2)
ax.plot(positions, means, marker="o", color=color, markersize=16, linestyle="-", linewidth=5)

ax.set_xticks(positions)
ax.set_xticklabels(labels)
ax.set_xlabel(x_label, fontsize=28)
ax.set_ylabel(y_label, fontsize=28)
ax.tick_params(axis='x', labelsize=24)
ax.tick_params(axis='y', labelsize=24)
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax.grid(axis="y")

plt.tight_layout()
plt.savefig(save_path + prefix + folder + data_type, dpi=100, bbox_inches="tight", pad_inches=0.1)
plt.show()