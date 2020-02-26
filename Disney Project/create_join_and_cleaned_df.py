# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 19:49:14 2020

@author: Nate P
"""

import pandas as pd

studios_df = pd.read_csv(r'C:\Users\Nate P\Desktop\Disney Project\studios_df.csv')
movies_df = pd.read_csv(r'C:\Users\Nate P\Desktop\Disney Project\movies_df.csv')

"""Join movies_df and studios_df. Both have same index, so join method used here. """

movies_studios_df = movies_df.join(studios_df[['Ratings','Studio','Director(s)']])

""" Clean movies_studios_df. Notable issues: Director names need to be fixed. Studio names need to be fixed. Studio nameds
retitled to account for subsidiaries of major studios"""


def change_name(name):
    """
    Parameter is string of director(s) names. 
    Adjust names of directors. Same director pair, but original list has them in different orders i.e. 'Joe Russo, Anthony Russo' 
    and 'Anthony Russo, Joe Russo' are the same. 
    """   
    
    
    if 'Joe Russo' and 'Anthony Russo' in name:
        name = 'Anthony Russo, Joe Russo'
        return name
    if 'Joss Whedon' in name:
        name = 'Joss Whedon'
        return name
    if 'Jennifer Lee' and 'Chris Buck' in name:
        name = 'Chris Buck, Jennifer Lee'
        return name
    else:
        return name
    
""" Change studio names to account for studios that are a subsidiary of larger studio """
def studio_name_change(name):
    # Change the name of the studio
    if 'Disney' in name:
        name = 'Walt Disney Pictures'
        return name
    if 'Marvel' in name:
        name = 'Walt Disney Pictures'
        return name
    if 'Buena Vista' in name:
        name = 'Walt Disney Pictures'
        return name
    if 'Warner Bros.' in name:
        name = 'Warner Bros. Pictures'
        return name
    if 'New Line Cinema' in name:
        name = 'Warner Bros. Pictures'
        return name
    if 'Universal' in name:
        name = 'Universal Pictures'
        return name
    if 'Paramount' in name:
        name = 'Paramount Pictures'
        return name
    else:
        return name
   


"""Fix Director(s) column and Studio column using functions above """
movies_studios_df['Director(s)'] = movies_studios_df['Director(s)'].apply(change_name)
movies_studios_df['Studio'] = movies_studios_df['Studio'].apply(studio_name_change)


movies_studios_df.to_csv(r'C:\Users\Nate P\Desktop\Disney Project\movies_studios_df.csv', index = False)











