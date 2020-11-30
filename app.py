from flask import Flask, redirect, url_for, render_template,request
import os
import json
import pandas as pd 

import pickle
import folium
# import folium
app = Flask(__name__)

# pic_folder = os.path.join('static','pics')
# app.config['UPLOAD_FOLDER'] = pic_folder


# @app.route("/")
# def home():
#     pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'second.png')
#     return render_template("index.html",user_image = pic1)

with open('imp_ohio_reviews.pkl','rb') as f:          # How to load the data from pickle
    imp_ohio_reviews = pickle.load(f)

with open('ohio_restaurants.pkl','rb') as f:
    ohio_restaurants = pickle.load(f)

ohio_categorywise = ohio_restaurants[['business_id','stars','sep_categories']]
imp_ohio_reviews = imp_ohio_reviews.merge(ohio_categorywise)

def get_popular_restaurants(df,categories_list):
    
    store_restaurants = []
    
    df_rest = pd.DataFrame(columns=ohio_restaurants.columns)
    for category in categories_list:        
        category_restaurants = df[df['sep_categories'].apply(lambda x: True if category in x else False)]
        rest_list = category_restaurants[['business_id','stars']].groupby('business_id').mean().sort_values(by=['stars'],ascending=False).index.tolist()
        df_categ = ohio_restaurants[ohio_restaurants['business_id'].apply(lambda x: True if x in rest_list else False)]
        df_rest = pd.concat([df_rest,df_categ])  
    for index,row in df_rest.iterrows():
        restaurant_details = {}
        restaurant_details['Name'] = row['name']
        restaurant_details['Address'] = row['address']
        restaurant_details['Zip Code'] = row['postal_code']
        restaurant_details['Latitude'] = row['latitude']
        restaurant_details['Longitude'] = row['longitude']
        
        restaurant_details['Category'] = row['sep_categories']
        restaurant_details['Stars'] = row['stars']
#         restaurant_details['additional_details'] = row['attributes']
        store_restaurants.append(restaurant_details)
    return sorted(store_restaurants,key = lambda x: x['Stars'],reverse=True)



@app.route("/")
def index():
    start_coords = (41.499300, -81.694400)
    folium_map = folium.Map(location=start_coords,width=1500,height=800,tiles="OpenStreetMap", zoom_start=11)
    folium_map.save('templates/map.html')
    return render_template('index.html') 

@app.route('/predict',methods = ['GET','POST'])
def predict():
    if request.method == 'GET':
        user_inputs = request.args
    elif request.method == 'POST':
        user_inputs = request.form
        
    try:
        preference1 = user_inputs.get('User1')
        preference2 = user_inputs.get('User2')
        
    except ValueError:
        return "Fill out the values!"

    lst_store = []
    preference1 = [preference1]
    preference2 = [preference2]

    # preferences_list = [preference1,preference2]
    # restaurants = get_popular_restaurants(imp_ohio_reviews,preferences_list)
    
    rest_pref1 = get_popular_restaurants(imp_ohio_reviews,preference1)
    rest_pref2 = get_popular_restaurants(imp_ohio_reviews,preference2)
    lst_prefer = [rest_pref1,rest_pref2]

    # For top 15 from either category, 30 in total
    if preference1 != preference2:
        for i in range(2):
            lst_store.extend(lst_prefer[i][:15])
    else:
        lst_store.extend(lst_prefer[0][:30])
    
    start_coords = (41.499300, -81.694400)
    folium_map = folium.Map(location=start_coords,width=1500,height=800,tiles="OpenStreetMap", zoom_start=11)
    folium_map.save('templates/.html')
    for restaurant in lst_store:
        coordinates = restaurant['Latitude'],restaurant['Longitude']
        folium.Marker(coordinates,popup=(restaurant['Name'],restaurant['Zip Code'],restaurant['Category'])).add_to(folium_map)
    folium_map.save('templates/rest.html') 
    return render_template('predict.html') 

    
    # return json.dumps(restaurants)


def get_coords(preference):
    if preference == "Indian":
        coordinates = (41.499300, -81.694400)
    return coordinates

@app.route('/map',methods = ['GET','POST'])
def map():

    start_coords = (41.499300, -81.694400)
    folium_map = folium.Map(location=start_coords, zoom_start=12)
    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run(debug = True)
