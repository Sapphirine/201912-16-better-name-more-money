import json

from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import jitter
from django.shortcuts import render
from airbnb_analysis.modeling import myWordCloud, embedding
from geopy.geocoders import Nominatim
import joblib
import numpy as np

def index(request):
    return render(request, "index.html")


def map(request):
    # city = request.GET.get('city')
    # if city:
    data_path = './new_york.json'
    json_data = open(data_path)
    data = json.loads(json_data.read())
    ret = []
    for element in data:
        ret.append({'name': element['listing_name'],
                    'lat': element['lat'],
                    'lng': element['lng'],
                    'reviews': element['reviews_count'],
                    'prices': element['price']})
    json_data.close()
    data = json.dumps(ret)
    return render(request, "home.html", {'data': data})


def wordmap(request):
    city = request.GET.get('city')
    room_type = request.GET.get('room type')
    picture_src = None
    if city:
        data_path = './new_york.json'
        picture_src = myWordCloud.wordCloud(data_path, room_type)
    return render(request, "wordcloud.html", {'data':picture_src})


def prediction(request):
    address = request.GET.get('address')
    if address:
        name = request.GET.get('name')
        name_vec = embedding.name2Vec(name)
        geolocator = Nominatim(user_agent="airbnb analysis")
        location = geolocator.geocode(address)
        min_nights = int(request.GET.get('min_nights'))
        max_nights = int(request.GET.get('max_nights'))
        price = int(request.GET.get('price'))
        person_capacity = int(request.GET.get('person_capacity'))
        bedrooms = int(request.GET.get('bedrooms'))
        bathrooms = int(request.GET.get('bathrooms'))
        can_instant_book = request.GET.get('can_instant_book') == '1'
        is_superhost = request.GET.get('is_superhost') == '1'
        room_type_category = request.GET.get('room_type_category')
        room_type_category_entire_home = int(room_type_category == '0')
        room_type_category_hotel_room = int(room_type_category == '1')
        room_type_category_private_room = int(room_type_category == '2')
        room_type_category_shared_room = int(room_type_category == '3')
        pipe = joblib.load('./airbnb_analysis/modeling/random_forest.joblib')
        pr_list = [location.latitude, location.longitude,
                   min_nights, max_nights,
                   price, person_capacity, bedrooms, bathrooms,
                   can_instant_book, is_superhost] + list(name_vec) + \
                   [room_type_category_entire_home, room_type_category_hotel_room,
                   room_type_category_private_room, room_type_category_shared_room]
        print(pr_list)
        pr_list = np.array(pr_list).reshape(1, -1)
        result = pipe.predict(pr_list)
    else:
        result = 'Please enter the information'
    return render(request, "prediction.html", {'result': result})


def analysis(request):
    feature_name = request.GET.get('feature')
    feature_names = ["bedrooms", "bathrooms", "room_type_category"]
    data_path = './new_york.json'
    json_data = open(data_path)
    data = json.loads(json_data.read())
    prices = []
    category = []
    if not feature_name:
        feature_name = 'bedrooms'
    for element in data:
        if element[feature_name] is not None:
            prices.append(element['price'])
            category.append(element[feature_name])
    json_data.close()
    data = {'prices': prices,
            'category': category}
    source = ColumnDataSource(data=data)
    cats = list(set(category))
    cats = [str(c) for c in sorted(cats)]
    p = figure(plot_width=800, plot_height=800, y_range=cats,
               title="Rent by Category")
    p.circle(x='prices', y=jitter('category', width=0.6, range=p.y_range), alpha=0.3, source=source)
    p.x_range.range_padding = 0
    p.ygrid.grid_line_color = None
    script, div = components(p)
    return render(request, "analysis.html", {'script': script, 'div': div, 'feature_names': feature_names,
                                             "current_feature_name": feature_name})
