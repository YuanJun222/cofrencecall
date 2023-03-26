import pandas as pd
import speech_recognition as sr
import wave
import subprocess

# ffmpeg를 사용하여 mp3 파일을 wav 파일로 변환
subprocess.call(['ffmpeg', '-i', '/content/Ray G. Young_1_10.mp3', '/content/Ray G. Young_1_10.wav'])

# 오디오 파일 경로 지정
filename = '/content/Ray G. Young_1_10.wav'

# recognizer 객체 생성
r = sr.Recognizer()

# 음성 파일 불러오기
with sr.AudioFile(filename) as source:
    audio_data = r.record(source)

# 음성 파일을 텍스트로 변환
text = r.recognize_google(audio_data, language='us-EN')

# wave 모듈로 wav 파일 열기
with wave.open(filename, 'rb') as wavfile:
    # 샘플 레이트와 채널 수 얻기
    framerate = wavfile.getframerate()
    nchannels = wavfile.getnchannels()
    # 총 프레임 수 계산
    nframes = wavfile.getnframes()
    # 오디오 파일 길이 계산
    duration = nframes / float(framerate)

# 단어 수 계산
word_count = len(text.split())

# speech rate 계산
speech_rate = word_count / duration

# 데이터프레임 생성
data = {'Text': [text],
        'Text Length': [len(text)],
        'WAV Duration (s)': [duration],
        'Speech Rate (wpm)': [speech_rate]}
df = pd.DataFrame(data)

# 엑셀 파일로 저장
df.to_excel('audio_data.xlsx', index=False)