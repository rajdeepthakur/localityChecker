#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install bs4')
get_ipython().system('pip install urllib')
get_ipython().system('pip install json')
get_ipython().system('pip install polyline')
get_ipython().system('pip install geojson')
get_ipython().system('pip install shapely')


# In[2]:


import pandas as pd
import numpy as np
import html
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import polyline
import geojson
from shapely.geometry import shape, Point


# In[3]:


url = "https://housing.com/in/buy/bangalore/all-localities"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')


# In[4]:


localities = soup.find_all("a", class_="css-4huaz2")
for kk in range(len(localities)):
    localities[kk] = localities[kk]['href'].split("/")[-1]


# In[5]:


localityDictionary = {}
for a in range(len(localities)):
    url = "https://housing.com/in/buy/bangalore/"+localities[a]
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    ss = soup.find_all("a")
    for aaa in range(len(ss)):
        if ss[aaa].text == "Know more":
            localityDictionary[localities[a]] = ss[aaa]['href'].split("-")[-1]

for a in localityDictionary.keys():
    print(a+": "+localityDictionary[a])


# In[ ]:


# only including 1 locality for checking (need id hash map for other localities)
url = "https://mightyzeus.housing.com/api/gql/stale?isBot=false&source=web&query=query($ids:%20[String])%20{%20%20%20%20polygons(ids:%20$ids)%20{%20%20%20%20%20%20id%20%20%20%20%20%20name%20%20%20%20%20%20type%20%20%20%20%20%20polylines%20%20%20%20%20%20center%20%20%20%20}%20%20}&variables={\"ids\":[\"a273c4c3be0ee8b3669f\"]}"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
temp = polyline.decode(json.loads(str(soup))['data']['polygons'][0]['polylines'][0])
polygonDictionary = {"Whitefield": { "type": "Polygon", "coordinates": [[np.array(temp[a]) for a in range(len(temp))]]} }


#the point to check
point = Point(12.9692923597698,77.7392696661217) #this point is inside Whitefiled

# check each polygon to see if it contains the point
for polygon in polygonDictionary.keys():
    poly = shape(polygonDictionary[polygon])
    if poly.contains(point):
        print('Found containing locality: ' + polygon)
    else:
        print("Doesn't exist")


# In[ ]:




