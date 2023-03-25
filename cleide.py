import speech_recognition as sr
import os
import openai
from gtts import gTTS
from playsound import playsound
from datetime import datetime
from apikey import APIKEY
openai.api_key = APIKEY

##### CONFIGURACOES #####
hotword = 'cleide'

with open('cleide-python-assistente-add88c3fa973.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o comando!")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()
                print(trigger)
                if hotword in trigger:
                    print('Comando: ', trigger)
                    responde('feedback')
                    ###executar comandos
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))


def responde(resposta):
    path = 'audios/' + resposta + '.mp3'
    playsound(path)


def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')

    path = 'audios/' + str(datetime.now().timestamp()) + '.mp3'
    tts.save(path)
    playsound(path)
    os.remove(path)


def executa_comandos(trigger):
    response = aciona_gpt(trigger)
    cria_audio(response)

## funcoes de comandos ###

def aciona_gpt(trigger):
    text = trigger.split(hotword)
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content":
            text[1]}]
    )
    return output['choices'][0]['message']['content']


def main():
    while True:
        monitora_audio()


main()