import os
import cv2
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
from ultralytics import YOLO
from collections import defaultdict

Layer1 = YOLO("Model/Layer1.pt")  # Import the best model from training
Layer2 = YOLO("Model/Layer2.pt")
Layer3 = YOLO("Model/Layer3.pt")
Layer4 = YOLO("Model/Layer4.pt")

def select_files():
    while True:
        user_need = int(input("\nDo you have...\n1. Only pictures\n2. Only videos\n3. Both\n\n1/2/3: ").strip().lower())
        
        if user_need == 1:
            root = tk.Tk()
            root.withdraw()
            image_paths = filedialog.askopenfilenames(title="Select image(s)", filetypes=[("All files", "*.*")])
            return user_need, list(image_paths), []

        elif user_need == 2:
            root = tk.Tk()
            root.withdraw()
            video_paths = filedialog.askopenfilenames(title="Select video(s)", filetypes=[("All files", "*.*")])
            return user_need, [], list(video_paths)
        
        elif user_need == 3:
            root = tk.Tk()
            root.withdraw()
            image_paths = filedialog.askopenfilenames(title="Select image(s)", filetypes=[("All files", "*.*")])
            video_paths = filedialog.askopenfilenames(title="Select video(s)", filetypes=[("All files", "*.*")])
            return user_need, list(image_paths), list(video_paths)

        else:
            print("\nInvalid input. Please enter '1', '2' or '3'.\n")

def process_results(results, model, all_classes, object_id_counters, frame_idx=None):
    processed = []
    
    for result in results:
        file_name = result.path
        
        for box in result.boxes:
            classe = model.names[int(box.cls)]
            confiance = box.conf.item()
            
            # Generate a unique object ID based on class
            object_id = f"{classe}_{object_id_counters[classe]}"
            object_id_counters[classe] += 1
            
            # Create an entry for the detected object
            entry = {
                "filename": file_name,
                "object_id": object_id,  # Unique ID for each object
                "class": classe,
                "confidence": confiance
            }
            if frame_idx is not None:
                entry["frame"] = frame_idx
            
            processed.append(entry)
        
    return processed

def process_videos(video_paths, models, all_classes, object_id_counters, frame_idx = 0, frame_skip = 45):
    combined_results = []
    
    for video_index, video_path in enumerate(video_paths):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video file {video_path}")
            continue
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_idx % frame_skip == 0:
                # Temporary save frame for processing
                temp_frame_path = "temp_frame.jpg"
                cv2.imwrite(temp_frame_path, frame)
                
                # Process results for each model
                processed_results = []

                for model in models:
                    results = model(temp_frame_path)
                    processed_results.append(process_results(results, model, all_classes, object_id_counters, frame_idx))
                
                # Add index and combine results for this frame
                for res in processed_results:
                    for item in res:  # Assuming process_results returns a list of results
                        item["Index"] = f"VID_{video_index}_FRAME_{frame_idx}"
                    combined_results.extend(res)
            
            frame_idx += 1
        
        cap.release()
    
    return combined_results

def process_images(image_paths, models, all_classes, object_id_counters):
    combined_results = []
    
    for image_index, image_path in enumerate(image_paths):
        # Initialize a list to store processed results for the current image
        processed_results = []
        
        # Iterate over each model and process the results
        for model in models:
            results = model(image_path)
            processed_results.append(process_results(results, model, all_classes, object_id_counters))
        
        # Add the index and combine the results for this image
        for res in processed_results:
            for item in res:  # Assuming process_results returns a list of results
                item["Index"] = f"IMG_{image_index}"
            combined_results.extend(res)
    
    return combined_results

def select_save_path(message=str):
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title=message)
    return save_path

while True:
    user_need = input("\nDo you have aerial pictures in your dataset (enter: Y) or only ground-level pictures (enter: n)?\nY/n: ").strip().lower()
    
    if user_need == "n":
        models = [Layer1, Layer2, Layer4]
        print("Initialized YOLO models for ground-level pictures.")
        break

    elif user_need == "Y":
        models = [Layer1, Layer2, Layer3, Layer4]
        print("Initialized YOLO models for a mix of ground-level and aerial pictures.")
        break 

    else:
        print("\nInvalid input. Please enter 'Y' or 'n'.\n")

RSSAT_classes = list(set([name for model in [Layer1, Layer2, Layer3, Layer4] for name in model.names.values()]))
all_classes = list(set([name for model in models for name in model.names.values()]))
formatted_results = []
object_id_counters = {classe: 1 for classe in all_classes}

scenario, image_paths, video_paths = select_files()

if scenario == 1:
    image_results = process_images(image_paths, models, all_classes, object_id_counters)
    combined_results = image_results
elif scenario == 2:
    video_results = process_videos(video_paths, models, all_classes, object_id_counters)
    combined_results = video_results
