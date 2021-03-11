import numpy as np 
import pandas as pd 
import os
import random
import json
import pickle 
import folium
from folium import plugins
from folium.plugins import HeatMap
from scipy import stats
from collections import Counter

from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired

# Reading the files
with open('rec.json', 'r') as fp:
    user_ids = json.load(fp)
with open('rec_content.json', 'r') as fp:
    store_restaurants_content = json.load(fp)
with open('zip_codes.json', 'r') as fp:
    zips = json.load(fp)

with open('restaurants.pkl','rb') as f:
    restaurants = pickle.load(f)

zip_codes = restaurants['postal_code'].unique().tolist()
locations = {item['fields']['zip']:item['fields']['geopoint'] for item in zips if item['fields']['zip'] in zip_codes}
locations['89183'] = [35.9987, -115.1593]
locations['89169'] = [36.1295, -115.1326]
locations['89178'] = [36.0457, -115.3134]
locations['89166'] = [36.3192, -115.3683]
locations['89179'] = [35.9919, -115.2555]

#functions

# approximate radius of earth in km
def distance(coord1,coord2):
    R = 6373.0
    lat1,lon1 = coord1
    lat2,lon2 = coord2
    lat1,lon1 = np.radians(lat1), np.radians(lon1)
    lat2,lon2 = np.radians(lat2), np.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    dist = R*c/1.6
    return dist

def get_restaurants_by_preference(df,categories_list):
    
    store_restaurants = []
    
    df_rest = pd.DataFrame(columns=restaurants.columns)
    for category in categories_list:        
        category_restaurants = df[df['sep_categories'].apply(lambda x: True if category in x else False)]
        rest_list = category_restaurants[['business_id','stars']].groupby('business_id').mean().sort_values(by=['stars'],ascending=False).index.tolist()
        df_categ = restaurants[restaurants['business_id'].apply(lambda x: True if x in rest_list else False)]
        df_rest = pd.concat([df_rest,df_categ])  
    for index,row in df_rest.iterrows():
        restaurant_details = {}
        restaurant_details['Name'] = row['name']
        restaurant_details['Address'] = row['address']
        restaurant_details['Zip Code'] = row['postal_code']
        restaurant_details['Latitude'] = row['latitude']
        restaurant_details['Longitude'] = row['longitude']
        
        restaurant_details['Category'] = row['sep_categories']
        restaurant_details['Topics'] = row['Topics']
        restaurant_details['Stars'] = row['stars']
#         restaurant_details['additional_details'] = row['attributes']
        store_restaurants.append(restaurant_details)
    return sorted(store_restaurants,key = lambda x: x['Stars'],reverse=True)

def get_restaurants_by_topic(df,categories_list):
    
    store_restaurants = []
    
    df_rest = pd.DataFrame(columns=restaurants.columns)
    for category in categories_list:        
        category_restaurants = df[df['Topics'].apply(lambda x: True if category in x else False)]
        rest_list = category_restaurants[['business_id','stars']].groupby('business_id').mean().sort_values(by=['stars'],ascending=False).index.tolist()
        df_categ = restaurants[restaurants['business_id'].apply(lambda x: True if x in rest_list else False)]
        df_rest = pd.concat([df_rest,df_categ])  
    for index,row in df_rest.iterrows():
        restaurant_details = {}
        restaurant_details['Name'] = row['name']
        restaurant_details['Address'] = row['address']
        restaurant_details['Zip Code'] = row['postal_code']
        restaurant_details['Latitude'] = row['latitude']
        restaurant_details['Longitude'] = row['longitude']
        
        restaurant_details['Category'] = row['sep_categories']
        restaurant_details['Topics'] = row['Topics']
        restaurant_details['Stars'] = row['stars']
#         restaurant_details['additional_details'] = row['attributes']
        store_restaurants.append(restaurant_details)
    return sorted(store_restaurants,key = lambda x: x['Stars'],reverse=True)

def get_restaurants_by_usr_id(df,usr_id):
    
    store_restaurants = []
    
    df_colab = restaurants[restaurants['business_id'].isin([item[0] for item in user_ids[usr_id]])]
    df_content = restaurants[restaurants['business_id'].isin([item for item in store_restaurants_content[usr_id]])]
    df_rest = pd.concat([df_colab,df_content])
     
    for index,row in df_rest.iterrows():
        restaurant_details = {}
        restaurant_details['Name'] = row['name']
        restaurant_details['Address'] = row['address']
        restaurant_details['Zip Code'] = row['postal_code']
        restaurant_details['Latitude'] = row['latitude']
        restaurant_details['Longitude'] = row['longitude']
        
        restaurant_details['Category'] = row['sep_categories']
        restaurant_details['Topics'] = row['Topics']
        restaurant_details['Stars'] = row['stars']
#         restaurant_details['additional_details'] = row['attributes']
        store_restaurants.append(restaurant_details)
    return sorted(store_restaurants,key = lambda x: x['Stars'],reverse=True)




categories_list = restaurants['sep_categories'].values.flatten()
categories_list = [item for sublist in categories_list for item in sublist]
categories_list = [item for item in categories_list if item not in ['Restaurants','Food']]
unique_categories = sorted(list(set(categories_list)))

topic_list = restaurants['Topics'].values.flatten()
topic_list = [item for sublist in topic_list for item in sublist]
unique_topics = sorted(list(set(topic_list)))

category_dict = Counter()
for item in categories_list:
    category_dict[item] += 1

topic_dict = Counter()
for item in topic_list:
    topic_dict[item] += 1

