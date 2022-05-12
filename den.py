# Голосовой ассистент ДЕНИС 1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser
 
# настройки
opts = {
    "alias": ('дениска','денис','ден', 'дэн'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
        "stupid1": ('анекдот','ты знаешь анекдоты'),
        "exit": ('выключись', 'заткнись', 'перестань', 'выход'),
        "webbrowser_yandex": ("открой яндекс", "открой сайт яндекс"),
        "text_write": ("запиши", "запомни", "напиши"),
        "text_read": ("напечатай", "распечатай")
        
    }
}
 
# функции
class MySpeak():
    engine = None
    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        #self.engine.stop()

def speak(message):
    print(message)
    tmp = MySpeak()
    tmp.start(message)
    del(tmp)

 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            # обращаются к Дениске
            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd1 = cmd
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'], cmd1)
 
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")
 
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
        if c == "text_write" or c == "text_read":
            for x in v:
                vrt = fuzz.ratio(cmd[:cmd.find(" ")], x)
                if vrt > RC['percent']:
                    RC['cmd'] = c
                    RC['percent'] = vrt
        else:
            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > RC['percent']:
                    RC['cmd'] = c
                    RC['percent'] = vrt
    
    return RC
 
def execute_cmd(cmd, cmd1):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Зима, стоят мужики на остановке. Один достаёт сигарету и грит мол Огоньку не найдётся? Второй достаёт зажигалку, бензиновую, а она протекла по всей куртке. Чиркает, загорается вся рука. Ну а первый закуривает прям от руки: Ну, ты бл, фокусник!")
    elif cmd == 'webbrowser_yandex':
        webbrowser.open('https://yandex.ru', new = 2)
        speak("Открываю Яндекс")
    elif cmd == 'exit':
        # выход из программы
        speak("Клим Саныч! Потраченного времени жаль.")
        os._exit(1)
    elif cmd == 'text_write':
        #print("cmd1", cmd1)
        for x in opts["cmds"]["text_write"]:
            cmd1 = cmd1.replace(x, "").strip()
        direct = os.getcwd() 
        direct += "\example.txt"
        f = open(direct,'a', encoding='utf-8')
        f.write(cmd1 + '\n') 
        f.close()
        speak("Записал")
    elif cmd == 'text_read':
        #for x in opts["cmds"]["text_read"]:
         #   cmd1 = cmd1.replace(x, "").strip()
        direct = os.getcwd() 
        direct += "\example.txt"
        f = open(direct,'r', encoding='utf-8')
        print(f.read()) 
        speak("Печатаю")
        #print(f.read()) 
        f.close()
    else:
        print('Команда не распознана, повторите!')
 
# main
def den():
    r = sr.Recognizer()
    m = sr.Microphone(device_index = 1)
    cmd1 = ""
    #подавление шума 
    with m as source:
        r.adjust_for_ambient_noise(source)
 
    #speak_engine = pyttsx3.init()
 
    speak("Добрый день, повелитель")
    speak("Дениска слушает")
 
    stop_listening = r.listen_in_background(m, callback)
    while True: time.sleep(0.1) #infinity loop

if __name__  == '__main__':
    den()