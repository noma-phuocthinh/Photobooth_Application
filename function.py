import cv2
import os
from datetime import datetime

ALBUM_DIR = "Album"


def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("❌ Không thể mở camera")
    return cap


def save_shot(frame, index):
    """Lưu 1 tấm hình vào Album"""
    if not os.path.exists(ALBUM_DIR):
        os.makedirs(ALBUM_DIR)

    filename = os.path.join(
        ALBUM_DIR, f"shot_{index+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    )
    cv2.imwrite(filename, frame)
    print(f"✅ Đã lưu ảnh: {filename}")
    return filename
