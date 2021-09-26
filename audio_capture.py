import pulsectl
import wave
import subprocess
import time
import settings
target_search = settings.target_search
duration = settings.duration
pulse = pulsectl.Pulse('my-client-name')

def get_raw_audio_data(target):

    for sinkInput in pulse.sink_input_list():
        if target_search in sinkInput.proplist["application.name"].lower():
            global index
            index = sinkInput.index
            break
    else:
        index = None

    if index:
        sp = subprocess.Popen(["parec", "--raw", f"--monitor-stream={index}" ], stdout= subprocess.PIPE,stderr= subprocess.PIPE)
        out = sp.stdout
        return out , sp
    else:
        return None

def raw_PCM_to_wav(rawBufferStream , duration , filename):
    fps = 44100
    channels = 2
    depth = 2
    data= b""
    now = time.time()
 
    for line in rawBufferStream:
        if len(data) > fps*channels*depth*duration:
            break
        data += line       
   
    with wave.open(f"{filename}.wav", "wb") as out_f:
        out_f.setnchannels(channels)
        out_f.setsampwidth(depth) 
        out_f.setframerate(fps)
        out_f.writeframesraw(data)


if __name__ == "__main__":
    now = time.time()
    while True:
        raw_audio_tuple = get_raw_audio_data(target_search)
        if raw_audio_tuple:    
            print("got audio")
            rawBufferStream, subproc = raw_audio_tuple
            break
        elif time.time() > now+duration:
            print(duration, "expired")
            raise TimeoutError
    duration = duration - (time.time() - now)
    raw_PCM_to_wav(rawBufferStream, duration,"sound")
    subproc.terminate()
