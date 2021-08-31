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

**Пример запуска для dataset_1**

 - В датасете есть две папки - labels, images
 следовательно нам нужно создать отдельную директорию под названием lpdDataset_1, к примеру. И в эту же директорию добавляем две папки labels, images.
 
 - Далее нужно вставить пути в массивы до этих папок:
 

	    inputImagesPaths = ["path/to/dataset_1/images/"]
    
	    inputLabelsPaths = ["path/to/dataset_1/labels/"]
    
	    saveImagesPaths = ["path/to/lpdDataset_1/images/"]
    
	    saveLabelsPaths = ["path/to/lpdDataset_1/labels/"]

**Очень важно чтоб на конце этих путей стоял '/'**

Для запуска скрипта нужно скачать:

 - Pillow
	

	    python3 -m pip install --upgrade pip
    	python3 -m pip install --upgrade Pillow

 - Tkinter
 

	    pip install tk

 - Ну и запускаем скрипт
 
 

	    python lpdNet-converter.py

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

 - подготовить датасет используя уже размеченные картинки для trafficCamNet используя lpdNet-converter
 - повторить то же самое с TrafficCamDataset
 
## Тренировка LPRNet
 
 - **Необходимо подготовить датасет**
	 1. Первым делом должен присутствовать размеченный LPDNet для йоло
	 2. Преобразовать из LPDNet в LPR используя скрипт fromLpdToLpr.py
	 3. Раделить датасет на train, val и распределить используя dataset-distributor.py
	 4. Вставить датасет к примеру в ~/projects/LPRNet/datasets под названием dataset_2
	 5. Создадим папку specs и добавим текстовый документ под названием us_lp_characters.txt
	 6. Заполним us_lp_characters.txt, добавляя символы, которые будут присутствовать в номерах, **раздельно и с переносом строки**
 - **Нужно настроить .tlt_mounts.json:**

	    nano ~/tlt_mounts.json

 и вставить следующее:
 

	    {
		    "Mounts": [
		        {
		            "source": "~/projects/LPRNet",
		            "destination": "/workspace/LPRNet"
		        }
		    ]
		}
				
Отныне введенная директория сверху будет развертываться в tlt_container 
    

 - **Далее нужно подготовить файл конфигурации:** 
  Создадим txt файл под названием dataset_2_spec.txt и сохраним его в папке specs. Вставим эту конфигурацию:

	    random_seed: 42
		lpr_config {
		  hidden_units: 512
		  max_label_length: 10
		  arch: "baseline"
		  nlayers: 18
		}
		training_config {
		  batch_size_per_gpu: 64
		  num_epochs: 300
		  learning_rate {
			  soft_start_annealing_schedule {
			    min_learning_rate: 1e-6
			    max_learning_rate: 1e-4
			    soft_start: 0.001
			    annealing: 0.7
				}
			}
		  regularizer {
		    type: L2
		    weight: 5e-4
		  }
		}
		eval_config {
		  validation_period_during_training: 5
		  batch_size: 1
		}
		augmentation_config {
		  output_width: 96
		  output_height: 48
		  output_channel: 3
		  max_rotate_degree: 5
		  rotate_prob: 0.5
		  gaussian_kernel_size: 5
		  gaussian_kernel_size: 7
		  gaussian_kernel_size: 15
		  blur_prob: 0.5
		  reverse_color_prob: 0.5
		  keep_original_prob: 0.3
		}
		dataset_config {
		  data_sources: {
		    label_directory_path: "/workspace/LPRNet/datasets/dataset_2/train/labels"
		    image_directory_path: "/workspace/LPRNet/datasets/dataset_2/train/images"
		  }
		  characters_list_file: "/workspace/LPRNet/specs/us_lp_characters.txt"
		  validation_data_sources: {
		    label_directory_path: "/workspace/LPRNet/datasets/dataset_2/train/val/images"
		    image_directory_path: "/workspace/LPRNet/datasets/dataset_2/train/val/labels""
		  }
		}
Отдельно стоит выделить **dataset_config**:
|dataset_config|  |
|--|--|
|data_sources| label_directory_path - путь до тренировочных лейблов, image_directory_path - путь до тренировочных картинок   |
|characters_list_file| путь до txt файла со списком символов |
|validation_data_sources| label_directory_path - путь до валидационных лейблов, image_directory_path - путь до валидационных картинок   |

Подробную информацию о каждой конфигурации можно найти тут -
https://docs.nvidia.com/tao/tao-toolkit/text/character_recognition/lprnet.html


 - **Virtual environment** 
 

	    source ~/.local/bin/virtualenvwrapper.sh
		mkvirtualenv launcher -p /usr/bin/python3

   

 - **Тренировка**

			

	    tao lprnet train -e <experiment_spec_file>
                 -r <results_dir>
                 -k <key>
                [--gpus <num_gpus>]
                [--gpu_index <gpu_index>]
                [--use_amp]
                [--log_file <log_file>]
                [-m <resume_model_path>]
                [--initial_epoch <initial_epoch>]
	| Обязятельные аргументы |   |
	|--|--|
	| -e, --experiment_spec_file | Путь до файла конфигурации |
	| -r, --results_dir | Путь к папке, в которую должны быть записаны результаты 			эксперимента. |
	| -k, --key | Ключ кодировки, определяемый пользователем, для сохранения или 	загрузки модели .tlt. |
	______
	| Необязятельные аргументы|  |
	|--|--|
	|. --gpus | Количество графических процессоров, которые будут использоваться 	при обучении в сценарии с несколькими графическими процессорами (по умолчанию: 1). |
	|. --gpu_index | Индексы GPU, используемые для обучения. Мы можем указать индексы графического процессора, используемые для запуска обучения, когда на машине установлено несколько графических процессоров. |
	|. --use_amp | Флаг для включения обучения AMP. |
	|. --log_file | Путь к файлу журнала. По умолчанию - stdout. |
	| -m,  --resume_model_weights | Путь к предварительно обученной модели или модели для продолжения обучения.|
	|. --initial_epoch | Эпоха начала тренировок. |

Запуск тренировки

    tao lprnet train -e /workspace/LPRNet/specs/dataset_2_spec.txt -r /workspace/LPRNet/unpruned_pretrained_model -k nvidia_tlt -m /workspace/LPRNet/unpruned_pretrained_model/weights/lprnet_epoch-300 --initial_epoch 301

  - **Экспорт модели**

			

	    tlt lprnet export -m <model>
                  -k <key>
                  -e <experiment_spec>
                  [--gpu_index <gpu_index>]
                  [--log_file <log_file>]
                  [-o <output_file>]
                  [--data_type {fp32,fp16}]
                  [--max_workspace_size <max_workspace_size>]
                  [--max_batch_size <max_batch_size>]
                  [--engine_file <engine_file>]
                  [-v]
	
	|  Обязятельные аргументы |   |
	| -- | -- |
	| -e, --experiment_spec_file | Путь до файла конфигурации |
	| -m,  --resume_model_weights | Экспортируемая модель .tlt|
	| -k, --key | Ключ кодировки, определяемый пользователем, для сохранения или 	загрузки модели .tlt. |
	______
	
	|  Необязятельные аргументы|  |
	| -- | -- |
	|  . --gpu_index | Индексы GPU, используемые для обучения. Мы можем указать индексы графического процессора, используемые для запуска обучения, когда на машине установлено несколько графических процессоров. |
	|  . --log_file | Путь к файлу журнала. По умолчанию - stdout. |
	|  -o,  --output_file | Путь для сохранения экспортированной модели. По умолчанию   ./ <input_file> .etlt. |
	|  . --data_type | Требуемый тип данных двигателя для создания кэша калибровки в режиме INT8. Возможные варианты: fp32 или fp16. Значение по умолчанию - fp32. Вы можете использовать следующие необязательные аргументы для сохранения механизма TRT, созданного для проверки экспорта: |
	|  . --max_batch_size| Максимальный размер пакета движка TensorRT. Значение по умолчанию - 16. |
	|  .  --max_workspace_size | Максимальный размер рабочего пространства движка TensorRT. Значение по умолчанию - 1073741824 (1 << 30).|
	|  .  --engine_file | Путь к сериализованному файлу движка TensorRT. Обратите внимание, что этот файл зависит от оборудования и не может быть распространен на графические процессоры. Полезно для быстрой проверки точности вашей модели с помощью TensorRT на хосте. Поскольку файл ядра TensorRT зависит от оборудования, вы не можете использовать этот файл ядра для развертывания, если графический процессор развертывания не идентичен обучающему графическому процессору.|

Запуск экспорта

    tlt lprnet export -m /workspace/LPRNet/unpruned_pretrained_model/weights/lprnet_epoch-600.tlt -k nvidia_tlt -e /workspace/LPRNet/specs/dataset_2_spec.txt --data_type fp16 -o /workspace/LPRNet/exported_models/dataset_2_epoch_600.etlt

 - **Конвертирование в engine**
 
		
		docker run --gpus all -it --rm -v ~/projects/LPRNet:/workspace/LPRNet nvcr.io/nvidia/tensorrt:21.08-		py3
		cd /workspace/LPRNet/tao_converter/cuda11.3-trt8.0
	    ./tao-converter ../../exported_models/dataset_2_epoch_600.etlt -k nvidia_tlt -p image_input,1x3x48x96,4x3x48x96,16x3x48x96 -e ../../engines/dataset_2_epoch_600.engine
