# 1、使用moviepy模块 提取视频中的音频文件
from moviepy.editor import AudioFileClip

my_audio_clip = AudioFileClip(".\\examples\\demo\\ml.mp4")
print(type(my_audio_clip))  # <class 'moviepy.audio.io.AudioFileClip.AudioFileClip'>

#  提取视频中的音频文件  m4v,mp3等音频格式也是支持的
my_audio_clip.write_audiofile(".\\examples\\demo\\ml.mp3")
