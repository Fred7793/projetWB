from ultralytics import YOLO

model = YOLO('yolov8m.yaml')  # load a pretrained model (recommended for training)

model.train(data='Model/Yolo/config_layer1.yaml',epochs=1)

results = model.val()