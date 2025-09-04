from pathlib import Path
from tkinter import Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("asset")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_ui(root):
    root.geometry("857x960")
    root.configure(bg="#B5C7A3")

    canvas = Canvas(
        root,
        bg="#B5C7A3",
        height=960,
        width=857,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Background
    image_bg = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.image_bg = image_bg
    canvas.create_image(429.0, 480.0, image=image_bg)

    # Nút click
    click_image = PhotoImage(file=relative_to_assets("click.png"))
    btn_click = Button(
        image=click_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    btn_click.image = click_image
    btn_click.place(x=562.0, y=705.0, width=274.0, height=201.0)

    # 3 ô hiển thị camera
    placeholder = PhotoImage(file=relative_to_assets("image_2.png"))
    slot1 = canvas.create_image(270.0, 253.0, image=placeholder)
    slot2 = canvas.create_image(270.0, 511.0, image=placeholder)
    slot3 = canvas.create_image(270.0, 769.0, image=placeholder)
    canvas.placeholder = placeholder  # giữ ref để reset

    # Countdown text
    text_widget = canvas.create_text(
        668.0,
        99.0,
        anchor="nw",
        text="",
        fill="#B5C7A3",
        font=("Crimson Pro Bold", -100),
        justify="center"
    )

    return canvas, text_widget, btn_click, [slot1, slot2, slot3]
