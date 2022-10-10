
import os
import csv
import time
import matplotlib.pyplot as plt
import tkinter
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw()
from pandas import read_fwf
import os
import pandas as pd



aa= filedialog.askopenfile()
#print(aa)
df = pd.read_csv (aa.name)
print (df)

dg = df.Currentx1
aa=float((dg.nlargest(1)).values)
bb=float((dg.nsmallest(1)).values)
dg = dg.sub(aa)
#dg = df.Aimx
#print(df)


cc = aa-bb
print(aa,bb,cc)


time.sleep(5)
for col in df.columns:
    print(col)



df = df.drop(labels=0, axis=0)
dg = df[df.GVQual == 4]
dh = df[df.GVQual == 5]
ax = df.plot(kind="scatter", x="GV.startx",y="GV.starty", color="b", label="a vs. x")
#df.plot.scatter(x='GV.currentx1', y=' GV.currenty1',s=5,c="red", ax =ax)
dg.plot.scatter(x='GV.currentx1', y='GV.currenty1',s=1,c="green", ax =ax)
dh.plot.scatter(x='GV.currentx1', y='GV.currenty1',s=1,c="red", ax =ax)
df.plot.scatter(x='Aimx', y='Aimy',s=5,c="purple", ax =ax)
#df.plot(x="GV.startx", y="GV.starty",c="blue", ax =ax)

plt.show()


