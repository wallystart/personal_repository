import ee
from ee import oauth
from google.oauth2.credentials import Credentials


def get_elevation(lat, lon):
  p = ee.Geometry.Point(lon, lat)

  image = ee.Image('USGS/SRTMGL1_003')
  dataN = image.select('elevation').reduceRegion(ee.Reducer.first(), p).get("elevation")
  dataN = ee.Number(dataN)
  return dataN.getInfo()

def initialize_gee():
    # Create Oatuh credentials by using a hardcoding token
    hard_creds = {"refresh_token": "TOKEN"}
    credentials = Credentials(None,
                            refresh_token=hard_creds['refresh_token'],
                            token_uri=oauth.TOKEN_URI,
                            client_id=oauth.CLIENT_ID,
                            client_secret=oauth.CLIENT_SECRET,
                            scopes=oauth.SCOPES)

    # Initiliaze Earth Engine 
    ee.Initialize(credentials=credentials)
    #print('The Earth Engine package initialized successfully!')
    
    return True