sorted_categories = sorted(category_dict.items(),key=lambda x: x[1],reverse=True)[:75]

class GroupForm(FlaskForm):
    preference1 = SelectField(u'Preference 1',
                            choices = [(item[0],item[0]) for item in sorted_categories])
    preference2 = SelectField(u'Preference 2',
                            choices = [(item[0],item[0]) for item in sorted_categories])
    miscellaneous = SelectField(u'Amenities',
                            choices = [(item,item) for item in unique_topics])
    zip_code = SelectField(u'Zip Code', 
                            choices = [(item,item) for item in list(map(str,sorted([int(item) for item in sorted(locations.keys())])))])
    distance = StringField('Distance (in miles)', validators = [DataRequired()])
    submit = SubmitField('Submit')


class PersonalizedForm(FlaskForm):
    user_id = SelectField(u'User ID',
                             choices = [(item,item) for item in user_ids.keys()])
    zip_code = SelectField(u'Zip Code', 
                            choices = [(item,item) for item in list(map(str,sorted([int(item) for item in sorted(locations.keys())])))])
    distance = StringField('Distance (in miles)', validators = [DataRequired()])
    submit = SubmitField('Submit')




app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/group', methods=['GET', 'POST'])
def group():
    form = GroupForm()
    if form.validate_on_submit():
        # session['preference1'] = form.preference1.data
        # session['preference2'] = form.preference2.data
        # session['miscellaneous'] = form.miscellaneous.data
        # session['zip_code'] = form.zip_code.data
        # session['distance'] = form.distance.data
        # session['ans'] = f'The results are {form.preference1.data}'
        preference1 = [form.preference1.data]
        preference2 = [form.preference2.data]
        topic = [form.miscellaneous.data]
        zip_code = form.zip_code.data
        proximity = float(form.distance.data)

        store_rest = []
        rest_pref1 = get_restaurants_by_preference(restaurants,preference1)
        rest_pref2 = get_restaurants_by_preference(restaurants,preference2)
        pref_store = [rest_pref1,rest_pref2]

        if preference1 != preference2:
            for i in range(2):
                store_rest.extend(pref_store[i][:15])
        else:
            store_rest.extend(pref_store[0][:30])
        store_rest.extend(get_restaurants_by_topic(restaurants,topic)[:15])
        store_rest = list(set(store_rest))
        store_rest = [item for item in store_rest if distance(locations[zip_code],locations[item['Zip Code']]) < proximity]
        # tiles="cartodbpositron"
        vegas_coordinates = (36.1699, -115.1398)
        folium_map = folium.Map(location=vegas_coordinates, tiles="cartodbpositron", width=1200,height=600,zoom_start=12)

        for restaurant in store_rest:
            coordinates = restaurant['Latitude'],restaurant['Longitude']
            coordinates = restaurant['Latitude'],restaurant['Longitude']
            html = f'''<strong>Name:</strong> {restaurant['Name']}<br>
            <strong>Categories:</strong> {restaurant['Category']}<br>
            <strong>Amenities:</strong> {restaurant['Topics']}<br>
            <strong>Rating:</strong> {restaurant['Stars']}
            '''

            iframe = folium.IFrame(html,
                                width=200,
                                height=200)
            popup = folium.Popup(iframe,
                                max_width=200)
            folium.Marker(coordinates,popup=popup).add_to(folium_map)  
        data = [(restaurant['Latitude'],restaurant['Longitude']) for restaurant in store_rest]
        HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(folium_map))

        folium_map.save('templates/map_group.html')


        return redirect(url_for('results_group'))
    return render_template('group.html',form=form)


@app.route('/personalized', methods=['GET', 'POST'])
def personalized():
    form = PersonalizedForm()
    if form.validate_on_submit():
        # session['user_id'] = form.user_id.data        
        # session['zip_code'] = form.zip_code.data
        # session['distance'] = form.distance.data
        user_id = form.user_id.data
        zip_code = form.zip_code.data
        proximity = float(form.distance.data)
        
        store_rest = list(set(get_restaurants_by_usr_id(restaurants,user_id)))
        store_rest = [item for item in store_rest if distance(locations[zip_code],locations[item['Zip Code']]) < proximity]
        # tiles="cartodbpositron"
        vegas_coordinates = (36.1699, -115.1398)
        folium_map = folium.Map(location=vegas_coordinates, tiles="cartodbpositron", width=1200,height=600,zoom_start=12)

        for restaurant in store_rest:
            coordinates = restaurant['Latitude'],restaurant['Longitude']
            coordinates = restaurant['Latitude'],restaurant['Longitude']
            html = f'''<strong>Name:</strong> {restaurant['Name']}<br>
            <strong>Categories:</strong> {restaurant['Category']}<br>
            <strong>Amenities:</strong> {restaurant['Topics']}<br>
            <strong>Rating:</strong> {restaurant['Stars']}
            '''

            iframe = folium.IFrame(html,
                                width=200,
                                height=200)
            popup = folium.Popup(iframe,
                                max_width=200)
            folium.Marker(coordinates,popup=popup).add_to(folium_map)  
        data = [(restaurant['Latitude'],restaurant['Longitude']) for restaurant in store_rest]
        HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(folium_map))

        folium_map.save('templates/map_personalized.html')


        return redirect(url_for('results_personalized'))
    
    return render_template('personalized.html',form=form)


@app.route('/results_group')
def results_group():
    return render_template('results_group.html')

@app.route('/results_personalized')
def results_personalized():
    return render_template('results_personalized.html')


if __name__ == '__main__':
    app.run()
