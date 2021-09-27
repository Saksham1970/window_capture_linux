import pulsectl
import wave
import subprocess
import time
import settings
target_search = settings.target_search
duration = settings.duration
pulse = pulsectl.Pulse('my-client-name')

def sinkInputList_by_applicationName(applicationName):
    sinkInputList = []
    for sinkInput in pulse.sink_input_list():
        if applicationName in sinkInput.proplist["application.name"].lower():
            sinkInputList.append(sinkInput)
    return sinkInputList

def get_raw_audio_data(sinkInput, fps = 44100, channels = 2, depth = 2):
    dtd = {
        1: "u8",
        2: "s16ne",
        3: "s24ne",
        4: "s32ne"
    }

    index = sinkInput.index
    sp = subprocess.Popen(["parec", "--raw", f"--monitor-stream={index}", f"--rate={fps}", f"--channels={channels}", f"--format={dtd[depth]}"], stdout= subprocess.PIPE,stderr= subprocess.PIPE)
    rawAudioBuffer = sp.stdout
    return rawAudioBuffer , sp

def AudioBuffer_to_data(rawAudioBuffer , duration , fps = 44100, channels = 2, depth = 2):
    data= b""
    
    for line in rawAudioBuffer:
        if len(data) > fps*channels*depth*duration:
            break
        data += line       
    return data

def PCM_to_wav(data , filename, fps = 44100, channels = 2, depth = 2):
    with wave.open(f"{filename}.wav", "wb") as out_f:
        out_f.setnchannels(channels)
        out_f.setsampwidth(depth) 
        out_f.setframerate(fps)
        out_f.writeframesraw(data)


def record_audio_data(application_name, duration, fps = 44100, channels = 2, depth = 2):
    now = time.time()
    data = b""
    while True:
        sink_input_list = sinkInputList_by_applicationName(application_name)
        if sink_input_list:    
            print("got audio")
            sink_input = sink_input_list[0]
            AudioBuffer, subproc = get_raw_audio_data(sink_input,fps,channels,depth)
            break
        elif time.time() > now+duration:
            data = b"\x00"*int(fps*channels*depth*duration)
            break
    if not data:
        duration_left = duration - (time.time() - now)
        silence = b"\x00"*int(fps*channels*depth*(duration-duration_left)) 
        data = silence +  AudioBuffer_to_data(AudioBuffer,duration_left,fps,channels,depth)[1:]
        subproc.terminate()
    return data

def record_audio_wav(application_name, duration, filename,fps = 44100, channels = 2, depth = 2):

    data = record_audio_data(application_name, duration,fps, channels, depth)
    PCM_to_wav(data,filename,fps,channels,depth)

def record_sink_to_wav(sink_input,duration,filename,fps = 44100, channels =2, depth = 2):
    ab,sp = get_raw_audio_data(sink_input,fps,channels,depth)
    data = AudioBuffer_to_data(ab,duration,fps,channels,depth)
    PCM_to_wav(data,filename,fps,channels,depth)

if __name__ == "__main__":
    record_audio_wav("chrome",10,"sound")