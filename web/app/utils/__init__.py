from app import mongo
from app import config
import requests, json
from datetime import datetime,timedelta

api = config['BING_API_KEY']

def get_current_location(username):
    current_location = dict(mongo.db.current_loc.find_one({'username' : username}) )
    current_location.pop('_id')
    current_location.pop('username')

    return current_location

def get_plot_locations(data, all_locs): 

    plot_locations = []
    r = requests.post('https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key=' + api , data=json.dumps(data))

    result_list = r.json()['resourceSets'][0]['resources'][0]['results']

    for result,loc in zip(result_list , all_locs): 
        if result['travelDistance'] <= 500 and result['travelDistance'] >=0:
            plot_locations.append(loc) 

    return plot_locations 

def get_dest_list(): 

    end = datetime.now() 
    start = datetime.now() - timedelta(days = 90)

    d = datetime.today() - timedelta(hours=0, minutes=50)

    all_locations = list(mongo.db.reports.find({'date' : { '$lt' : end, '$gte' : start}}))
    
    dest_list = []
    all_locs = []
    disease_count = {}
   
    for loc in all_locations:
        if loc['place_id'] in disease_count:
            if loc['disease_name'] in disease_count[loc['place_id']]:
                disease_count[loc['place_id']][loc['disease_name']] +=1 
            else:
                disease_count[loc['place_id']][loc['disease_name']] =1  
        else: 
            disease_count[loc['place_id']] = {}
            disease_count[loc['place_id']][loc['disease_name']] = 1 
       
        temp_loc = {}
        temp_loc["latitude"] = loc.pop('lat')
        temp_loc["longitude"] = loc.pop('lng')
        dest_list.append(temp_loc)
        temp_loc['place_id'] = loc.pop('place_id')
        temp_loc['loc_name'] = loc.pop('loc_name')
        all_locs.append(temp_loc)
    
    return dest_list, disease_count, all_locs

def get_death_list(): 

    end = datetime.now() 
    start = datetime.now() - timedelta(days = 90)

    d = datetime.today() - timedelta(hours=0, minutes=50)

    all_locations = list(mongo.db.deaths.find({'date' : { '$lt' : end, '$gte' : start}}))
    
    dest_list = []
    
    disease_count = {}
    for loc in all_locations:
        if loc['place_id'] in disease_count:
            if loc['disease_name'] in disease_count[loc['place_id']]:
                disease_count[loc['place_id']][loc['disease_name']] +=1 
            else:
                disease_count[loc['place_id']][loc['disease_name']] =1  
        else: 
            disease_count[loc['place_id']] = {}
            disease_count[loc['place_id']][loc['disease_name']] = 1 
    
    return dest_list, disease_count



def poll(): 

    end = datetime.now() 
    start = datetime.now() - timedelta(days = 90)

    d = datetime.today() - timedelta(days = 30)

    diseases = list(mongo.db.reports.find({'date' : { '$lt' : end, '$gte' : start}}))
    deaths = list(mongo.db.deaths.find({'date' : { '$lt' : end, '$gte' : start}}))

    disease_count = {}

    for disease in deaths:
        if disease['place_id'] in disease_count:
            if disease['disease_name'] in disease_count[disease['place_id']]:
                disease_count[disease['place_id']][disease['disease_name']] +=1 
            else:
                disease_count[disease['place_id']][disease['disease_name']] =1  
        else: 
            disease_count[disease['place_id']] = {}
            disease_count[disease['place_id']][disease['disease_name']] = 1 

    print(disease_count)