import requests

key = 'AIzaSyC3Tji10eVgL2CRMW6U8AEFggEV-jLWmBk'

def get_LatLong(address:str):
    global key
    param = {'key':key,'address':address}
    res = requests.get('https://maps.googleapis.com/maps/api/geocode/json',params=param)
    location = res.json()['results'][0]['geometry']['location']
    return location['lat'],location['lng']


