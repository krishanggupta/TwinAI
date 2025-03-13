import ggwave
import pyaudio
import threading
import time
from gtts import gTTS
import io
import pygame
from playsound import playsound
import tempfile
from llm_class import ai2ai

class MyAIAgent:
    def __init__(self):
        self.receiving_sound = True
        self.p = pyaudio.PyAudio()

    def text_2_speech(self,language,message):
        language=language[:2]
        tts = gTTS(text=message, lang=language)  # 'fr' for French
        tts.save(f"{message.strip()}.mp3")  
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            playsound(temp_audio.name)

    def send_message(self, send_message):
        time.sleep(2)  # Delay to ensure receiving starts first
        waveform = ggwave.encode(send_message, protocolId=1, volume=100)
        print(f"Transmitting text: {send_message}")
        
        stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
        stream.write(waveform, len(waveform)//4)
        stream.stop_stream()
        stream.close()
        return send_message
    
    def receive_message(self):
        stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)
        print("Listening for incoming messages...")
        instance = ggwave.init()
        received_text='Error Occurred'
        try:
            while self.receiving_sound:
                data = stream.read(1024, exception_on_overflow=False)
                res = ggwave.decode(instance, data)
                if res:
                    try:
                        received_text=res.decode('utf-8')
                        #print(f"Received text: {received_text}")
                    except:
                        pass
        except KeyboardInterrupt:
            pass

        ggwave.free(instance)
        stream.stop_stream()
        stream.close()
        self.receiving_sound = False  # Stop receiving when done
        self.text_2_speech('en',received_text)
        print(f"Received text: {received_text}")
        return received_text

    def send_receive(self):
        thread_receive = threading.Thread(target=self.receive_message)
        thread_send = threading.Thread(target=self.send_message, args=("Hi! I am on a google meet.",))

        thread_receive.start()
        thread_send.start()

        thread_send.join()
        self.receiving_sound = False  # Stop receiving after sending is done
        thread_receive.join()

        self.p.terminate()
        print("Both processes completed.")

if __name__=='__main__':
    # Run the agent
    myagent = MyAIAgent()
    myagent.send_receive()
