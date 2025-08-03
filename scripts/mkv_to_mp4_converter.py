from moviepy.editor import VideoFileClip

def convert_mkv_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec="libx264")
