import cv2
import pytesseract
import pandas as pd
import os

def detect_text_from_video(input_path, output_csv):
    cap = cv2.VideoCapture(input_path)
    index = 0
    results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        text = pytesseract.image_to_string(frame)
        if text.strip():
            results.append({'frame': index, 'text': text.strip()})
        index += 1

    pd.DataFrame(results).to_csv(output_csv, index=False)
    cap.release()
