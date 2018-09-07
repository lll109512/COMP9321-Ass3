import requests
from app import db
from app.models import Universities, Geo_info

key = 'AIzaSyC3Tji10eVgL2CRMW6U8AEFggEV-jLWmBk'


def get_LatLng(address: str):
    global key
    param = {'key': key, 'address': address}
    res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=param)
    location = res.json()['results'][0]['geometry']['location']
    return location['lat'], location['lng']


def get_List_LatLng(addresses):
    coordinates = []
    for address in addresses:
        lat, lng = get_LatLng(address)
        coordinates.append({'latlng': [lat, lng], 'address': address})
    return coordinates


def get_all_coordinates_from_db():
    coordinates = []
    for uni, geo in db.session.query(Universities, Geo_info).filter(Universities.id == Geo_info.uni_id).all():
        coordinates.append({'latlng': [geo.lat, geo.lng], 'address': uni.name})
    return coordinates


def get_coordinates_by_uni(uni):
    uni, geo = db.session.query(Universities, Geo_info).filter(
        Universities.id == Geo_info.uni_id).filter(Universities.name == uni).first()
    return geo.lat, geo.lng


def insert_geo_data():
    for uni in Universities.query.all():
        lat, lng = get_LatLng(uni.name)
        uni.geo_info.append(Geo_info(lat=lat, lng=lng))
    db.session.commit()
