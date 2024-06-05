## Search for Panoramas

# The photos on Google street view are panoramas. Each parnorama has its own
# unique ID. Retrieving photos is a two step process. First, you must translate GPS
# coordinates into panorama IDs. The following code retrieves a list of
# the closest panoramas: 51.49636418835301, -0.1988411328790174

from streetview import search_panoramas

panos = search_panoramas(lat=28.069389, lon=-26.558250)
first = panos[0]

Pid = first.pano_id

# pano_id='_R1mwpMkiqa2p0zp48EBJg' lat=41.89820676786453 lon=12.47644220919742 heading=0.8815613985061646 pitch=89.001953125 roll=0.1744659692049026 date='2019-08'

# Get Metadata

#Not all panoramas will have a `date` field in the search results. You can fetch a date for any valid panorama from the metadata api:

from streetview import get_panorama_meta

meta = get_panorama_meta(pano_id=Pid, api_key='API KEY')

print(meta)

# date='2019-08' location=Location(lat=41.89820659475458, lng=12.47644649615282) pano_id='_R1mwpMkiqa2p0zp48EBJg'

## Download streetview image

#You can then use the panorama ids to download streetview images:

from streetview import get_streetview

image = get_streetview(
    pano_id=Pid,
    api_key='API KEY',
    heading = 90,
)

image.save("image.jpg", "jpeg")

# ## Download panorama

# #You can download a full panorama like this:

# from streetview import get_panorama

# image = get_panorama(pano_id=Pid)

# image.save("image1.jpg", "jpeg")
