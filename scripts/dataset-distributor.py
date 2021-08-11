from os import listdir
from shutil import copyfile

inputImgPath = "$yourPath"
inputLblPath = "$yourPath"
saveImgPaths = ["$yourPath"]
saveLblPaths = ["$yourPath"]
imgsCount = [500]

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
