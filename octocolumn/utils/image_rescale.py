def profile_image_resizing(img, margin):
    if margin[0] == 'x':
        size = float(margin[1:]) * 0.01
        img.height = 200
        src_width = img.width - 200*size
        src_height = 200
        img.crop(im)
        pass
    else:
        pass
