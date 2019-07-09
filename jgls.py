#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import os
from subprocess import *
import sys


if len(sys.argv) < 2:
    path = "./"
else:
    path = str(sys.argv[1])

orig_pwd = os.path.abspath(os.curdir)
#os.chdir(os.path.dirname(os.path.realpath(__file__)))

title="File dates"

# Run command as subprocess
def runSubp(command):
    p = Popen("exec " +command, shell=True, stdout=PIPE)
    p.wait()
    error_code = p.returncode
    out = str(p.communicate()[0])[2:-3].split('\\n')
    return out
dates = []
names = []
for x in runSubp("""ls """+path+""" -thlr --time-style=+"%Y-%m-%d %H:%M:%S" | awk '{print $6 "*" $7 " " $8 " " $9 " " $10 " " $11}'""")[1:-2]:
    if '*' in x and not x[20:].strip() == '':
        dates.append(x[:19].replace('*', ' ').strip()) 
        names.append(x[20:].strip())

print(names)
# Convert date strings (e.g. 2014-10-18) to datetime
dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]


# Choose some nice levels
levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(dates)/6)))[:len(dates)]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4))
ax.set(title="JGLS - File Date/Timeline")

markerline, stemline, baseline = ax.stem(dates, levels,
                                         linefmt="C3-", basefmt="k-",
                                         use_line_collection=True)

plt.setp(markerline, mec="k", mfc="w", zorder=3)

# Shift the markers to the baseline by replacing the y-data by zeros.
markerline.set_ydata(np.zeros(len(dates)))

# annotate lines
vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
for d, l, r, va in zip(dates, levels, names, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                textcoords="offset points", va=va, ha="right")

# format xaxis with 4 month intervals
ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y axis and spines
ax.get_yaxis().set_visible(False)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

ax.margins(y=0.1)
fig = plt.gcf()
plt.grid()

fig.set_size_inches(18.5, 10.5)
fn='./'+title+' - '+datetime.now().strftime('%Y%m%d%H%M%S')+".png"
#fig.savefig(fn, dpi=300)
plt.show()

