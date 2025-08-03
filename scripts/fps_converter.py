import cv2
import os

def convert_video_to_1fps(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    out = None
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % int(fps) == 0:
            if out is None:
                height, width = frame.shape[:2]
                out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))
            out.write(frame)
            frame_count += 1

    cap.release()
    if out:
        out.release()
