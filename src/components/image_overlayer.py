from PIL import Image
from datetime import datetime
from components.pixmap_viewer import PixmapViewer
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QObject, Signal
import os
import time
from icecream import ic

class ImageOverlayer(QObject):
    overlay_image_made = Signal(str)
    def __init__(self):
        super().__init__()
        self.pixmap_viewer = PixmapViewer()
        self.home_dir = os.path.expanduser("~")
        self.save_path = self.home_dir + "/Pictures/FastPhotoCaptures/Processed"
        # print(self.save_path)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        
    def overlay_image(self, image_paths: list, coords:list, frame:str):
        # ic()
        # Load the photostrip frame (with transparency)
        frame = Image.open(frame).convert("RGBA")
        background = Image.new("RGBA", frame.size, (255, 255, 255, 0))

        # Open the three images to place behind the photostrip
        images = {}
        for i in range(0, len(image_paths)):
            img =  Image.open(image_paths[i]).convert("RGBA")

            target_width = int(coords[i]["width"])
            target_height = int(coords[i]["height"])

            original_width, original_height = img.size

            width_ratio = target_width / original_width
            height_ratio = target_height / original_height
            scaling_factor = max(width_ratio, height_ratio)

            new_width = int(original_width * scaling_factor)
            new_height = int(original_height * scaling_factor)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Center the resized image in the target box
            offset_x = int(coords[i]["x"] + (target_width - new_width) / 2)
            offset_y = int(coords[i]["y"] + (target_height - new_height) / 2)
            
            # Paste the resized image onto the background
            background.paste(resized_img, (offset_x, offset_y), resized_img)
            

        # Overlay the photostrip on top of the photos
        #change the background and frame places to change the overlay order
        final_image = Image.alpha_composite(background, frame)

        # Save or display the final image
        save_path = f"{self.save_path}/{self.current_date_time()}.png"
        final_image.save(save_path)
        time.sleep(0.5)
        self.overlay_image_made.emit(save_path)        

    def current_date_time(self,):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%y%m%d-%H%M%S")

        return formatted_time
    