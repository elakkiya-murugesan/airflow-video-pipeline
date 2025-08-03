import cv2
import pandas as pd
import os

def match_template(cropped_dir, template_path, output_csv):
    template = cv2.imread(template_path, 0)
    result = []

    for file in os.listdir(cropped_dir):
        if file.endswith('.mp4'):
            cap = cv2.VideoCapture(os.path.join(cropped_dir, file))
            index = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > 0.8:
                    result.append({'video': file, 'frame': index, 'score': max_val})
                index += 1
            cap.release()

    pd.DataFrame(result).to_csv(output_csv, index=False)
