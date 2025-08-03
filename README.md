
# Video Processing Pipeline with Apache Airflow

 Automated video processing pipeline built with Apache Airflow, integrating essential operations such as frame rate conversion, cropping, freeze detection, OCR text extraction, template matching, and video format conversion within a DAG-based workflow.

---

## Key Features

- Convert videos to 1 FPS for analysis
- Crop videos using coordinate sets from JSON
- Detect freeze frames
- Perform text detection (OCR) on frames
- Template matching to find similar frames
- Convert MKV files to MP4

---

## Folder Structure

```
video_pipeline/
├── dags/
│   └── video_processing_pipeline_dag.py     
│
├── scripts/                                 
│   ├── fps_converter.py
│   ├── cropper.py
│   ├── freeze_detector.py
│   ├── ocr_text_detector.py
│   ├── template_matcher.py
│   └── mkv_to_mp4_converter.py
│
├── sample_data/                             
│   ├── sample.mkv
│   ├── coords.json
│   ├── template.jpg
│   └── workflow.json
│
├── output/                                  
│   ├── video_1fps.mp4
│   ├── cropped_videos/
│   ├── freeze_frames.txt
│   ├── detected_text.csv
│   ├── template_matches.csv
│   └── converted_video.mp4
│
├── requirements.txt                       
└── README.md                               
```

---

##  Inputs

All input files are stored in the `sample_data/` directory.

| File              | Purpose                                        |
|-------------------|------------------------------------------------|
| `sample.mkv`      | Main video file                                |
| `coords.json`     | JSON file containing crop coordinates          |
| `template.jpg`    | Image template to search for in cropped frames |



---

## Outputs

All outputs are saved in the `/output/` directory.

| File/Folder              | Description                             |
|--------------------------|-----------------------------------------|
| `video_1fps.mp4`         | Video downsampled to 1 FPS              |
| `cropped_videos/`        | Folder containing cropped video clips   |
| `freeze_frames.txt`      | Frame indexes that appear frozen        |
| `detected_text.csv`      | OCR results per frame                   |
| `template_matches.csv`   | Frames matching the input template      |
| `converted_video.mp4`    | MKV converted to MP4                    |


---

## DAG Overview

The pipeline runs in the following order:

```
[1] Convert to 1 FPS
 ├─> [2] Crop Videos
 │     └─> [5] Template Matching
 └─> [4] Text Detection
[3] Freeze Frame Detection
[6] MKV to MP4 Conversion
```

Some tasks run in parallel (e.g., text detection and cropping), while others depend on outputs from earlier steps.
