from os import listdir
from shutil import copyfile

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
        copyfile(inputImgPath + img, saveImgPaths[i] + img)
        copyfile(inputLblPath + img[:-4] + ".txt", saveLblPaths[i] + img[:-4] + ".txt")
