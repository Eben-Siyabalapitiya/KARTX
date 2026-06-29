import cv2
from config import CAMERA_INDEX
from src.detector import detect
from src.cart import update, handle_lost, get_cart
from src.prices import calculate
from src.display import draw

cap = cv2.VideoCapture(CAMERA_INDEX)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect(frame)
    active_ids = []

    for track_id, class_name, y_center, box in detections:
        active_ids.append(track_id)
        update(track_id, class_name, y_center)

    handle_lost(active_ids)

    cart = get_cart()
    subtotal, tax, total = calculate(cart)
    frame = draw(frame, cart, subtotal, tax, total)

    cv2.imshow("KART", frame)

    if cv2.waitKey(1) & 0xFF == ord("z"):
        break

cap.release()
cv2.destroyAllWindows()