import requests
from PIL import Image
from io import BytesIO
import pandas as pd

def get_street_view_image(lat, lon, api_key, heading=0, pitch=0, fov=90, size="640x640", radius=50):
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "location": f"{lat},{lon}",
        "size": size,
        "heading": heading,
        "pitch": pitch,
        "fov": fov,
        "radius": radius,
        "key": api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print(f"Error: {response.status_code}")
        return None

# Load the Excel file
file_path = '/Users/fredericdai/Desktop/Projet/Exceltri/ton_nouveau_fichier.xlsx'
excel_data = pd.read_excel(file_path)

# Remplacez 'YOUR_API_KEY' par votre clé API Google Street View
api_key = "api"

# Process each row in the Excel file
for index, row in excel_data.iterrows():
    lat = row['Longitude']
    lon = row['Latitude']
    direction = row['Direction']
    
    # Adjust heading based on direction
    heading = 0
    if direction == 'S':
        heading = 0
    elif direction == 'W':
        heading = 90
    elif direction == 'N':
        heading = 180
    elif direction == 'E':
        heading = 270

    # Set radius (in meters)
    radius = 50

    image = get_street_view_image(lat, lon, api_key, heading=heading, radius=radius)
    
    if image:
        # Save the image with a unique name
        image_path = f"street_view_image_{index}.jpg"
        image.save(image_path)
        print(f"Saved image for row {index} at {image_path}")
