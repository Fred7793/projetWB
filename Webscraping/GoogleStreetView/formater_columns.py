import pandas as pd

# Lire le fichier Excel
file_path = 'Webscraping/Exceltri/coord_in.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Afficher les noms des colonnes pour vérifier le nom correct
print("Colonnes disponibles dans le fichier :", df.columns)

# Fonction pour séparer la longitude et la latitude
def split_coordinates(coordinate):
    try:
        longitude, latitude = coordinate.split(',')
        return pd.Series([float(longitude), float(latitude)])
    except Exception as e:
        return pd.Series([None, None])

# Vérifier si la colonne "Coordinates" existe dans le DataFrame
if 'Coordinates' in df.columns:
    # Appliquer la fonction de séparation à la colonne "Coordinates"
    df[['Longitude', 'Latitude']] = df['Coordinates'].apply(split_coordinates)

    # Sauvegarder le DataFrame modifié dans un nouveau fichier Excel
    output_file_path = 'Webscraping/Exceltri/coord_out.xlsx'
    df.to_excel(output_file_path, index=False, engine='openpyxl')
    print("Séparation des coordonnées terminée et fichier sauvegardé.")
else:
    print("La colonne 'Coordinates' n'existe pas dans le fichier. Vérifiez le nom de la colonne.")