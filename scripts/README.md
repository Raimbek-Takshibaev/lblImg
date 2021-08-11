## Превью по скриптам

**dataset-distributor**
	 Он нужен для распределения картинок и размеченных лейблов по другим папкам по типу train, val, test.
	 Если посмотреть на сам код, но в начале инициализируются входные параметры:
	 

    inputImgPath = "C:\\datasets\\lpr_images\\images\\"  ## путь до самих картинок
    
    inputLblPath = "C:\\datasets\\lpr_images\\labels\\"  ## путь до лейблов
    
    saveImgPaths = ["C:\\datasets\\lprnet_dataset\\train\\images\\", "C:\\datasets\\lprnet_dataset\\val\\images\\"] ## пути сохранения картинок
    
    saveLblPaths = ["C:\\datasets\\lprnet_dataset\\train\\labels\\", "C:\\datasets\\lprnet_dataset\\val\\labels\\"] ## пути сохранения лейблов
    
    imgsCount = [500, 500] ## количество картинок и лейблов, которые будут сохраняться в выше указанные пути
    
    ## длина массивов imgsCount, saveLblPaths, saveImgPaths должна быть одинаковой, а также порядок папок по типу train, val, test должен быть схожим

**lpdNet-converter**
	Этот скрипт берет пути до картинок, и пути до **размеченных** для TrafficCamNet лейблов, вырезает размеченную машину, в которой присутствует уже имеющийся номер машины при имеющихся координатах номера. В случае пересечения координат скрипт дает выбрать правильную машину
	

    inputImagesPaths = ["$yourPath"] # вводные пути до картинок
    
    inputLabelsPaths = ["$yourPath"] # вводные пути до уже размеченных лейблов
    
    saveImagesPaths = ["$yourPath"] # пути сохранения картинок
    
    saveLabelsPaths = ["$yourPath"] # пути сохранения лейблов
    
    classList = ["license_plate"] # название класса (для LPDNet длина массива должна остаться текущей)
    ## длина массивов inputImagesPaths, inputLabelsPaths, saveImagesPaths, saveLabelsPaths должна быть одинаковой, а также порядок папок по типу train, val, test должен быть схожим

## Тренировка TrafficCamNet

 1. Раделить датасет на train, val, test и распределить используя dataset-distributor
 2. Загрузить его на машину, в которой будет происходить тренировка
 3. Сделать файл конфигурации по типу ниже, обратите внимание что в каждой из приведенных директорий должны содержатся папки images и labels, уже размеченные
 

        train: ../path/to/train
	    val: ../path/to/val
	    test: ../path/to/test
    
	    # number of classes
	    nc: 1
    
	    # class names
	    names: ['className']

 4.  run train
 

		    # Train YOLOv5s on COCO128 for 3 epochs
			$ python train.py --batch 16 --epochs 3 --data coco128.yaml --weights yolov5s.pt

5. Для большей информации https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data

## Тренировка LPDNet

 1. подготовить датасет используя уже размеченные картинки для trafficCamNet используя lpdNet-converter
 2. повторить то же самое с TrafficCamDataset
 
## Тренировка LPRNet
 1. Сконвертировать картинки используя ViolationFilter
 2. Раделить датасет на train, val, test и распределить используя dataset-distributor
 3. настроить .tlt_mounts.json:

	    nano ~/tlt_mounts.json

 и вставить следующее:
 

	    {
		    "Mounts": [
		        {
		            "source": "/path/to/your/experiments",
		            "destination": "/workspace/tlt-experiments"
		        }
		    ]
		}
				
Отныне введенная директория сверху будет использоваться в tlt_container 
    4. подготовить файл конфигурации, вот ссылка на документацию: https://docs.nvidia.com/tlt/tlt-user-guide/text/character_recognition/lprnet.html
    5.  тренировка
			

    tlt lprnet train -e <experiment_spec_file>
                 -r <results_dir>
                 -k <key>
                [--gpus <num_gpus>]
                [--gpu_index <gpu_index>]
                [--use_amp]
                [--log_file <log_file>]
                [-m <resume_model_path>]
                [--initial_epoch <initial_epoch>]
6. подробное описание всех комманд присутствует по ссылке сверху
