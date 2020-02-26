# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 13:22:31 2020

@author: Nate P
"""

"""
Code used to scrape Top 50 Highest-Grossing Movies off Rotten Tomato. 
"""
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd


"""
URL is link to Top 50 highest-grossing movies. 
"""
url = 'https://editorial.rottentomatoes.com/article/highest-grossing-movies-all-time/'
top_50_request = requests.get(url).text
top_50_soup = bs(top_50_request, features = 'html.parser')

"""
h2 Tag cotains everything I want, from the box office amount to the title of the movie. However, it goes every other. Meaning,
one h2 will have the title, the following h2 tag will have the box office gross
"""

"""
Collect h2 text in a list
Remove blank line. Blank line occurs ~ movie 19 or 20. Note: Issues before where blank lines disrupt the 'every other' pattern.
"""
h2_list = [h2.text for h2 in top_50_soup.findAll('h2')[2:104] if h2.text != '']
"""
Box Office Revenue. Remember, h2 tags have 'Revenue, Movie, Revenue, Movie' pattern, with box office revenue appearing first
"""
movie_box_office = h2_list[:len(h2_list):2][:50]
movie_titles = h2_list[1:len(h2_list):2][:50]

"""
Using regular expressions, extract the numerical value of the box office gross. Remove preceding '$'
"""
movie_box_office_pattern = re.compile(r'\$[\d\.]+')
box_office_numerical = []
for box_office in movie_box_office:
    """Store box office value to check if value is million or billion (millions will begin with a 9)"""
    temp1 = movie_box_office_pattern.search(box_office)[0].strip('$')
    if temp1.startswith('9'):
        """If number in the millions, covert to numerical by multiplying by 1,000,000"""
        temp1 = float(temp1) * 1000000
    else:
         """ If number in the billion, covert to numerical by multiplying by 1,000,000,000 """
         temp1 = float(temp1) * 1000000000
    
    box_office_numerical.append(round(temp1))
    
"""
Using regular expressions, extract the Ttile, Year, and Rotten Tomato score
"""
movie_title_only = []
movie_year = []
movie_score = []
for movie in movie_titles:
    movie_title_only.append(re.search(r'[\w: \-\']+',movie)[0].strip(' '))
    """Regular expression matches any word character, the ':' character, then any '-' or parenthesis. """
    movie_year.append(re.search(r'[0-9]{4}', movie)[0])
    movie_score.append(re.search(r' [0-9]{2}', movie)[0].strip(' '))

"""Create a dataframe containing the movie title, the box office gross, release year, and rotten tomato score. Save to df."""
movie_df = pd.DataFrame([movie_title_only, box_office_numerical, movie_year, movie_score]).T
movie_df.columns = ['Title','Box Office in $', 'Release Year','Rotten Score']
movie_df.to_csv('movies_df.csv', index = False) 






    
    
    