elif scenario == 3:
    image_results = process_images(image_paths, models, all_classes, object_id_counters)
    video_results = process_videos(video_paths, models, all_classes, object_id_counters)
    combined_results = image_results + video_results

# Check if the file exists before attempting to delete it
if os.path.exists('temp_frame.jpg'):
    os.remove('temp_frame.jpg')
else:
    print(f"The file 'temp_frame.jpg' does not exist.")

grouped_result_detailed = pd.DataFrame(combined_results)
grouped_result_detailed['GPS'] = '-'

# DDD
save_path = select_save_path("Save detailed unique object results")
grouped_result_detailed.to_csv(save_path, index=False)
print(f"\nSave detailed unique object results {save_path}")

new_dataframe = grouped_result_detailed.copy()
new_dataframe['index'] = new_dataframe['Index'].apply(lambda x: '_'.join(x.split('_')[:2]))
data = pd.DataFrame(columns=['index', 'class', 'count', 'avg_confidence'])
existing_classes = set(new_dataframe['class'].unique())
for idx in new_dataframe['index'].unique():
    index_df = new_dataframe[new_dataframe['index'] == idx]
    class_counts = index_df['class'].value_counts()
    avg_confidences = index_df.groupby('class')['confidence'].mean()
    
    index_data = pd.DataFrame({
        'class': class_counts.index,
        'count': class_counts.values,
        'avg_confidence': [avg_confidences.get(cls, 0) for cls in class_counts.index]
    })
    
    # Add missing classes from RSSAT_classes
    missing_classes = [cls for cls in RSSAT_classes if cls not in index_data['class'].values]
    missing_data = pd.DataFrame({
        'class': missing_classes,
        'count': 0,
        'avg_confidence': 0
    })
    
    index_data = pd.concat([index_data, missing_data], ignore_index=True)
    index_data['index'] = idx
    index_data = index_data[['index', 'class', 'count', 'avg_confidence']]
    data = pd.concat([data, index_data], ignore_index=True)

# MMM
save_path = select_save_path("Save aggregated results")
data.to_csv(save_path, index=False)
print(f"\nSave aggregated results {save_path}")

# Creating new columns based on the conditions given
data['roundabout_present'] = data.apply(lambda row: 'Present' if row['class'] == 'roundabout' and row['count'] >= 1 else 'None', axis=1)
data['grade_junction_present'] = data.apply(lambda row: 'Present' if row['class'] == 'grade-junction' and row['count'] >= 1 else 'None', axis=1)
data['signalized_junction_present'] = data.apply(lambda row: 'Present' if row['class'] == 'traffic light' and row['count'] >= 1 else 'None', axis=1)

# Checking for signalized crossing
def check_signalized_crossing(index):
    crossing_present = data[(data['index'] == index) & (data['class'] == 'crossing')]['count'].sum() >= 1
    traffic_light_present = data[(data['index'] == index) & (data['class'] == 'traffic light')]['count'].sum() >= 1
    return 'Present' if crossing_present and traffic_light_present else 'None'

data['signalized_crossing_present'] = data.apply(lambda row: check_signalized_crossing(row['index']), axis=1)
data['marked_crossing_present'] = data.apply(lambda row: 'Present' if row['class'] == 'crossing' and row['count'] >= 1 else 'None', axis=1)
data['safety_barriers_present'] = data.apply(lambda row: 'Present' if row['class'] == 'safety_bar' and row['count'] >= 5 else 'None', axis=1)
data['static_roadside_object_present'] = data.apply(lambda row: 'Present' if (row['class'] == 'pole' and row['count'] >= 1) or (row['class'] == 'tree' and row['count'] >= 1) else 'None', axis=1)
data['minor_hazards_present'] = data.apply(lambda row: 'Present' if row['class'] == 'traffic sign' and row['count'] >= 1 else 'None', axis=1)

# Checking for pedestrian facilities
def check_pedestrian_facilities(index):
    if data[(data['class'] == 'pro_sidewalk')]['count'].sum() >= 1:
        return 'Protected sidewalk'
    elif data[(data['index'] == index) & (data['class'] == 'sidewalk')]['count'].sum() >= 1:
        return 'Sidewalk'
    return 'None'

data['pedestrian_facilities'] = data.apply(lambda row: check_pedestrian_facilities(row['index']), axis=1)
data['central_hatching_present'] = data.apply(lambda row: 'Present' if row['class'] == 'central_hatch' and row['count'] >= 1 else 'None', axis=1)
data['physical_median_present'] = data.apply(lambda row: 'Present' if row['class'] == 'phy_med' and row['count'] >= 1 else 'None', axis=1)
data['safety_barrier_present'] = data.apply(lambda row: 'Present' if row['class'] == 'safety_bar' and row['count'] >= 2 else 'None', axis=1)

