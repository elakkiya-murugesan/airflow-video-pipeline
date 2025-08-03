import json
import cv2
import os

def crop_video(input_path, coords_path, output_dir):
    with open(coords_path, 'r') as f:
        coords = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    for i, coord in enumerate(coords):
        cap = cv2.VideoCapture(input_path)
        width = int(coord['x2']) - int(coord['x1'])
        height = int(coord['y2']) - int(coord['y1'])
        out_path = os.path.join(output_dir, f'crop_{i}.mp4')
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cropped = frame[coord['y1']:coord['y2'], coord['x1']:coord['x2']]
            out.write(cropped)

        cap.release()
        out.release()
