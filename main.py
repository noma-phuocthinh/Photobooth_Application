import tkinter as tk
import cv2
from PIL import Image, ImageTk
from frame import create_ui
from function import open_camera, save_shot
from frame_output import create_photobooth_frame


def resize_and_crop(frame, target_w, target_h):
    h, w = frame.shape[:2]
    scale = max(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h))
    start_x = (new_w - target_w) // 2
    start_y = (new_h - target_h) // 2
    cropped = resized[start_y:start_y + target_h, start_x:start_x + target_w]
    return cropped


def main():
    root = tk.Tk()
    root.title("Photobooth")

    canvas, text_widget, btn_click, image_slots = create_ui(root)

    cap = open_camera()

    current_slot = [0]
    captured_files = []

    SLOT_W, SLOT_H = 445, 218

    def update_camera():
        if current_slot[0] < 3:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = resize_and_crop(frame, SLOT_W, SLOT_H)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                slot_id = image_slots[current_slot[0]]
                canvas.itemconfig(slot_id, image=imgtk)
                canvas.imgtk = imgtk
        root.after(30, update_camera)

    update_camera()

    def reset_photobooth():
        """Reset lại UI để chụp tiếp"""
        for slot_id in image_slots:
            canvas.itemconfig(slot_id, image=canvas.placeholder)
        canvas.itemconfig(text_widget, text="")
        captured_files.clear()
        current_slot[0] = 0

    def countdown_and_shoot(i=0, t=5):
        if t >= 0:
            canvas.itemconfig(text_widget, text=str(t))
            root.after(1000, countdown_and_shoot, i, t - 1)
        else:
            ret, frame = cap.read()
            if ret:
                file = save_shot(frame, i)
                captured_files.append(file)

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = resize_and_crop(img, SLOT_W, SLOT_H)
                pil_img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=pil_img)
                canvas.itemconfig(image_slots[i], image=imgtk)
                canvas.image_refs = getattr(canvas, "image_refs", []) + [imgtk]

            canvas.itemconfig(text_widget, text="")

            current_slot[0] += 1
            if current_slot[0] < 3:
                root.after(1000, countdown_and_shoot, i + 1, 5)
            else:
                final_path = create_photobooth_frame(captured_files)
                print(f"✅ Photobooth đã tạo: {final_path}")
                canvas.itemconfig(text_widget, text="")
                root.after(3000, reset_photobooth)  # reset sau 3s

    def on_click():
        if current_slot[0] == 0:
            countdown_and_shoot(0, 5)

    btn_click.config(command=on_click)

    root.mainloop()
    cap.release()


if __name__ == "__main__":
    main()
