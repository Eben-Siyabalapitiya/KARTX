from config import LINE_Y, GRACE_FRAMES

prev_positions = {}
grace_counter = {}
cart = {}

def update(track_id, class_name, y_center):
    if track_id in prev_positions:
        prev_y = prev_positions[track_id]

        # crossed down = entered cart
        if prev_y < LINE_Y and y_center >= LINE_Y:
            cart[track_id] = class_name
            grace_counter.pop(track_id, None)

        # crossed up = left cart
        if prev_y >= LINE_Y and y_center < LINE_Y:
            cart.pop(track_id, None)

    prev_positions[track_id] = y_center

def handle_lost(active_ids):
    for track_id in list(cart.keys()):
        if track_id not in active_ids:
            grace_counter[track_id] = grace_counter.get(track_id, 0) + 1
            if grace_counter[track_id] > GRACE_FRAMES:
                cart.pop(track_id, None)
                grace_counter.pop(track_id, None)
        else:
            grace_counter.pop(track_id, None)

def get_cart():
    return cart