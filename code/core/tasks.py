import os
from django.conf import settings

from celery import shared_task
from PIL import Image

@shared_task
def create_thumbnails(file_path, sizes=[]):
    os.chdir(settings.IMAGES_DIR)
    path, file = os.path.split(file_path)
    file_name, ext = os.path.splitext(file)

    results = {'resized_image_path': f"{settings.MEDIA_URL}images/{file_name}.thumbnail.png"}
    for new_size in sizes:
        try:
            with Image.open(file_path) as img:
                # Square center crop
                img_width, img_height = img.size
                img_diff = abs(img_width - img_height)
                if img_width < img_height:
                    img = img.crop(0, (img_height - img_diff) // 2, img_width, (img_height + img_diff) // 2)
                else:
                    img = img.crop((img_width - img_diff) // 2, 0, (img_height + img_diff) // 2, img_height)

                # Resize then save
                img.thumbnail(new_size)
                img.save(file_name + ".thumbnail.png", "PNG")
        except IOError as error:
            print(error)
        return results