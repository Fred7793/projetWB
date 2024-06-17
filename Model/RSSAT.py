import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import matplotlib.pyplot as plt
import pandas as pd

# Initialize the YOLO models with the pre-trained weights
Layer1 = YOLO("Model/Layer1.pt")  # Import the best model from training
Layer2 = YOLO("Model/Layer2.pt")
Layer3 = YOLO("Model/Layer3.pt")

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        initialdir="",  # Specify the initial directory
        title="Select a file",
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("all files", "*.*"))  # Specify file types
    )
    return file_path

def get_class_counts(results):
    class_counts = {}
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
    return class_counts

# Predict on an image
file_path = select_file()

if file_path:
    results1 = Layer1(file_path)
    results2 = Layer2(file_path)
    results3 = Layer3(file_path)
    
    class_counts1 = get_class_counts(results1)
    class_counts2 = get_class_counts(results2)
    class_counts3 = get_class_counts(results3)
    
    # Combine class counts from all models
    combined_class_counts = {}
    for class_counts in [class_counts1, class_counts2, class_counts3]:
        for class_name, count in class_counts.items():
            combined_class_counts[class_name] = combined_class_counts.get(class_name, 0) + count
    
    # Create DataFrame
    df = pd.DataFrame(list(combined_class_counts.items()), columns=['Class', 'Count'])
    
    # Print DataFrame
    print(df)
    
    # Display the result image from one of the models (e.g., Layer1)
    result_image = results1[0].plot()
    plt.imshow(result_image)
    plt.axis('off')  # Hide the axis
    plt.show()
else:
    print("No file selected")