#!/usr/bin/env python
# coding: utf-8

# In[13]:


import csv
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

hdb_resale_listings = []

with open('HDB_Resale_With_Geocoordinates.csv', newline='', encoding="utf8") as f:
    reader = csv.reader(f)
    for row in reader:
        hdb_resale_listings.append(row)
    # To Remove header    
    hdb_resale_listings_headers = hdb_resale_listings[0]
    hdb_resale_listings = hdb_resale_listings[1:]
    
for row in hdb_resale_listings:
    floor_area_sqm = row[6]
    lease_remaining = row[9]                 
    resale_price = row[10]
    longitude = row[12]
    latitude = row[13]
    
    row[6] = float(floor_area_sqm)
    
    # If lease_remaining info is of string data type
    if isinstance(lease_remaining,str):
        row[9] = int(lease_remaining[:2]) 
   
    row[10] = float(resale_price)
    
    if longitude == '':
        row[12] = 0
    else:
        row[12] = float(longitude)
        
    if latitude == '':
        row[13] = 0
    else:
        row[13] = float(latitude)

hdb_resale_df = pd.DataFrame(hdb_resale_listings, columns = hdb_resale_listings_headers)
# hdb_resale_df.head()


resale_counts_by_town = {}  # Populate this dictionary with counts

## Write your code below

for row in hdb_resale_listings:
    
    town_name = row[1]
    
    if town_name in resale_counts_by_town:        
        resale_counts_by_town[town_name] += 1    
    else:        
        resale_counts_by_town[town_name] = 1
    
sorted_resale_counts_by_town = dict(sorted(resale_counts_by_town.items(), key=lambda x:x[1], reverse=True))

resale_counts_sorted_desc = sorted_resale_counts_by_town

resale_counts_sorted_desc_town = resale_counts_sorted_desc.keys()
resale_counts_sorted_desc_town_num = resale_counts_sorted_desc.values()

fig, ax = plt.subplots()
ax.bar(resale_counts_sorted_desc_town,resale_counts_sorted_desc_town_num)
ax.set_title("Counts of Resales Flats from Jan 2017 to June 2020")
ax.set_xlabel("Town")
ax.set_ylabel("Number of Resale Flats")
ax.set_xticklabels(resale_counts_sorted_desc_town, rotation=90)

plt.show()

town_resale_value_total = {}

for row in hdb_resale_listings:
    
    resale_value = row[10]
    town_name = row[1]
    
    if town_name in town_resale_value_total:
        town_resale_value_total[town_name] += resale_value
    else:
        town_resale_value_total[town_name] = resale_value
        
town_resale_average = {}       

for town, totalresale in town_resale_value_total.items():
    
    average_resale = totalresale / resale_counts_sorted_desc[town]
    
    town_resale_average[town] = round(average_resale)

town_resale_average_town = town_resale_average.keys()
town_resale_average_town_num = town_resale_average.values()

fig, ax = plt.subplots()
ax.bar(town_resale_average_town,town_resale_average_town_num)
ax.set_title("Average Resale Value in Each Town")
ax.set_xlabel("Town")
ax.set_ylabel("Average Resale Value")
ax.set_xticklabels(town_resale_average_town, rotation=90)

plt.show()

average_resale_for_lease_year_remaining = {45: 226042, 46: 242145, 47: 246401, 48: 254636, 49: 260232, 50: 269885, 51: 296375, 52: 325913, 53: 354740, 54: 364082, 55: 366896, 56: 379482, 57: 362915, 58: 358926, 59: 361077, 60: 363807, 61: 363912, 62: 368609, 63: 386043, 64: 389136, 65: 401178, 66: 405131, 67: 409869, 68: 423459, 69: 431147, 70: 446439, 71: 488230, 72: 502543, 73: 513224, 74: 509820, 75: 485555, 76: 480516, 77: 467435, 78: 461030, 79: 457907, 80: 458187, 81: 448684, 82: 458495, 83: 452845, 84: 457780, 85: 475330, 86: 539646, 87: 572114, 88: 563815, 89: 536062, 90: 639708, 91: 596058, 92: 579430, 93: 521120, 94: 453963, 95: 451161, 96: 679590}

lease = list(average_resale_for_lease_year_remaining.keys())
average_resale_value = list(average_resale_for_lease_year_remaining.values())

fig , ax = plt.subplots()
ax.plot(lease, average_resale_value, marker="D")
ax.set_title("Average Resale Value for Lease Years Remaining")
ax.set_xlabel("Lease Remaining")
ax.set_ylabel("Resale Value")

plt.show()

def extract_column(the_list, column_number):
    
    column = []
    
    for row in the_list:
        column.append(row[column_number])
    
    return column
    
floor_area_sqm_list = extract_column(hdb_resale_listings, 6)
resale_price = extract_column(hdb_resale_listings, 10)

fig, ax = plt.subplots(figsize=(18,12))

ax.scatter(floor_area_sqm_list,resale_price)
ax.set_title("Average Resale Value for Lease Years Remaining")
ax.set_xlabel("Floor Area (in square meters)")
ax.set_ylabel("Sale Price (in millions SGD)")

plt.show()

map_folium = folium.Map(location=[1.357,103.826], height=550, width=900, zoom_start=11.5)

marker_cluster = MarkerCluster().add_to(map_folium)

listing_price = []
lat_and_long = []

for row in hdb_resale_listings:
    lat_and_long.append([row[-1], row[-2]])
    listing_price.append(row[-4])


for i in range(0,len(lat_and_long)):
    lat_long_one_listing = lat_and_long[i]
    pop_display_price = '$'+ str(listing_price[i])
    
    
    folium.Marker(
        location=lat_long_one_listing,
        popup=pop_display_price,
        icon=None,
    ).add_to(marker_cluster)

display(map_folium)


# In[ ]:




