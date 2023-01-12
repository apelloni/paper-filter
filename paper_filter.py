import cv2
import numpy as np

BG_COLOR = 209
BG_SIGMA = 5
MONOCHROME = 1


def blank_image(height=1024,
                width=1024,
                background: int | list = BG_COLOR):
    """
    It creates a blank image of the given background color
    """
    if type(background) == int:
        img = np.full((height, width, MONOCHROME), background, np.uint8)
    elif type(background) == list and len(background) == 3:
        img = np.full((height, width, 3), background, np.uint8)
    else:
        raise TypeError

    return img


def add_noise(img, sigma=BG_SIGMA):
    """
    Adds noise to the existing image
    """
    height, width, ch = img.shape
    n = noise(height, width, sigma=sigma)
    img = img + n
    return img.clip(0, 255)


def noise(height: int,
          width: int,
          ratio: int = 1,
          sigma=BG_SIGMA
          ):
    """
    The function generates an image, filled with gaussian noise.
     - ratio parameter:
        noise will be generated for a smaller image and then
        scaled up to the original size.
        In that case noise will generate larger square patterns.
        To avoid multiple lines, the upscale uses interpolation.

    :param ratio: the size of generated noise "pixels"
    :param sigma: defines bounds of noise fluctuations
    """
    mean = 0
    assert width % ratio == 0,\
        f"Can't scale image with of size {width} and ratio {ratio}"

    assert height % ratio == 0,\
        f"Can't scale image with of size {height} and ratio {ratio}"

    h = int(height / ratio)
    w = int(width / ratio)

    result = np.random.normal(mean, sigma, (w, h, MONOCHROME))
    #result = np.reshape(np.linspace(-100,100, w*h*MONOCHROME),(w,h,MONOCHROME))
    print(np.shape(result))
    if ratio > 1:
        print("noise: ", ratio)
        result = cv2.resize(result,
                            dsize=(width, height),
                            interpolation=cv2.INTER_LINEAR)
        # interpolation=cv2.INTER_CUBIC)
    #result.reshape((width, height, MONOCHROME))
    return result.reshape((height, width, MONOCHROME))
    # print(np.shape(result))
    # return result


def texture(image,
            sigma=BG_SIGMA,
            turbulence=2
            ):
    """
    Consequently applies noise patterns to the original image from big to small.

    sigma: defines bounds of noise fluctuations
    turbulence: defines how quickly big patterns will be replaced with the small ones. The lower
    value - the more iterations will be performed during texture generation.
    """
    print("Convert")
    result = image.astype(float)
    print("Convert DONE")
    rows, cols, ch = image.shape
    # Find smallest rescaling
    ratio = 1
    print(rows, cols)
    while True:
        if rows % (ratio*turbulence) == 0 and cols % (ratio*turbulence) == 0:
            ratio = ratio*turbulence
        else:
            break
    print(ratio)
    while not ratio == 1:
        print("texture: ", ratio)
        result += noise(rows, cols, ratio, sigma=sigma)
        ratio = (ratio // turbulence) or 1
    print("clip: ")
    cut = np.clip(result, 0, 255)
    return cut.astype(np.uint8)


if __name__ == '__main__':
    print("Import")
    #image = cv2.imread('BarnsleyFern2.png')
    #image = cv2.imread('2023-01-11 09.34.22-1.jpg')
    image = cv2.imread('US10752321-20200825-D00005.png')
    #MONOCHROME = 3
    # print(image.shape)
    #background_color = [255, 255, 255]
    #image = blank_image(width=512, height=1024, background=background_color)
    #image = blank_image(width=3840, height=2160, background=230)
    print(image.shape)
    height, width, ch = image.shape

    new_height = 2**int(np.ceil(np.log2(height)))
    new_width = 2**int(np.ceil(np.log2(width)))
    # extend height
    background_color = [0, 0, 0]
    patch_height = blank_image(height=new_height-height,
                         width=width, background=background_color)
    image_patched = cv2.vconcat([image, patch_height])
    # extend width
    patch_width = blank_image(
        height=new_height, width=new_width-width,  background=background_color)
    image_patched = cv2.hconcat([image_patched, patch_width])
    print(image_patched.shape)

    print("Make Texture")
    #image_texture = texture(image, sigma=4, turbulence=4)
    # image_texture = texture(image_patched, sigma=10, turbulence=4) # compare_1
    image_texture = texture(image_patched, sigma=8, turbulence=2) # compare_2
    image_texture = image_texture[:height, :width]
    print("write: texture.jpg")
    image_texture = image_texture[:height, :width]
    cv2.imwrite('texture.jpg', image_texture)

    line_color = [0, 0, 0]
    line = blank_image(height=height,
                         width=20, background=line_color)
    compare = cv2.hconcat([image,line,image_texture])
    cv2.imwrite('compare.jpg', compare)
    # print("Make Texture + Noise")
    # texture_and_noises = add_noise(image_texture, sigma=10)
    # print("write: texture-and-noise.jpg")
    # cv2.imwrite('texture-and-noise.jpg', texture_and_noises)

    #print("Make Noise")
    #cv2.imwrite('noise.jpg', add_noise(blank_image(width, height), sigma=10))
    # print("DONE")
