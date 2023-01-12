import cv2
import numpy as np

BG_COLOR = 209
BG_SIGMA = 5
MONOCHROME = 1


def blank_image(width=1024,
                height=1024,
                background=BG_COLOR):
    """
    It creates a blank image of the given background color
    """
    img = np.full((height, width, MONOCHROME), background, np.uint8)
    return img


def add_noise(img, sigma=BG_SIGMA):
    """
    Adds noise to the existing image
    """
    width, height, ch = img.shape
    n = noise(width, height, sigma=sigma)
    img = img + n
    return img.clip(0, 255)


def noise(width: int,
          height: int,
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
                            #dsize=(width, height),
                            dsize=(height, width),
                            interpolation=cv2.INTER_LINEAR)
        # interpolation=cv2.INTER_CUBIC)
    #result.reshape((width, height, MONOCHROME))
    return result.reshape((width, height, MONOCHROME))
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
    result = image.astype(float)
    cols, rows, ch = image.shape
    # Find smallest rescaling
    ratio = 1
    while True:
        if cols % (ratio*turbulence) == 0 and rows % (ratio*turbulence) == 0:
            ratio = ratio*turbulence
        else:
            break
    print(ratio)
    while not ratio == 1:
        print("texture: ", ratio)
        result += noise(cols, rows, ratio, sigma=sigma)
        ratio = (ratio // turbulence) or 1
    cut = np.clip(result, 0, 255)
    return cut.astype(np.uint8)


if __name__ == '__main__':
    print("Import")
    #image = cv2.imread('BarnsleyFern2.png')
    image = cv2.imread('2023-01-11 09.34.22-1.jpg')
    #MONOCHROME = 3
    # print(image.shape)
    #image = blank_image(width=1280, height=1024, background=230)
    #image = blank_image(width=3840, height=2160, background=230)
    print(image.shape)
    width, height, ch = image.shape
    print("Make Texture")
    #image_texture = texture(image, sigma=4, turbulence=4)
    image_texture = texture(image, sigma=4, turbulence=4)
    print("write: texture.jpg")
    cv2.imwrite('texture.jpg', image_texture)
    print("Make Texture + Noise")
    texture_and_noises = add_noise(image_texture, sigma=10)
    print("write: texture-and-noise.jpg")
    cv2.imwrite('texture-and-noise.jpg', texture_and_noises)

    #print("Make Noise")
    #cv2.imwrite('noise.jpg', add_noise(blank_image(width, height), sigma=10))
    # print("DONE")
