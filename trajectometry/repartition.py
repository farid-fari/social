''' Permet de visualiser pour un secteur donné les répartitions. '''

import sqlite3 as sq
import seaborn as sb
import numpy as np
import matplotlib as mtpl
import matplotlib.pyplot as plt
from interface import Secteur

secteur = 102

MAP = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
       121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
       141, 142, 143, 201, 202, 203, 204, 205, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312,
       313, 314, 401, 402, 403, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515,
       516, 517, 518, 519, 601, 602, 603, 701, 801, 802, 803, 804, 805, 806, 901, 902, 903, 990]

TIMES = [0, 15, 30, 45, 100, 115, 130, 145, 200, 215, 230, 245, 300, 315, 330, 345, 400, 415, 430, 445, 500,
         515, 530, 545, 600, 615, 630, 645, 700, 715, 730, 745, 800, 815, 830, 845, 900, 915, 930, 945, 1000,
         1015, 1030, 1045, 1100, 1115, 1130, 1145, 1200, 1215, 1230, 1245, 1300, 1315, 1330, 1345, 1400, 1415,
         1430, 1445, 1500, 1515, 1530, 1545, 1600, 1615, 1630, 1645, 1700, 1715, 1730, 1745, 1800, 1815, 1830,
         1845, 1900, 1915, 1930, 1945, 2000, 2015, 2030, 2045, 2100, 2115, 2130, 2145, 2200, 2215, 2230, 2245,
         2300, 2315, 2330, 2345]

map_labels = ["101", "", "", "", "", "", "", "", "", "110", "", "", "", "", "", "", "", "", "", "120",
       "", "", "", "", "", "", "", "", "", "130", "", "", "", "", "", "", "", "", "", "140",
       "", "", "", "201", "", "", "", "", "301", "", "", "", "", "", "", "", "", "310", "", "",
       "", "", "401", "", "", "501", "", "", "", "", "", "", "", "", "510", "", "", "", "", "",
       "", "", "", "", "601", "", "603", "701", "801", "", "", "", "", "", "901", "", "", "990"]

times_labels = ["00", "", "", "", "01", "", "", "", "02", "", "", "", "03", "", "", "", "04", "", "", "", "05",
         "", "", "", "06", "", "", "", "07", "", "", "", "08", "", "", "", "09", "", "", "", "10",
         "", "", "", "11", "", "", "", "12", "", "", "", "13", "", "", "", "14",
         "", "", "", "15", "", "", "", "16", "", "", "", "17", "", "", "", "18", "", "", "",
         "19", "", "", "", "20", "", "", "", "21", "", "", "", "22", "", "", "",
         "23", "", "", "",]

conn = sq.connect('trajecto_nouv.db')
curs = conn.cursor()

sect = Secteur(curs, secteur)

data = np.zeros((98, 96))
dp = 1 / sect.nombre
for _, person in sect.people.items():
    for heure, endroit in enumerate(person.positions):
        data[MAP.index(endroit)][heure] += dp

data = np.ma.masked_equal(data, 0)
data[MAP.index(secteur)].mask = np.ones(96, dtype=bool)

plt.figure(num=1, figsize=(15, 6))
plt.subplot(1, 2, 1)

plt.title("Répartition de la population du secteur " + str(secteur))
sb.heatmap(np.ma.filled(data, 0), xticklabels=times_labels, yticklabels=map_labels, mask=data.mask, cmap=mtpl.cm.get_cmap(name="YlOrRd"))
plt.yticks(rotation=0)

plt.subplot(1, 2, 2)

plt.title("Proportion de la population du secteur " + str(secteur) + " présent dans son secteur")
plt.plot(TIMES, data.data[MAP.index(secteur)])

plt.show()

curs.close()
conn.close()
