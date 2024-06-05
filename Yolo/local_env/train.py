from ultralytics import YOLO

model = YOLO('yolov8m.yaml')  # load a pretrained model (recommended for training)

model.train(data='/Users/fredericdai/Desktop/Projet/Yolo/config.yaml',epochs=100)
# Evaluate the model's performance on the validation set
results = model.val()
