from ultralytics import YOLO

# model = YOLO('yolov8m.yaml')                                                      #from scratch
model = YOLO("runs/detect/train/weights/best.pt")                                   #import best one from training

# results = model.train(data="Model/config_layer1.yaml", epochs=1, device="mps")    #train the model
# metrics = model.val()

# predict on an image
results = model("Database/DataLayer1/images/train/000febf5a81b5f6d.jpg")