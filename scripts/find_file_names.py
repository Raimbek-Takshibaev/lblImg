import os

outputTxt = "file_names.txt"
names = []
dirsCount = 0
filesCount = 0
# ../../566E73F36E73CA6F/ViolationsData/57/2017/02/15/12/32/20170215123222_946_F0139_3_3_B-504-WON   _000_3_1.dat
for path, subdirs, files in os.walk("../../566E73F36E73CA6F/ViolationsData"):
    dirsCount += len(subdirs)
    filesCount += len(files)
    for name in files:
        txt =  os.path.join(path, name)
        if txt[-3:] == "dat":
            ff = txt.replace("../../566E73F36E73CA6F/ViolationsData", "\\\\10.200.10.218\\data")
            ff = ff.replace("/", "\\")
            names.append(txt + "\n")

outputFile = open(outputTxt, "w+")
outputFile.writelines(names)
outputFile.close()
print(len(names), dirsCount, filesCount)