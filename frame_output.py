from pathlib import Path
from datetime import datetime
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("asset")
OUTPUT_DIR = "Output_Image"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def resize_and_crop(img, target_w, target_h):
    """Resize và crop ảnh để vừa khít khung (fill full)"""
    w, h = img.size
    scale = max(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = img.resize((new_w, new_h))
    start_x = (new_w - target_w) // 2
    start_y = (new_h - target_h) // 2
    cropped = resized.crop((start_x, start_y, start_x + target_w, start_y + target_h))
    return cropped


def create_photobooth_frame(images, save_path=None):
    frame = Image.open(relative_to_assets("final_frame.png")).convert("RGBA")

    SLOT_W, SLOT_H = 445, 218

    img1 = resize_and_crop(Image.open(images[0]), SLOT_W, SLOT_H)
    img2 = resize_and_crop(Image.open(images[1]), SLOT_W, SLOT_H)
    img3 = resize_and_crop(Image.open(images[2]), SLOT_W, SLOT_H)

    frame.paste(img1, (47, 142))
    frame.paste(img2, (47, 400))
    frame.paste(img3, (47, 658))

    if not Path(OUTPUT_DIR).exists():
        Path(OUTPUT_DIR).mkdir(parents=True)

    if not save_path:
        now = datetime.now()
        timestamp = now.strftime("%H%M%S_%d_%m_%Y")
        save_path = str(Path(OUTPUT_DIR) / f"photobooth_result_{timestamp}.png")

    frame.save(save_path)
    print(f"📸 Ảnh cuối đã lưu: {save_path}")
    return save_path
