# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 08:44:45 2020

@author: Nate P
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

"""URL template. Replace {} with movie title. """
rotten_tomatoes_template_url = 'https://www.rottentomatoes.com/m/{}'

"""Read in movies_df"""
movies_df = pd.read_csv(r'C:\Users\Nate P\Desktop\Disney Project\movies_df.csv')

studios = []
directors = []
ratings = []


def scrape_movie_page(response):
    """ 
    Parameter passed is a Requests package response object. Each page will have its own response object.
    """
    soup = bs(response.text, features = 'html.parser')
    for tag in soup.findAll('li','meta-row clearfix'):
        """Information regarding parental rating, Director, and Studio is available under the 'li' tag, with 'meta-row clearfix' class"""
        text = ' '.join(tag.text.split())
        if 'Rating' in text:
            """Two different regex patterns. One for ratings that have a '(', one for those without (G ratings do NOT have a parenthesis) """
            if '(' in text:
                ratings.append((re.search(r'(?<=: ).+\(', text)[0].strip('(').strip()))
            else:
                ratings.append((re.search(r'(?<=: ).+', text)[0].strip()))
        if 'Directed By' in text:
            directors.append(re.search(r'(?<=: ).+', text)[0])
        if 'Studio' in text:
            studios.append(re.search(r'(?<=: ).+', text)[0])

"""Movie titles and movie release years will be used to format url correctly"""
movie_titles = list(movies_df['Title'])
movie_release_years = list(movies_df['Release Year'])

"""looping over movie titles, creating url
Had to get creative with URL creation. Could not replace apostrophe ("'s") with blank space, creating an error with 'Avenger's' (avengers_s).
Could not replace every non letter character with '', as this messed up 'Spider-man, Far from home' (creating spiderman, not spider_man)
Decided to make non-word a space, while making "'" an empty space ('')
.split() method then splits the sentence on the blank spaces (" "), then join combines them. 
"""
root_url = 'https://www.rottentomatoes.com/m/{}'
for i, title in enumerate(movie_titles):
    # For loop goes through each movie title, then creates url out of title. 
    url = root_url.format('_'.join(re.sub(r'[:\-]',' ',title).replace('\'','').lower().split()))
    year = '_' + str(movie_release_years[i])
    #print(title)
    # If/else statement checks to see if a request is valid, specifically checking to see 'url+year' is valid
    # Reason is some movies repeat, i.e. lion king is on list twice. Would be great if every movie could be found using 'url' + 'year',
    # but unfortunately not the case. First try request that uses name + year, and if not found, moves on to just name. 
    if requests.get(url + year):
        scrape_movie_page(requests.get(url+year))
    else:
        scrape_movie_page(requests.get(url))
        

studios_df = pd.DataFrame([movie_titles, ratings, studios, directors]).T
studios_df.columns = ['Title','Ratings','Studio','Director(s)']
studios_df.to_csv(r'C:\Users\Nate P\Desktop\Disney Project\studios_df.csv', index = False)








