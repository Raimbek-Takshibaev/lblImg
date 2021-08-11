from os import listdir
from shutil import copyfile
from PIL import Image

outputSize = [96, 48]
ratio = outputSize[0] / outputSize[1]

def resize(img):
    size = img.size
    r = size[0] / size[1]
    if r < 1.75 or r > 2.25:
        return img.resize((outputSize[0], outputSize[1]))
    i = 1
    b = 0
    if r < ratio:
        i = 0
        b = 1
        n = size[0] % ratio
        new = []
        w = int(size[0] + ratio - n)
        new.append(w)
        new.append(int(w / r))
        size = new
        img = img.resize((size[0], size[1]))
    width_height = size[i] / int(ratio)
    delta = (width_height - size[i]) % 2
    right_bottom = int((size[b] - width_height) / 2) + delta
    left_top = int(right_bottom - delta)
    if i == 0:
        img = img.crop((0, left_top, size[0], int(size[1] - right_bottom)))
    else:
        img = img.crop((left_top, 0, int(size[0] - right_bottom), size[1]))
    return img.resize((outputSize[0], outputSize[1]))

inputImgPath = "C:\\datasets\\lpr_images\\images\\"
inputLblPath = "C:\\datasets\\lpr_images\\labels\\"
saveImgPaths = ["C:\\datasets\\lprnet_dataset\\train\\images\\", "C:\\datasets\\lprnet_dataset\\val\\images\\"]
saveLblPaths = ["C:\\datasets\\lprnet_dataset\\train\\labels\\", "C:\\datasets\\lprnet_dataset\\val\\labels\\"]
imgsCount = [500, 500]

files = listdir(inputImgPath)
for (i, savePath) in enumerate(saveImgPaths):
    count = 0
    for a in range(i):
        count = count + imgsCount[a]
    imgs = files[count:]
    imgs = imgs[:imgsCount[i]]
    for img in imgs:
        image = Image.open(inputImgPath + img)
        image.save(saveImgPaths[i] + img)
        copyfile(inputLblPath + img[:-4] + ".txt", saveLblPaths[i] + img[:-4] + ".txt")