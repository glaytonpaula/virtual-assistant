import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import os

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
    if 'notícias' in trigger:
        ultimas_noticias()

    if 'giro' in trigger:
        cria_audio('O melhor Chapter do Giro é o contratação Gerente')
        print('O melhor Chapter do Giro é o contratação Gerente')

## funcoes de comandos ###
def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')

    for item in noticias.findAll('item')[:5]:
        mensagem = item.title.text
        index = 0
        index = index + 1
        print(mensagem)
        cria_audio(mensagem)



def main():
    while True:
        monitora_audio()

main()

#ultimas_noticias()