import subprocess
import shutil
import os

from my_sound.alarm import finish_alarm

class AnomalyDetector:
    current_dir = os.path.dirname(__file__)
    def __init__(self, source_dir, weights_path="best.onnx", output_dir="output"):
        self.source_dir = source_dir
        self.weights_path = weights_path
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # yolov5 모델의 경로 설정
        self.model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov5")

    def detect(self):
        # 결과 파일이 저장될 디렉토리 삭제
        shutil.rmtree(os.path.join(self.model_dir, "runs/detect"), ignore_errors=True)

        # detect.py 실행
        command = f"python {os.path.join(self.model_dir, 'detect.py')} --source ../{self.source_dir} --weights ../{self.weights_path}"
        subprocess.run(command, shell=True, cwd=self.model_dir)

        # 결과 파일을 output 디렉토리로 이동
        src_dir = os.path.join(self.model_dir, "runs/detect/exp")
        dst_dir = self.output_dir

        exp_num = 0
        while os.path.exists(os.path.join(dst_dir, f"exp{exp_num}")):
            exp_num += 1

        dst_exp_dir = os.path.join(dst_dir, f"exp{exp_num}")
        os.makedirs(dst_exp_dir)

        for filename in os.listdir(src_dir):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_exp_dir, filename)
            shutil.move(src_file, dst_file)

        finish_alarm()
