from io import StringIO, BytesIO
from PIL import Image
from django.core.files.base import ContentFile


# 프로필이미지 커스텀
def profile_image_resizing(content_file, margin):
    img = Image.open(content_file)
    # img = img.convert("RGB")
    img_io = BytesIO()
    if margin[0] == 'x':
        size = float(margin[1:]) * 0.01
        height = img.height
        width = img.width

        if height > 200:
            rescale_height = height - 200
            rescale_ratio = rescale_height/height
            img.thumbnail((int(width - width * rescale_ratio), 200))
            area = (int(200 * size), 0, int(200 * size) + 200, 200)
            img = img.crop(area)
            img.resize((200, 200), Image.HAMMING)
            img.save(img_io, format='JPEG', quality=70)
            img_content = ContentFile(img_io.getvalue(), 'profile.jpeg')
            return img_content
        elif height == 200:
            area = (int(200 * size), 0, int(200 * size) + 200, 200)
            img.crop(area)
            img = img.crop(area)
            img.save(img_io, format='JPEG', quality=70)
            img_content = ContentFile(img_io.getvalue(), 'profile.jpeg')
            return img_content
        else:
            rescale_ratio = 200/height
            img.thumbnail((int(width * rescale_ratio), 200), Image.ANTIALIAS)
            area = (int(200 * size), 0, int(200 * size) + 200, 200)
            img.crop(area)
            img = img.crop(area)
            img.save(img_io, format='JPEG', quality=70)
            img_content = ContentFile(img_io.getvalue(), 'profile.jpeg')
            return img_content

    else:
        size = float(margin[1:]) * 0.01
        height = img.height
        width = img.width

        if width > 200:
            rescale_width = width - 200
            rescale_ratio = rescale_width / height
            img.thumbnail((200, int(height - height * rescale_ratio)))
            area = (0, int(200 * size), 200, int(200 * size) + 200)
            img = img.crop(area)
            img.save(img_io, format='JPEG', quality=70)
            img_content = ContentFile(img_io.getvalue(), 'profile.jpeg')
            return img_content
        elif width == 200:
            area = (0, int(200 * size), 200, int(200 * size) + 200)
            img.crop(area)
            img = img.crop(area)
            img.save(img_io, format='JPEG', quality=70)
            img_content = ContentFile(img_io.getvalue(), 'profile.jpeg')
            return img_content
        else:
            rescale_ratio = 200 / width
            img.thumbnail((200, int(height - height * rescale_ratio)))
            area = (0, int(200 * size), 200, int(200 * size) + 200)
            img.crop(area)
            print(2)
            img = img.crop(area)
            img.save(img_io, format='JPEG', quality=70)
            img_content = ContentFile(img_io.getvalue(), 'profile.jpeg')
            return img_content


def image_quality_down(content_file):
    img = Image.open(content_file)
    img = img.convert("RGB")
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=70)
    img_content = ContentFile(img_io.getvalue(), 'image.jpeg')
    return img_content
