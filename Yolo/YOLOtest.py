import ultralytics
from ultralytics import YOLO

# Model
model = YOLO("/Users/fredericdai/Desktop/Projet/Yolo/local_env/runs/detect/train/weights/best.pt")  # build a new model from scratch

# Use the model
results = model.train(data="/Users/fredericdai/Desktop/Projet/Yolo/config.yaml", epochs=20, device="mps")  # train the model
metrics = model.val()  # evaluate model performance on the validation set
# results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
