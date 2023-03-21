from AnomalyDetector import AnomalyDetector

# 반드시 소스 파일 혹은 디렉토리는 지정해주어야 합니다.
ad = AnomalyDetector('../dataset/images/val')

ad.detect()