# Checking for bicycle facilities
def check_bicycle_facilities(index):
    if data[(data['index'] == index) & (data['class'] == 'pro_bikelane')]['count'].sum() >= 1:
        return 'Protected bikelane'
    elif data[(data['index'] == index) & (data['class'] == 'bikelane')]['count'].sum() >= 1:
        return 'Bikelane'
    return 'None'

data['bicycle_facilities'] = data.apply(lambda row: check_bicycle_facilities(row['index']), axis=1)

# Adding new column for road marking and road sign assessment
def road_marking_sign_assessment():
    relevant_classes = ['crossing', 'line1', 'arrow_st', 'traffic sign', 'arrow_st_left', 'diamond', 'arrow_right', 'slow', 'central_hatch', 'line2', 'yellowmark', 'arrow_st_right', 'bike', 'arrow_left']
    total_count = data[data['class'].isin(relevant_classes)]['count'].sum()
    unique_indices = data['index'].nunique()
    assessment_value = total_count / unique_indices

    if assessment_value < 2:
        return 'Poor'
    elif 1 <= assessment_value <= 5:
        return 'Fair'
    else:
        return 'Good'

# Creating a new column for the assessment
data['road_marking_sign_assessment'] = road_marking_sign_assessment()

# Extracting only relevant columns to match the required output format
required_data = data[['class', 'roundabout_present', 'grade_junction_present', 'signalized_junction_present', 'signalized_crossing_present', 'marked_crossing_present', 'safety_barriers_present', 'static_roadside_object_present', 'minor_hazards_present', 'pedestrian_facilities', 'central_hatching_present', 'physical_median_present', 'safety_barrier_present', 'bicycle_facilities', 'road_marking_sign_assessment']].drop_duplicates()

# Calculating the outputs
roundabout_present = 'Present' if (required_data['roundabout_present'] == 'Present').any() else 'None'
grade_junction_present = 'Present' if (required_data['grade_junction_present'] == 'Present').any() else 'None'
signalized_junction_present = 'Present' if (required_data['signalized_junction_present'] == 'Present').any() else 'None'
signalized_crossing_present = 'Present' if (required_data['signalized_crossing_present'] == 'Present').any() else 'None'
marked_crossing_present = 'Present' if (required_data['marked_crossing_present'] == 'Present').any() else 'None'
safety_barriers_present = 'Present' if (required_data['safety_barriers_present'] == 'Present').any() else 'None'
static_roadside_object_present = 'Present' if (required_data['static_roadside_object_present'] == 'Present').any() else 'None'
minor_hazards_present = 'Present' if (required_data['minor_hazards_present'] == 'Present').any() else 'None'
pedestrian_facilities = required_data['pedestrian_facilities'].max()
central_hatching_present = 'Present' if (required_data['central_hatching_present'] == 'Present').any() else 'None'
physical_median_present = 'Present' if (required_data['physical_median_present'] == 'Present').any() else 'None'
safety_barrier_present = 'Present' if (required_data['safety_barrier_present'] == 'Present').any() else 'None'
bicycle_facilities = required_data['bicycle_facilities'].max()
road_marking_sign_assessment = required_data['road_marking_sign_assessment'].max()

# Creating a table in the same style as the provided image
output_table = pd.DataFrame({
    'Requirement categories': [
        'Intersection Characteristics', 
        'Intersection Characteristics',
        'Intersection Characteristics',
        'Pedestrian Crossing',
        'Pedestrian Crossing',
        'Dominant Roadside Object',
        'Dominant Roadside Object',
        'Dominant Roadside Object',
        'Segment Characteristics',
        'Segment Characteristics',
        'Segment Characteristics',
        'Segment Characteristics',
        'Segment Characteristics',
        'Segment Characteristics'
    ],
    'Attributes': [
        'Roundabout', 
        'Grade-Junction',
        'Signalized Junction',
        'Signalized Crossing',
        'Marked Crossing',
        'Safety Barriers',
        'Static Roadside Object',
        'Minor Hazards',
        'Pedestrian Facilities',
        'Central Hatching',
        'Physical Median',
        'Safety Barrier',
        'Bicycle Facilities',
        'Road marking and Road sign'
    ],
    'Output': [
        roundabout_present, 
        grade_junction_present,
        signalized_junction_present,
        signalized_crossing_present,
        marked_crossing_present,
        safety_barriers_present,
        static_roadside_object_present,
        minor_hazards_present,
        pedestrian_facilities,
        central_hatching_present,
        physical_median_present,
        safety_barrier_present,
        bicycle_facilities,
        road_marking_sign_assessment
    ]
})

# Final RSSAT
output_csv_path = select_save_path("Save final RSSAT")
output_table.to_csv(output_csv_path, index=False)
print(f"\nSave final RSSAT {output_csv_path}")