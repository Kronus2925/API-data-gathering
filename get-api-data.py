import requests
import pandas as pd
from database import Database

def main():

    url = 'https://rickandmortyapi.com/api/'

    tables = ['character','location','episode']
    
    for table in tables :
        endpoint = table
        mainlist = []
        data = main_requests(url, endpoint, 1)

        for x in range(1, get_pages(data)+1):
            if endpoint == 'character':
                mainlist.extend(get_character_values(main_requests(url, endpoint, x)))
            elif endpoint == 'location':
                mainlist.extend(get_location_values(main_requests(url, endpoint, x)))
            else:
                mainlist.extend(get_episode_values(main_requests(url, endpoint, x)))
        
        #excel_export(mainlist,endpoint)
        db = get_sql_table(endpoint, mainlist)
        get_sql_values(mainlist,db.conn, endpoint)

   
def main_requests(url, endpoint, x):
    r = requests.get(url + endpoint + f'?page={x}')
    return r.json()


def get_pages(response):
    return response['info']['pages']


def get_character_values(response):
    charlist = []
    for item in response['results']:
        char = {
            'id' : item['id'],
            'name' : item['name'],
            'status' : item['status'],
            'species' : item['species'],
            'type' : item['type'],
            'gender' : item['gender'],
            'location' : item['location']['name'],
            'number of episodes' : len(item['episode'])
        }
        charlist.append(char)
    return charlist


def get_location_values(response):
    loclist = []
    for item in response['results']:
        char = {
            'id' : item['id'],
            'name' : item['name'],
            'type' : item['type'],
            'dimension' : item['dimension']
        }
        loclist.append(char)
    return loclist


def get_episode_values(response):
    eplist = []
    for item in response['results']:
        char = {
            'id number' : item['id'],
            'name text' : item['name'],
            'release_date text' : item['air_date'],
            'episode_number text' : item['episode']
        }
        eplist.append(char)
    return eplist


def get_sql_table(endpoint, mainlist):
    all_keys = set().union(*(d.keys() for d in mainlist))
    columns = " ,".join(list(all_keys))
    db = Database('Rick and Morty')
    db.create_table(f'''CREATE TABLE {endpoint} ({columns})''')
    return db


def get_sql_values(mainlist, db, endpoint):
    df = pd.DataFrame(mainlist)
    df.to_sql(endpoint, db, if_exists='replace',index=False)

# def excel_export(mainlist, endpoint):
    
#     df = pd.DataFrame(mainlist)
#     df.to_excel(f'{endpoint}.xlsx',index=False)
    

if __name__ == '__main__':    
    main()






    #({",".join(['?' for c in list(all_keys)])})