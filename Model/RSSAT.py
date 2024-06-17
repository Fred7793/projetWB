import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Initialize the YOLO model with the pre-trained weights
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

# Predict on an image
file_path = select_file()

if file_path:
    results = Layer1(file_path)
    results2 = Layer2(file_path)
    results3 = Layer3(file_path)
    result_image = results[0].plot()
    result_image = results2[0].plot()
    result_image = results3[0].plot()

    # Display the result image
    plt.imshow(result_image)
    plt.axis('off')  # Hide the axis
    plt.show()
else:
    print("No file selected")