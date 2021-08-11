from os import listdir
from shutil import copyfile

inputLabelsPaths = ["C:\\Projects\\trafficCamDataset\\test\\labels\\", "C:\\Projects\\trafficCamDataset\\train\\labels\\", "C:\\Projects\\trafficCamDataset\\val\\labels\\"]
imgsCount = [400, 400, 90]

for (i, savePath) in enumerate(inputLabelsPaths):
    files = listdir(savePath)
    for label in files:
        file = open(savePath + label, "r")
        lines = []
        for line in file:
            j = "0" + line[1:]
            lines.append(j)
            print(line)
        writeFiles = open(savePath + label, "w")
        writeFiles.writelines(lines)
        file.close()
        writeFiles.close()