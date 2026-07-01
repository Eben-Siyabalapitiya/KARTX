from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE

model = YOLO(MODEL_PATH)

def detect(frame):
    results = model.track(frame, persist=True, conf=CONFIDENCE)
    detections = []

    if results[0].boxes.id is None:
        return detections

    boxes = results[0].boxes.xyxy.cpu().numpy()
    ids = results[0].boxes.id.cpu().numpy().astype(int)
    classes = results[0].boxes.cls.cpu().numpy().astype(int)
    names = results[0].names

    for box, track_id, cls in zip(boxes, ids, classes):
        x1, y1, x2, y2 = box
        y_center = (y1 + y2) / 2
        class_name = names[cls]
        detections.append((track_id, class_name, y_center, box))

    return detections