#Train own model

import ultralytics
from ultralytics import YOLO

# Model
model = YOLO("yolov8n.yaml")  # build a new model from scratch 
# 'n' stands for nano, meaning you can choose the size of your model, 's': small, 'm': medium, 'l': large, 'x': extra large
# add -seg for segmentation training
# more information on : https://docs.ultralytics.com/quickstart/#understanding-settings 

# Use the model
results = model.train(data="/Path/to/config.yaml", epochs=X)  # train the model
metrics = model.val()  # evaluate model performance on the validation set

