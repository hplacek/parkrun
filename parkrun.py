# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd


from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent="parkrun")

def get_gps(address):
    #print(address)
    location = geolocator.geocode(address+', UK')
    if location is None:
        #print(address)
        latitude=90.0000 
        longitude=0
    else:
        latitude=location.latitude
        longitude=location.longitude
    return (latitude, longitude)

initial_gps= get_gps("Fulham Palace")


def get_distance(gps):
    
    return geodesic(gps, initial_gps).miles

def add_distance(df):
    df['gps']=df['address'].apply(get_gps)
    df['distance']=df['gps'].apply(get_distance)
    return df.drop(columns=['address', 'gps'])

p_list=[2,3]
for i in range(165):
    for j in [-1,1]:
        p=6*(i+1)+j
        for num in p_list:
            if (p%num)==0:
                break
        else:
            p_list.append(p)

f_list=[1,2]
while f_list[-1]<1000 :
    f_list.append(f_list[-1]+f_list[-2])
    
n_list=[]
for i in range(9):
    n_list.append(111*(i+1))
    
def unique(list1):
  
    # initialize a null list
    unique_list = []
  
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return sorted(unique_list)


henri=pd.read_html('https://www.thepowerof10.info/athletes/profile.aspx?athleteid=595763')[13]
henri_parkrun=data=henri.loc[henri[0]=='parkrun']
henri_parkrun=henri_parkrun[10].str.split(" # ", n = 1, expand = True)
henri_location=unique(list(henri_parkrun[0]))
henri_event=unique(list(henri_parkrun[1].astype('int')))


data=pd.read_html('https://www.thepowerof10.info/results/resultslookup.aspx?event=parkrun&datefrom=07-jan-2023&dateto=07-Jan-2023&terraintypecodes=A')
parkrun=data[2].loc[1:,[1,2]]
parkrun.columns=['name','address']
parkrun_temp=parkrun.loc[~parkrun['address'].str.contains(',')]
#df.loc[df['Name'].str.contains("pokemon", case=False)]
parkrun_uk=parkrun_temp['name'].str.split(" # ", n = 1, expand = True)
parkrun_uk.columns=['location','event']
parkrun_uk['event']=parkrun_uk['event'].astype('int')
parkrun_uk['address']=parkrun_temp.address

parkrun_uk=parkrun_uk.loc[parkrun_uk.apply(lambda x: x.location not in henri_location , axis=1)]
p_list=[x for x in p_list if x not in henri_event]
f_list=[x for x in f_list if x not in henri_event]
n_list=[x for x in n_list if x not in henri_event]


for i in range(3):
    parkrun_uk['event']=parkrun_uk['event'].astype('int')+1
    
    parkrun_uk_p=parkrun_uk.loc[parkrun_uk.apply(lambda x: x.event in p_list, axis=1)].copy()
    parkrun_uk_p=add_distance(parkrun_uk_p)
    parkrun_uk_p.to_csv('parkrun_p_'+str(i)+'.csv',index=False)
    
    parkrun_uk_f=parkrun_uk.loc[parkrun_uk.apply(lambda x: x.event in f_list, axis=1)].copy()
    parkrun_uk_f=add_distance(parkrun_uk_f)
    parkrun_uk_f.to_csv('parkrun_f_'+str(i)+'.csv',index=False)
    
    parkrun_uk_n=parkrun_uk.loc[parkrun_uk.apply(lambda x: x.event in n_list, axis=1)].copy()
    parkrun_uk_n=add_distance(parkrun_uk_n)
    parkrun_uk_n.to_csv('parkrun_n_'+str(i)+'.csv',index=False)
    

