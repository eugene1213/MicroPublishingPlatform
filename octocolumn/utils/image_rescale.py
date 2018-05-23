from io import StringIO, BytesIO
from PIL import Image
from django.core.files.base import ContentFile


# 프로필이미지 커스텀
# def profile_image_resizing(content_file, margin):
#     img = Image.open(content_file)
#     img_io = BytesIO()
#     img = img.convert("RGB")

#     if margin[0] == 'x':

#         if int(margin[-1]) == 0:
#             img = img.resize((200, 200), Image.ANTIALIAS)
#             img.save(img_io, format='JPEG', quality=99)
#             img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#             return img_content

#         else:
#             size = float(margin[1:]) * 0.01
#             height = img.height
#             width = img.width

#             if height > 200:
#                 rescale_height = height - 200
#                 rescale_ratio = rescale_height/height
#                 img.thumbnail((int(width - width * rescale_ratio), 200))
#                 area = (int(200 * size), 0, int(200 * size) + 200, 200)
#                 img = img.crop(area)
#                 img.resize((200, 200), Image.ANTIALIAS)
#                 img.save(img_io, format='JPEG', quality=99)
#                 img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#                 return img_content
#             elif height == 200:
#                 area = (int(200 * size), 0, int(200 * size) + 200, 200)
#                 img.crop(area)
#                 img = img.crop(area)
#                 img.save(img_io, format='JPEG', quality=99)
#                 img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#                 return img_content
#             else:
#                 rescale_ratio = 200/height
#                 img.thumbnail((int(width * rescale_ratio), 200), Image.ANTIALIAS)
#                 area = (int(200 * size), 0, int(200 * size) + 200, 200)
#                 img.crop(area)
#                 img = img.crop(area)
#                 img.save(img_io, format='JPEG', quality=99)
#                 img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#                 return img_content

#     else:
#         size = float(margin[1:]) * 0.01
#         height = img.height
#         width = img.width

#         if width > 200:
#             rescale_width = width - 200
#             rescale_ratio = rescale_width / height
#             img.thumbnail((200, int(height - height * rescale_ratio)))
#             area = (0, int(200 * size), 200, int(200 * size) + 200)
#             img = img.crop(area)
#             img.save(img_io, format='JPEG', quality=99)
#             img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#             return img_content
#         elif width == 200:
#             area = (0, int(200 * size), 200, int(200 * size) + 200)
#             img.crop(area)
#             img = img.crop(area)
#             img.save(img_io, format='JPEG', quality=99)
#             img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#             return img_content
#         else:
#             rescale_ratio = 200 / width
#             img.thumbnail((200, int(height - height * rescale_ratio)))
#             area = (0, int(200 * size), 200, int(200 * size) + 200)
#             img.crop(area)
#             img = img.crop(area)
#             img.save(img_io, format='JPEG', quality=99)
#             img_content = ContentFile(img_io.getvalue(), 'profile.jpg')
#             return img_content


# 대다수의 이미지
def image_quality_down(content_file):
    img = Image.open(content_file)
    img = img.convert("RGB")
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=70)
    img_content = ContentFile(img_io.getvalue(), 'image.jpeg')
    return img_content


def thumnail_cover_image_resize(content_file):
    img = Image.open(content_file)
    img_io = BytesIO()
    img = img.convert("RGB")

    height = img.height
    width = img.width

    if height < 250 and width < 482:
        img.save(img_io, format='JPEG', quality=99)
        img_content = ContentFile(img_io.getvalue(), 'thumbnail.jpeg')
        return img_content

    else:
        if 480/250 > width/height:
            besehratio = 482 / width
            hsize = height * besehratio
            img = img.resize((482, int(hsize)), Image.ANTIALIAS)
            img.save(img_io, format='JPEG', quality=99)
            img_content = ContentFile(img_io.getvalue(), 'thumbnail.jpeg')
            return img_content

        else:
            baseratio = 250 / height
            wsize = width * baseratio
            img = img.resize((int(wsize), 250), Image.ANTIALIAS)
            img.save(img_io, format='JPEG', quality=99)
            img_content = ContentFile(img_io.getvalue(), 'thumbnail.jpeg')
            return img_content


def profile_image_resizing(content_file):
    img = Image.open(content_file)
    img_io = BytesIO()
    img = img.convert("RGB")

    height = img.height
    width = img.width

    if height < 140 and width < 140:
        img.save(img_io, format='JPEG', quality=80)
        img_content = ContentFile(img_io.getvalue(), 'thumbnail.jpeg')
        return img_content

    else:
        if width > height:
            besehratio = 140 / height
            wsize = width * besehratio
            img = img.resize((int(wsize), 140), Image.ANTIALIAS)
            img.save(img_io, format='JPEG', quality=80)
            img_content = ContentFile(img_io.getvalue(), 'thumbnail.jpeg')
            return img_content

        else:
            baseratio = 140 / width
            hsize = height * baseratio
            img = img.resize((140, int(hsize)), Image.ANTIALIAS)
            img.save(img_io, format='JPEG', quality=80)
            img_content = ContentFile(img_io.getvalue(), 'thumbnail.jpeg')
            return img_content
