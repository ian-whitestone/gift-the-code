import requests


req_url='https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'
api_key = 'AIzaSyBrfDTcZ9m3FnRBN4OorWa96Ox0Xa7IHfQ'

def get_coords(addr):
    address=addr +' Toronto, Ontario, Canada'
    try:
        response = requests.get(req_url.format(address,api_key))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
            print (response_dict)
            return coords['lat'],coords['lng'],response_dict['results'][0]['formatted_address'].replace(',','')
    except Exception as err:
        print (str(err))
        pass
    return None,None,None

def get_location_data(addr):
    address=addr +' Toronto, Ontario, Canada'
    try:
        response = requests.get(req_url.format(address,api_key))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
            return response_dict['results']
    except Exception as err:
        print (str(err))
        pass
    return None

# get_coords('M4Y 1N2')
