#Slappy Raspi 3b
import sounddevice as sd
import soundfile as sf
import random
import RPi.GPIO as GPIO
import time
from time import strftime
import numpy as np
from piper.voice import PiperVoice
import psutil #cpu info
import httplib2
import json

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

model =  "en_US-hfc_male-medium.onnx"
print ("model =  en_US-hfc_male-medium.onnx")

import sounddevice as sd
from piper.voice import PiperVoice

voicedir = "/home/pi/pipertts/lib/python3.11/site-packages/piper/" #Where onnx model files are stored
model = voicedir+"en_US-hfc_male-medium.onnx"
voice = PiperVoice.load(model)
print ("voice loaded")

SWITCH1_PIN = 20
SWITCH2_PIN = 21
SWITCH3_PIN = 18
BUTTON_PIN = 25
PIR_PIN = 23
AWAKE_PIN = 4
TALKING_PIN = 24
LEDRED_PIN = 17 # MOSFET "3" for cabinet lights
LEDBLUE_PIN = 27 # MOSFET "2" for cabinet lights
LEDWHITE_PIN = 22 # MOSFET "1" for cabinet lights
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #channel numbers on the Broadcom SOC
GPIO.setup(SWITCH1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(TALKING_PIN, GPIO.OUT)
GPIO.setup(AWAKE_PIN, GPIO.OUT)
GPIO.setup(LEDRED_PIN, GPIO.OUT)
GPIO.setup(LEDBLUE_PIN, GPIO.OUT)
GPIO.setup(LEDWHITE_PIN, GPIO.OUT)

PIR_current_time = time.time()
PIR_start_time = time.time()
PIR_total_time=0
loop_start_time=0

MOTION=False
nightMode=False

cycle = 0 #cycles through talking fxn

def playJoke():
    thisloop_start_time=time.time()
    url="https://v2.jokeapi.dev/joke/Misc,Dark,Pun,Spooky?type=twopart&blacklistFlags=racist"
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request(url, "GET")
    content = content.decode("utf-8")
    jokeJson = json.loads(content)
    setup=jokeJson["setup"]
    delivery=jokeJson["delivery"]
    print(jokeJson["setup"])
    print(jokeJson["delivery"])
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    print ("done setting up stream")

    stream.start()
    piperFlag=False #if first line faila to read
    try:
        for audio_bytes in voice.synthesize_stream_raw(setup):
                int_data = np.frombuffer(audio_bytes, dtype=np.int16)
                stream.write(int_data)
    except:
            print("Something else went wrong")
            piperFlag=True
            stream.stop()
            stream.close()
            stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    stream.stop()

    if(piperFlag==False):
        stream.start()
        try:
            for audio_bytes in voice.synthesize_stream_raw(delivery):
                int_data = np.frombuffer(audio_bytes, dtype=np.int16)
                stream.write(int_data)
        except:
            print("Something else went wrong")
            stream.stop()
            stream.close()
            stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
        stream.stop()
    
    stream.close()
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("playJoke time: ", thisloop_total_time)

def playJoke2():
    thisloop_start_time=time.time()
    url="https://plurimediagroup.com/get_json_data_jokes-api.php"
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request(url, "GET")
    content = content.decode("utf-8")
    getHTML_end_time=time.time()
    getHTML_total_time = int(getHTML_end_time)-int(thisloop_start_time)
    
    print("Joke: ",content)
    
    stream_setup_start_time=time.time()
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    print ("done setting up stream")
    stream_setup_end_time=time.time()
    stream_setup_total_time = int(stream_setup_end_time)-int(stream_setup_start_time)
    
    stream_start_start_time=time.time()
    stream.start()
    try:
        for audio_bytes in voice.synthesize_stream_raw(content):
                int_data = np.frombuffer(audio_bytes, dtype=np.int16)
                stream.write(int_data)
    except:
            print("Something else went wrong")
            stream.stop()
            stream.close()
            playSlappy()
    stream.stop()   
    stream_start_end_time=time.time()
    stream_start_total_time = int(stream_start_end_time)-int(stream_start_start_time)
    stream.close()
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("getHTML_total_time: ", getHTML_total_time)
    print ("stream_setup_total_time time: ", stream_setup_total_time)
    print ("stream_start_total_time time: ", stream_start_total_time)
    print ("thisloop_total_time time: ", thisloop_total_time)


def playNews():
    thisloop_start_time=time.time()
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("https://plurimediagroup.com/get_json_data_newsapi.php", "GET")
    content = content.decode("utf-8")
    #print (content)
    # Create an empty Array
    arr_str = []
    arr_str = content.split('<p>')
    print ("set up stream")
    # Setup a sounddevice OutputStream with appropriate parameters
    # The sample rate and channels should match the properties of the PCM data
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    print ("done setting up stream")
    i=0;
    for title in arr_str:
        print("speaking titles: ", title)
        stream.start()
        try:
            for audio_bytes in voice.synthesize_stream_raw(title):
                int_data = np.frombuffer(audio_bytes, dtype=np.int16)
                stream.write(int_data)
        except:
            print("Something else went wrong")
            stream.stop()
            stream.close()
            stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
        stream.stop()
        i = i+1
        print("i: ",i)
        if(i>=4):
            break #just read 4 healines
    stream.close()
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("playNews time: ", thisloop_total_time)
    
def playLaugh():
    thisloop_start_time=time.time()
    slappywav = [] #declare list
    slappywav = ["slappy_laugh1.mp3",\
"slappy_laugh2.mp3",\
"slappy_laugh3.mp3",\
"slappy_laugh4.mp3",\
"slappy_laugh5.mp3",\
"slappy_laugh6.mp3",\
"slappy_laugh7.mp3"]
    listLength = len(slappywav)
    indexToPlay = random.randint(0,listLength-1)
    fileToPlay = slappywav[indexToPlay]
    print("playing: ",fileToPlay)
    try:
        data, fs = sf.read(fileToPlay)
        sd.play(data, fs)
        sd.wait()
    except:
        print("Something else went wrong playing: ",fileToPlay)
    time.sleep(2)    
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("playLaugh time: ", thisloop_total_time)
    
def playSlappy():
    thisloop_start_time=time.time()
    slappywav = [] #declare list
    slappywav = ["didyahmissme_slappy_JackBlack.mp3",\
"dummy_slappy_JackBlack.mp3",\
"hello_slappy_JackBlack.mp3",\
"pulling_strings_slappy_JackBlack.mp3",\
"slappy_unhappy_slappy_JackBlack.mp3"]
    listLength = len(slappywav)
    indexToPlay = random.randint(0,listLength-1)
    fileToPlay = slappywav[indexToPlay]
    print("playing: ",fileToPlay)
    try:
        data, fs = sf.read(fileToPlay)
        sd.play(data, fs)
        sd.wait()
    except:
        print("Something else went wrong playing: ",fileToPlay)
    time.sleep(2)
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("playSlappy time: ", thisloop_total_time)
    
def playSlappyIntro():
    thisloop_start_time=time.time()
    fileToPlay = "hello_slappy_JackBlack.mp3"
    print("playing: ",fileToPlay)
    try:
        data, fs = sf.read(fileToPlay)
        sd.play(data, fs)
        sd.wait()
    except:
        print("Something else went wrong playing: ",fileToPlay)
    time.sleep(4)
    fileToPlay = "didyahmissme_slappy_JackBlack.mp3"
    print("playing: ",fileToPlay)
    try:
        data, fs = sf.read(fileToPlay)
        sd.play(data, fs)
        sd.wait()
    except:
        print("Something else went wrong playing: ",fileToPlay)
    time.sleep(4)
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("playSlappyIntro time: ", thisloop_total_time)
    
def getTime():
    thisloop_start_time=time.time()
    hour = strftime("%-H")
    minute = strftime("%M")
    am_pm = strftime("%p")
    day = strftime("%d")    # Results in '23'
    month = strftime("%B")  # Results in 'October'
    whole_date = strftime("%d/%m/%y")   # Results in '23/10/17'
    full_datetime = strftime("%d/%m/%y at %-H:%M%p") # Results in 23/10/17 at 09:20AM
    #print("hour: ",hour, "type: ",type(hour))
    return hour
    #print("full_datetime: ",full_datetime," hour: ",hour,"am_pm: ",am_pm)
    thisloop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    thisloop_total_time = int(thisloop_end_time)-int(thisloop_start_time)
    print ("getTime time: ", thisloop_total_time)
    
    
GPIO.output(LEDWHITE_PIN, GPIO.LOW)
GPIO.output(LEDBLUE_PIN, GPIO.LOW)
GPIO.output(LEDRED_PIN, GPIO.LOW)
minute = strftime("%M")
intOldMin = int(minute)
second = strftime("%S")
intOldSec = int(second)
   
while (True):
    hour = getTime() #reurn RTC hour in 24 hour time as string
    minute = strftime("%M")
    second = strftime("%S")
    intHour = int(hour)
    intMin = int(minute)
    intSec = int(second)
    if(intMin!=intOldMin):
        #playLaugh()
        minute = strftime("%M")
        intOldMin = int(minute)
    if(intHour >= 23 or intHour <=8):
        nightMode = True
    else:
        nightMode = False
    PIRState=GPIO.input(PIR_PIN)
    if GPIO.input(PIR_PIN):
        #print('PIR Input was HIGH')
        PIR_start_time = time.time()
        PIR_total_time = 0
        MOTION=True
        GPIO.output(AWAKE_PIN, GPIO.HIGH)
    else:
        #print('PIR Input was LOW')
        PIR_current_time = time.time()
        PIR_total_time = int(PIR_current_time)-int(PIR_start_time)        
    #print("PIR_total_time:", PIR_total_time)
    if(PIR_total_time<60 and MOTION==True):
        #print('MOTION')
        GPIO.output(AWAKE_PIN, GPIO.HIGH)
        GPIO.output(LEDWHITE_PIN, GPIO.HIGH)
        PIR_current_time = time.time()
        PIR_total_time = int(PIR_current_time)-int(PIR_start_time)
    else:
        #print('NO MOTION')
        GPIO.output(LEDWHITE_PIN, GPIO.LOW)
        MOTION=False
    button1State=GPIO.input(BUTTON_PIN)
    switch1State=GPIO.input(SWITCH1_PIN)
    switch2State=GPIO.input(SWITCH2_PIN)
    switch3State=GPIO.input(SWITCH3_PIN)
    #print("PIR_total_time: ",PIR_total_time)
    if(PIR_total_time >= 60):
        cycle = 0
        GPIO.output(AWAKE_PIN, GPIO.LOW)
        #print('set cycle = 0 every 60 sec (1 min) without movement')
    if(intSec!=intOldSec):
        #print('MOTION: ', MOTION, ', SW1: ',switch1State, 'SW2: ', switch2State,', SW3: ',switch3State, ', butt: ',button1State)
        second = strftime("%S")
        intOldSec = int(second)    
    if((MOTION==True) and (cycle==0)):
        GPIO.output(AWAKE_PIN, GPIO.HIGH)
        GPIO.output(LEDWHITE_PIN, GPIO.HIGH)
        loop_start_time = time.time()
        #print("START: Current processor time (in seconds):", loop_start_time)
        #print ("minutes: ",time.strftime("%M"),", seconds: ",time.strftime("%S"))
        
        playSlappyIntro()
        playLaugh()
        time.sleep(5)
        
        if(switch1State==True): #Jokes
            cycle = 1
            print('SW1 Active')
            print('Jokes, set TALKING_PIN HIGH')
            GPIO.output(LEDWHITE_PIN, GPIO.LOW)
            GPIO.output(LEDBLUE_PIN, GPIO.HIGH)
            GPIO.output(TALKING_PIN, GPIO.HIGH)
            if(nightMode == False):
                playJoke2()
                time.sleep(2)
            GPIO.output(LEDBLUE_PIN, GPIO.LOW)
            GPIO.output(LEDRED_PIN, GPIO.HIGH)
            if(nightMode == False):
                playLaugh()
                time.sleep(60)
            print('Done SLAPPY, set TALKING_PIN LOW')
            GPIO.output(LEDRED_PIN, GPIO.LOW)
            GPIO.output(LEDWHITE_PIN, GPIO.HIGH)
            GPIO.output(TALKING_PIN, GPIO.LOW)
        if(switch2State==True):  #News
            cycle = 1
            print('SW2 Active')
            print('News, set TALKING_PIN HIGH')
            GPIO.output(LEDRED_PIN, GPIO.HIGH)
            GPIO.output(LEDBLUE_PIN, GPIO.HIGH)
            GPIO.output(TALKING_PIN, GPIO.HIGH)  
            if(nightMode == False):
                playNews()
            print('Done SLAPPY, set TALKING_PIN LOW')
            GPIO.output(TALKING_PIN, GPIO.LOW)
            GPIO.output(LEDRED_PIN, GPIO.LOW)
            GPIO.output(LEDBLUE_PIN, GPIO.LOW)
        if(switch3State==True):  #Slappy
            cycle = 1
            print('SW3 Active')
            print('SLAPPY, set TALKING_PIN HIGH')
            GPIO.output(LEDWHITE_PIN, GPIO.LOW)
            GPIO.output(LEDRED_PIN, GPIO.HIGH)
            GPIO.output(TALKING_PIN, GPIO.HIGH)
            if(nightMode == False):
                playSlappy()
            print('Done SLAPPY, set TALKING_PIN LOW')
            GPIO.output(TALKING_PIN, GPIO.LOW)
            GPIO.output(LEDRED_PIN, GPIO.LOW)
            GPIO.output(LEDWHITE_PIN, GPIO.HIGH)
    if(button1State==True):
        print('No switches active, button pushed')
        print('Get one joke')
        GPIO.output(LEDWHITE_PIN, GPIO.LOW)
        GPIO.output(LEDBLUE_PIN, GPIO.HIGH)
        GPIO.output(TALKING_PIN, GPIO.HIGH)
        playJoke()
        print('Done SLAPPY, set TALKING_PIN LOW')
        GPIO.output(TALKING_PIN, GPIO.LOW)
        GPIO.output(LEDBLUE_PIN, GPIO.LOW)
        GPIO.output(LEDWHITE_PIN, GPIO.HIGH)           
    #print('Set LEDWHITE_PIN LOW')
    GPIO.output(LEDWHITE_PIN, GPIO.LOW)
    #GPIO.output(TALKING_PIN, GPIO.LOW)
    loop_end_time = time.time()
    #print("END: Current processor time (in seconds):", loop_end_time)
    loop_total_time = int(loop_end_time)-int(loop_start_time)
    #print("cycle: ", cycle, ", nightMode: ",nightMode,", TALKING_PIN: ", GPIO.input(TALKING_PIN),", AWAKE_PIN: ", GPIO.input(AWAKE_PIN))


GPIO.cleanup()