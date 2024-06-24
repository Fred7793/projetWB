import pandas as pd

# Read Excel file
file_path = 'Webscraping/Exceltri/coord_in.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Display column names to check that they are correct
print("Columns available in the file :", df.columns)

# Function for separating longitude and latitude
def split_coordinates(coordinate):
    try:
        longitude, latitude = coordinate.split(',')
        return pd.Series([float(longitude), float(latitude)])
    except Exception as e:
        return pd.Series([None, None])

# Check whether the "Coordinates" column exists in the DataFrame
if 'Coordinates' in df.columns:
    # Apply the separation function to the "Coordinates" column
    df[['Longitude', 'Latitude']] = df['Coordinates'].apply(split_coordinates)

    # Save the modified DataFrame in a new Excel file
    output_file_path = 'Webscraping/Exceltri/coord_out.xlsx'
    df.to_excel(output_file_path, index=False, engine='openpyxl')
    print("Coordinate separation completed and file saved.")
else:
    print("The 'Coordinates' column does not exist in the file. Check the column name.")
