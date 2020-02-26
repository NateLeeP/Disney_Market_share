# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:12:43 2020

@author: Nate P
"""

import pandas as pd
import matplotlib.pyplot as plt

movies_studios_df = pd.read_csv(r'C:\Users\Nate P\Desktop\Disney Project\movies_studios_df.csv')

x_val = movies_studios_df['Studio'].value_counts().index
y_val = movies_studios_df.groupby('Studio')['Box Office in $'].sum().sort_values(ascending = False)

fig, ax = plt.subplots()
fig.set_size_inches(15,6)
ax.bar(x_val, y_val)
ax.set_yticklabels(['${:,.0f}'.format(x) for x in ax.get_yticks()])
for i in ax.get_xticklabels():
    i.set_wrap(True)
ax.set_title('Box Office Total')

plt.show()