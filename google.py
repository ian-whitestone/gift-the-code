import request


req_url='https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'
api_key = Ugen.ConfigSectionMap('googlemaps')['key']

def get_coords(addr):
    address=addr +' Toronto, Ontario, Canada'
    try:
        response = requests.get(req_url.format(address,api_key))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
        #             print (response_dict)
            return coords['lat'],coords['lng'],response_dict['results'][0]['formatted_address'].replace(',','')
    except Exception as err:
        print (str(err))
        pass
    return None,None,None
