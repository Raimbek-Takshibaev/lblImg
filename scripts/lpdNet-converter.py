from os import listdir
from shutil import copyfile
from PIL import Image, ImageTk
import tkinter as tk

inputImagesPaths = ["$yourPath"] # вводные пути до картинок
inputLabelsPaths = ["$yourPath"] # вводные пути до уже размеченных лейблов
saveImagesPaths = ["$yourPath"] # пути сохранения картинок
saveLabelsPaths = ["$yourPath"] # пути сохранения лейблов
classList = ["license_plate"] # название класса (для LPDNet длина массива должна остаться текущей)

windowWidth = 250
window = tk.Tk()
imageCheck="none"

def askLabelOwnership(upper, lower, carNum):
    tkLabel = tk.Label(
        text="Какая из картинок имеет номер " + carNum + "?"
    )
    tkImgUpper = tk.Button(
        text="",
        image=upper,
        command=chosenUpperImage
    )
    tkImgLower = tk.Button(
        text="",
        image=lower,
        command=chosenLowerImage
    )
    tkImgLower.image = lower
    tkImgUpper.image = upper
    tkLabel.pack()
    tkImgUpper.pack()
    tkImgLower.pack()
    window.mainloop()

def chosenUpperImage():
    imageCheck = "upper"
    window.destroy()

def chosenLowerImage():
    imageCheck = "lower"
    window.destroy()

def getResizedImage(img):
    (w, h) = img.size
    r = w / h
    height = windowWidth / r
    img = img.resize((int(windowWidth), int(height)))
    return img

def get_yolo_params(prms):
    output = {
            "class": int(prms[0]),
            "center_x": int(prms[1]),
            "center_y": int(prms[2]),
            "w": int(prms[3]),
            "h": int(prms[4])
        }
    return output

# imgCoor = [x_min, y_min, x_max, y_max] labelCoor = [x_min, y_min]
def check_label_ownership(imgCoor, labelCoor):
    if(imgCoor[2] > labelCoor[0] > imgCoor[0] and imgCoor[3] > labelCoor[1] > imgCoor[1]):
        return True
    return False

def get_yolo_params(prms, path=""):
    output = []
    if path != "":
        file = open(path, "r")
        lines = file.readlines()
        for (i, line) in enumerate(lines):
            prms = line.split(" ")
            parsedPrms = {
                "class": int(prms[0]),
                "center_x": float(prms[1]),
                "center_y": float(prms[2]),
                "w": float(prms[3]),
                "h": float(prms[4])
            }
            output.append(parsedPrms)
        file.close()
    return output

# Label_ID_1 X_CENTER_NORM Y_CENTER_NORM WIDTH_NORM HEIGHT_NORM
def bnd_box_to_yolo_line(x_min, x_max, y_min, y_max, img_size, className, class_list=classList):
        x_center = float((x_min + x_max)) / 2 / img_size[0]
        y_center = float((y_min + y_max)) / 2 / img_size[1]

        w = float((x_max - x_min)) / img_size[0]
        h = float((y_max - y_min)) / img_size[1]

        class_index = class_list.index(className)

        return class_index, x_center, y_center, w, h

def yolo_line_to_shape(x_center, y_center, w, h, img_size):
        # label = outputClassList[int(class_index)]

        x_min = max(float(x_center) - float(w) / 2, 0)
        x_max = min(float(x_center) + float(w) / 2, 1)
        y_min = max(float(y_center) - float(h) / 2, 0)
        y_max = min(float(y_center) + float(h) / 2, 1)

        x_min = round(img_size[0] * x_min)
        x_max = round(img_size[0] * x_max)
        y_min = round(img_size[1] * y_min)
        y_max = round(img_size[1] * y_max)

        return x_min, y_min, x_max, y_max

# transportNumber_plateX_plateY_plateWidth_plateHeight or id_noNum
for (i, inputImgPath) in enumerate(inputImagesPaths):
    files = listdir(inputImgPath)
    for (a, file) in enumerate(files):
        params = file.split("_")
        if(len(params) != 5):
            continue
        image = Image.open(inputImgPath + file)
        format = image.format

        plateX = int(params[1])
        plateY = int(params[2])
        plateWidth = int(params[3])
        plateHeight = int(params[4][:-len(format)])
        
        labelName = file[:-len(format)] + ".txt"
        imageSize = image.size
        inputImgYoloPrms = get_yolo_params([], inputLabelsPaths[i] + labelName)
        x_min = 0
        y_min = 0
        x_max = 0
        y_max = 0
        isOnlyImage = False
        trueImgCoor = []
        for (p, inputImgYoloPrm) in enumerate(inputImgYoloPrms):
            inputImgCoor = yolo_line_to_shape(inputImgYoloPrm["center_x"], inputImgYoloPrm["center_y"], inputImgYoloPrm["w"], inputImgYoloPrm["h"], imageSize)
            if check_label_ownership(inputImgCoor, [plateX, plateY]):
                if isOnlyImage == False:
                    isOnlyImage = True
                    x_min = plateX - inputImgCoor[0]
                    y_min = plateY - inputImgCoor[1]
                    x_max = x_min + plateWidth
                    y_max = y_min + plateHeight - inputImgCoor[1]
                    trueImgCoor = inputImgCoor
                else:
                    x_min_l = plateX - inputImgCoor[0]
                    y_min_l = plateY - inputImgCoor[1]
                    x_max_l = plateX + plateWidth - inputImgCoor[0]
                    y_max_l = plateY + plateHeight - inputImgCoor[1]
                    upper = ImageTk.PhotoImage(getResizedImage(image.crop((trueImgCoor[0], trueImgCoor[1], trueImgCoor[2], trueImgCoor[3]))))
                    lower = ImageTk.PhotoImage(getResizedImage(image.crop((inputImgCoor[0], inputImgCoor[1], inputImgCoor[2], inputImgCoor[3]))))
                    imageCheck = "none"
                    askLabelOwnership(upper, lower, params[0])
                    if(imageCheck == "lower"):
                        x_min = x_min_l
                        y_min = y_min_l
                        x_max = x_max_l
                        y_max = y_max_l
                        trueImgCoor = inputImgCoor
        img = image.crop((trueImgCoor[0], trueImgCoor[1], trueImgCoor[2], trueImgCoor[3]))
        img.save(saveImagesPaths[i] + file)
        (class_index, x_center, y_center, w, h) = bnd_box_to_yolo_line(x_min, x_max, y_min, y_max, img.size, classList[0])
        newLabel = open(saveLabelsPaths[i] + labelName, "w")
        newLabel.write(str(class_index) + " " +  str(x_center) + " " +  str(y_center) + " " +  str(w) + " " +  str(h))
        newLabel.close()

        

        