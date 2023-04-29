from pynput import keyboard
import subprocess
import sys
import json

shift = False
micToggle = True

# Json config
with open('config.json') as user_file:
    file_contents = user_file.read()

parsed_json = json.loads(file_contents)
sound = parsed_json['sound']

def get_sound():
    return sound

subprocess.run('SoundVolumeView /Unmute "Capture"', shell=True)

def get_micToggle():
    return micToggle

def set_micToggle(m):
    global micToggle
    micToggle = m

def get_shift():
    return shift

def set_shift(s):
    global shift
    shift = s

def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'shift':
        set_shift(True)
    if k in ['f1', 'f2', 'f3', 'f12']:  # keys of interest
        if get_shift() == True:
            match k:
                case 'f1':
                    subprocess.run('nircmd setdefaultsounddevice "' + get_sound()[0]['device1output'] + '" 1', shell=True)
                    subprocess.run('nircmd setdefaultsounddevice "' + get_sound()[0]['device1input'] + '" 1', shell=True)
                    subprocess.run('nircmd setdefaultsounddevice "' + get_sound()[0]['device1input'] + '" 2', shell=True)
                case 'f2':
                    subprocess.run('nircmd setdefaultsounddevice "' + get_sound()[1]['device2output'] + '" 1', shell=True)
                    subprocess.run('nircmd setdefaultsounddevice "' + get_sound()[1]['device2input'] + '" 1', shell=True)
                    subprocess.run('nircmd setdefaultsounddevice "' + get_sound()[1]['device2input'] + '" 2', shell=True)
                case 'f3':
                    if get_micToggle() == True:
                        subprocess.run('SoundVolumeView /Mute "DefaultCaptureDevice"', shell=True)
                        set_micToggle(False)
                    else:
                        subprocess.run('SoundVolumeView /Unmute "DefaultCaptureDevice"', shell=True)
                        set_micToggle(True)
                case 'f12':
                    sys.exit()

def on_release(key):
    try:
        kr = key.char  # single-char keys
    except:
        kr = key.name  # other keys
    if kr == 'shift':
        set_shift(False)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys
