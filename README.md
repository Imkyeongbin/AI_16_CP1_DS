# AI_16_CP1_DS

## 해당 프로젝트는 과적 차량을 불법차량으로 간주하고, yoloV5 모델을 이용해 학습하여 과적 차량을 찾아내는 모델을 작성합니다.

---

- 들어가기 전에
    - 이 모델은 yoloV5를 사용하므로 yoloV5를 설치해야 합니다.
    - yoloV5 설치 방법은 다음과 같습니다.
    Clone repo and install requirements.txt in a Python>=3.7.0 environment, including PyTorch>=1.7.
    ```
    git clone https://github.com/ultralytics/yolov5  # clone
    cd yolov5
    pip install -r requirements.txt  # install
    ```

- 프로젝트 작성 환경
    - windows 10 64비트 22H2
    - Anaconda3 - conda 23.1.0
    - 아나콘다 가상환경 - python 3.9.16

---

###  파일 설명(실행 순서와 동일합니다.)

1. sources/01_json_to_dataset_dir_form.ipynb
    - 라벨링 데이터 json파일을 기반으로, 라벨링 데이터와 원천 데이터를 묶어서 train 셋과 val 셋이 8:2 비율로 분류된 디렉토리를 작성하는 주피터 노트북 파일입니다.

    - 샘플 데이터는 다음과 같은 디렉토리 구조로 되어 있어야 합니다.
        ```
        AI_16_CP1_DS
        New_Sample
        ├─라벨링데이터
        │  └─TL1.대형차
        │      ├─불법차량
        │      └─정상차량
        └─원천데이터
            └─TS1.대형차
                ├─불법차량
                └─정상차량
        ```

    - json 파일 데이터
        - FILE_NAME, RESOLUTION, ITEMS['BOX', 'PACKAGE'] 항목만 실사용합니다.
        - 라벨링데이터의 json파일내 데이터의 FILE_NAME과 동일한 이미지 파일이 원천데이터 동일 라벨 디렉토리에 있어, 쌍으로 존재해야합니다.
        - RESOLUTION의 경우 WIDTH*HEIGHT 형식으로 되어있어야 합니다.
        - ITEMS[<number>]['BOX']의 경우 xywh의 형식으로 되어있어야 합니다.

        - 예시
            ```
            {
                "FILE":[{
                    "FILE_NAME":"A04_B01_C04_D01_0819_E07_F07_53_4.jpg",
                    "COLLECTIONMETHOD":"CCTV",
                    "DAY/NIGHT":"주",
                    "LANE":"다선",
                    "ROADNUMBER":"356번지방도로",
                    "PLACE":"초지대교1(초지리125-362)",
                    "IDCODE":"F07",
                    "DATE":"2021.08.19",
                    "WEATHER":"맑은날",
                    "RESOLUTION":"1920*1080",
                    "MAKE":"한화테크윈",
                    "MODELNAME":"XNO-6020R",
                    "FILESIZE":"335557",
                    "BOUNDINGCOUNT":"2",
                    "ITEMS":[
                        {
                        "DRAWING":"Box",
                        "SEGMENT":"중형차",
                        "BOX":"687.57,152.74,368.26,288.62",
                        "POLYGON":"",
                        "PACKAGE":"정상차량",
                        "CLASS":"정상차량",
                        "COVER":"",
                        "COURSE":"후면우측",
                        "CURVE":"정상주행"
                        }
                        ,
                        {
                        "DRAWING":"Box",
                        "SEGMENT":"대형차",
                        "BOX":"1094.33,151.28,153.32,140.04",
                        "POLYGON":"",
                        "PACKAGE":"불법차량",
                        "CLASS":"적재불량",
                        "COVER":"덮개개방",
                        "COURSE":"후면우측",
                        "CURVE":"정상주행"
                        }
                    ]
                }]
            }
            ```

    - 모든 디렉토리, 파일 구조가 정상적으로 되어있다는 전제하에, `프로젝트 루트/dataset` 디렉토리에 images, labels 디렉토리가 `sources/config.yaml`파일 내용에 알맞게 각각 생성되며, `02_training_model.ipynb`을 통해 바로 학습할 수 있도록 파일이 배치됩니다.

2. sources/02_training_model.ipynb
    - 파이썬 매직 커맨드를 사용하여 yoloV5의 파일을 직접 이용해 학습합니다.

    - 순서대로 전부 실행하여, 학습된 모델 가중치파일(best.pt)를 얻을 수 있습니다.

    - 학습 및 검증 종료시 소리로 알 수 있게 알람 기능을 넣었습니다. (다만 OS별로 알람 소리가 다르므로 유의 부탁드립니다.)

    - 학습
        - 학습 과정에서 사용하는 패러미터는 다음과 같습니다.
            - `--img 640 --batch 32 --epochs 100 --data config.yaml --weights yolov5m.pt --cache`
        - 종료시 `yolov5/runs/train` 디렉토리 안에서 exp<number>의 형태의 디렉토리로 결과를 확인할 수 있습니다.
    - 검증
        - 검증 과정에서 사용하는 패러미터는 다음과 같습니다.
            - `--weights ../yolov5/runs/train/$max_dir_name/weights/best.pt --data config.yaml`
            여기서 `$max_dir_name`은 exp<number> 기준 최근 디렉토리명입니다.
        - 종료시 `yolov5/runs/val` 디렉토리 안에서 exp<number>의 형태의 디렉토리로 결과를 확인할 수 있습니다.

3. sources/03_detecting.ipynb
    - 파이썬 매직 커맨드를 사용하여 yoloV5의 파일을 직접 이용해 불법 차량(과적 차량)을 탐지합니다.

    - 순서대로 전부 실행하고, 마지막 네번째 주피터 셀에서 SOURCE변수를 변경하여 소스 파일 혹은 디렉토리를 선택해 불법 차량을 탐지할 수 있습니다.
        - SOURCE 양식은 `https://github.com/ultralytics/yolov5/blob/master/detect.py`의 6행부터의 내용을 참고 부탁드립니다.

    - 마찬가지로, 탐지 종료시 소리로 알 수 있게 알람 기능을 넣었습니다.

    - 탐지 종료시 `yolov5/runs/detect` 디렉토리 안에서 exp<number>의 형태의 디렉토리로 결과를 확인할 수 있습니다.