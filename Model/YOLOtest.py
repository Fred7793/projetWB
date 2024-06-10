import ultralytics
from ultralytics import YOLO

# Model
model = YOLO("runs/detect/train/weights/best.pt")  # build a new model from scratch

#results = model.train(data="Model/config_layer1.yaml", epochs=1, device="mps")  # train the model
# evaluate model performance on the validation set
# metrics = model.val()

# predict on an image
results = model("Database/DataLayer1/images/train/000febf5a81b5f6d.jpg")