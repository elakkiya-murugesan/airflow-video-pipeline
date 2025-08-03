from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

from scripts.fps_converter import convert_video_to_1fps
from scripts.cropper import crop_video
from scripts.freeze_detector import detect_freeze_frames
from scripts.ocr_text_detector import detect_text_from_video
from scripts.template_matcher import match_template
from scripts.mkv_to_mp4_converter import convert_mkv_to_mp4

BASE_DIR = "/opt/airflow"  
SAMPLE_DIR = os.path.join(BASE_DIR, "sample_data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 0,
}

with DAG(
    dag_id="video_processing_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Pipeline to process video in 6 steps",
) as dag:

    convert_to_1fps = PythonOperator(
        task_id="convert_to_1fps",
        python_callable=convert_video_to_1fps,
        op_kwargs={
            "input_path": os.path.join(SAMPLE_DIR, "sample.mkv"),
            "output_path": os.path.join(OUTPUT_DIR, "video_1fps.mp4"),
        },
    )

    crop_video_op = PythonOperator(
        task_id="crop_video",
        python_callable=crop_video,
        op_kwargs={
            "input_path": os.path.join(OUTPUT_DIR, "video_1fps.mp4"),
            "coords_path": os.path.join(SAMPLE_DIR, "coords.json"),
            "output_dir": os.path.join(OUTPUT_DIR, "cropped_videos"),
        },
    )

    detect_freeze = PythonOperator(
        task_id="detect_freeze",
        python_callable=detect_freeze_frames,
        op_kwargs={
            "input_path": os.path.join(SAMPLE_DIR, "sample.mkv"),
            "output_txt": os.path.join(OUTPUT_DIR, "freeze_frames.txt"),
        },
    )

    detect_text = PythonOperator(
        task_id="detect_text",
        python_callable=detect_text_from_video,
        op_kwargs={
            "input_path": os.path.join(OUTPUT_DIR, "video_1fps.mp4"),
            "output_csv": os.path.join(OUTPUT_DIR, "detected_text.csv"),
        },
    )

    match_template_op = PythonOperator(
        task_id="match_template",
        python_callable=match_template,
        op_kwargs={
            "cropped_dir": os.path.join(OUTPUT_DIR, "cropped_videos"),
            "template_path": os.path.join(SAMPLE_DIR, "template.jpg"),
            "output_csv": os.path.join(OUTPUT_DIR, "template_matches.csv"),
        },
    )

    mkv_to_mp4_op = PythonOperator(
        task_id="convert_mkv_to_mp4",
        python_callable=convert_mkv_to_mp4,
        op_kwargs={
            "input_path": os.path.join(SAMPLE_DIR, "sample.mkv"),
            "output_path": os.path.join(OUTPUT_DIR, "converted_video.mp4"),
        },
    )

    convert_to_1fps >> crop_video_op >> match_template_op
    convert_to_1fps >> detect_text
    mkv_to_mp4_op  
    detect_freeze  
