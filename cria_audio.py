from gtts import gTTS
from playsound import playsound

def cria_audio(audio, audio_name):
    tts = gTTS(audio, lang='pt-br')
    path = 'audios/' + audio_name
    tts.save(path)
    playsound(path)

cria_audio('Espera aí', 'feedback.mp3')
cria_audio('Espera aí', 'feedback1.mp3')