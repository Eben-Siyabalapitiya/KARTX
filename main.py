import cv2
import tkinter as tk
from config import CAMERA_INDEX
from src.detector import detect
from src.cart import update, handle_lost, get_cart
from src.prices import calculate, PRICES
from src.display import draw_frame

# tkinter window setup
root = tk.Tk()
root.title("KART")
root.geometry("300x500")
root.configure(bg="#0d0d0d")
root.resizable(False, False)

# title
title = tk.Label(root, text="KART", font=("Helvetica", 28, "bold"),
                 bg="#0d0d0d", fg="white")
title.pack(pady=10)

divider1 = tk.Label(root, text="─" * 30, bg="#0d0d0d", fg="#444444")
divider1.pack()

# cart items frame
cart_frame = tk.Frame(root, bg="#0d0d0d")
cart_frame.pack(fill="x", padx=20, pady=5)

divider2 = tk.Label(root, text="─" * 30, bg="#0d0d0d", fg="#444444")
divider2.pack()

# price labels
subtotal_label = tk.Label(root, text="Subtotal:   $0.00",
                          font=("Helvetica", 12), bg="#0d0d0d", fg="white")
subtotal_label.pack(pady=2)

tax_label = tk.Label(root, text="HST 13%:   $0.00",
                     font=("Helvetica", 12), bg="#0d0d0d", fg="white")
tax_label.pack(pady=2)

divider3 = tk.Label(root, text="─" * 30, bg="#0d0d0d", fg="#444444")
divider3.pack()

total_label = tk.Label(root, text="TOTAL:   $0.00",
                       font=("Helvetica", 16, "bold"), bg="#0d0d0d", fg="#00ff88")
total_label.pack(pady=10)

#update tkinter with current cart
item_labels = {}

def update_ui(cart, subtotal, tax, total):
    global item_labels

    # clear old item labels
    for widget in cart_frame.winfo_children():
        widget.destroy()
    item_labels = {}

    # add current items
    for track_id, class_name in cart.items():
        price = PRICES.get(class_name, 0.00)
        row = tk.Frame(cart_frame, bg="#0d0d0d")
        row.pack(fill="x", pady=2)

        name_lbl = tk.Label(row, text=class_name, font=("Helvetica", 11),
                            bg="#0d0d0d", fg="white", anchor="w")
        name_lbl.pack(side="left")

        price_lbl = tk.Label(row, text=f"${price:.2f}", font=("Helvetica", 11),
                             bg="#0d0d0d", fg="white", anchor="e")
        price_lbl.pack(side="right")

    subtotal_label.config(text=f"Subtotal:   ${subtotal:.2f}")
    tax_label.config(text=f"HST 13%:   ${tax:.2f}")
    total_label.config(text=f"TOTAL:   ${total:.2f}")

#main loop
cap = cv2.VideoCapture(CAMERA_INDEX)

def on_close():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

def loop():
    ret, frame = cap.read()
    if ret:
        detections = detect(frame)
        active_ids = []

        for track_id, class_name, y_center, box in detections:
            active_ids.append(track_id)
            update(track_id, class_name, y_center)

        handle_lost(active_ids)

        cart = get_cart()
        subtotal, tax, total = calculate(cart)

        # update tkinter panel
        update_ui(cart, subtotal, tax, total)

        # draw camera feed
        frame = draw_frame(frame, detections)
        cv2.imshow("KART - Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        on_close()
        return

    # call loop again after 10ms
    root.after(10, loop)

# start loop and tkinter window
loop()
root.mainloop()