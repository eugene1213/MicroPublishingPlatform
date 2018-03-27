from io import BytesIO

from PIL import Image


def profile_image_resizing(content_file, margin):
    img = Image.open(content_file)
    img = img.convert("RGB")
    if margin[0] == 'x':
        size = float(margin[1:]) * 0.01
        height = img.height
        width = img.width

        if height > 200:
            rescale_height = height - 200
            rescale_ratio = rescale_height/height
            img.resize((int(width - width * rescale_ratio), 200), Image.ANTIALIAS)
        elif height == 200:
            pass
        else:
            rescale_ratio = 200/height
            img.resize((int(width * rescale_ratio), 200), Image.ANTIALIAS)

        img.crop((200*size, 0, 200*size + 200, 200))
        output = BytesIO()
        img.save(output, format='JPEG', quality=70)
        img.file = output
        return img

    else:
        size = float(margin[1:]) * 0.01
        height = img.height
        width = img.width

        if width > 200:
            rescale_width = width - 200
            rescale_ratio = rescale_width / width
            img.resize((height - height * rescale_ratio, 200), Image.ANTIALIAS)
        elif width == 200:
            pass
        else:
            rescale_ratio = 200 / width
            img.resize((height * rescale_ratio, 200), Image.ANTIALIAS)

        img.crop((0, 200 * size, 200, 200 * size + 200))
        output = BytesIO()
        img.save(output, format='JPEG', quality=70)
        img.file = output
        return img
