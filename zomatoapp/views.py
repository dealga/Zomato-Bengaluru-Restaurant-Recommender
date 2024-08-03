from django.shortcuts import render
import pickle
from .forms import inputform  
import numpy as np

restaurant = pickle.load(open("restaurant_list.pkl", "rb"))

def index(request):
    restaurants = zip(
        restaurant["name"].values,
        restaurant["google_maps_link"].values,
        restaurant["address"].values,
        restaurant["delivery_url"].values
    )
    return render(request, 'zomatoapp/index.html', {'restaurants': restaurants})

def search_restaurant(request):
    query = request.GET.get('query', '')
    if query:
        filtered_restaurants = restaurant[restaurant["name"].str.contains(query, case=False, na=False)]
    else:
        filtered_restaurants = restaurant

    restaurants = zip(
        filtered_restaurants["name"].values,    
        filtered_restaurants["google_maps_link"].values,
        filtered_restaurants["address"].values,
        filtered_restaurants["delivery_url"].values
    )
    return render(request, 'zomatoapp/index.html', {'restaurants': restaurants})



def recommend_restaurants(request):
    form1 = inputform()
    if request.method == "POST":
        form1 = inputform(request.POST)
        if form1.is_valid():
            user_input = form1.cleaned_data['user_input']

            def recommend1(restaurant_name):
                target_tags = set(restaurant[restaurant['name'] == restaurant_name]['tags'].iloc[0].split())
                similar_restaurants = []

                for idx, row in restaurant.iterrows():
                    if row['name'] != restaurant_name:
                        similarity_score = len(target_tags.intersection(set(row['tags'].split()))) / len(target_tags.union(set(row['tags'].split())))
                        similar_restaurants.append((row['name'], similarity_score, row['google_maps_link'], row['delivery_url'], row['address']))

                similar_restaurants = sorted(similar_restaurants, key=lambda x: x[1], reverse=True)[:5]

                input_restaurant = {
                    "Name": restaurant_name,
                    "google_maps_link": restaurant[restaurant['name'] == restaurant_name]['google_maps_link'].iloc[0],
                    "delivery_url": restaurant[restaurant['name'] == restaurant_name]['delivery_url'].iloc[0]
                }

                recommended_restaurants = [
                    {
                        "Name": rest[0],
                        "google_maps_link": rest[2],
                        "delivery_url": rest[3],
                        "address": rest[4]
                    } for rest in similar_restaurants
                ]
                
                return input_restaurant, recommended_restaurants

            input_restaurant, recommended_restaurants = recommend1(user_input)

            return render(request, 'zomatoapp/recommend.html', {
                'form1': form1,
                'input_restaurant': input_restaurant,
                'recommended_restaurants': recommended_restaurants
            })

    return render(request, 'zomatoapp/recommend.html', {'form1': form1})

def contact(request):
    return render(request, 'zomatoapp/contact.html')
