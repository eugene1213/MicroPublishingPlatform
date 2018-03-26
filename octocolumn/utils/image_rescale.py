def profile_image_resizing(img, margin):
    if margin[0] == 'x':
        size = float(margin[1:]) * 0.01
        img.height = 200
        img.width = img.width - 200*size
        pass
    else:
        pass
