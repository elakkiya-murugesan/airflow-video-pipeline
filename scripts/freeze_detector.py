import cv2
import numpy as np

def detect_freeze_frames(input_path, output_txt):
    cap = cv2.VideoCapture(input_path)
    ret, prev_frame = cap.read()
    frozen_frames = []

    index = 0
    while True:
        ret, curr_frame = cap.read()
        if not ret:
            break
        diff = np.sum(cv2.absdiff(prev_frame, curr_frame))
        if diff < 100:  
            frozen_frames.append(index)
        prev_frame = curr_frame
        index += 1

    with open(output_txt, 'w') as f:
        for frame in frozen_frames:
            f.write(f"Freeze at frame: {frame}\n")
    cap.release()
