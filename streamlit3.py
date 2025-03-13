import streamlit as st
import av
import ggwave
import numpy as np
import pyaudio
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

# GGWave Decoder (Receiver)
class AudioReceiver(AudioProcessorBase):
    def __init__(self):
        self.gg_instance = ggwave.init()

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        """Receive and decode GGWave sound in real-time"""
        audio_np = np.array(frame.to_ndarray(), dtype=np.float32)
        decoded_message = ggwave.decode(self.gg_instance, audio_np.tobytes())
        print(decoded_message)

        if decoded_message:
            try:
                received_text = decoded_message.decode('utf-8')
                st.session_state["received_text"] = received_text  # Store in session state
            except:
                pass
        return frame

# GGWave Encoder (Transmitter)
class AudioTransmitter:
    def __init__(self):
        self.gg_instance = ggwave.init()

    def encode_message(self, message):
        """Ensure message is a string and encode it into GGWave audio signal"""
        message = str(message)  # Convert to string if it's an integer
        
        return np.frombuffer(ggwave.encode(message, protocolId=1, volume=100), dtype=np.float32)

def main():
    st.title("🔊 Real-Time Audio Transmission")

    message = st.text_input("Enter text to transmit:")
    if "received_text" not in st.session_state:
        st.session_state["received_text"] = "No message received yet."

    # Send Audio
    if st.button("Send Audio"):
        transmitter = AudioTransmitter()  # Now correctly defined
        audio_signal = transmitter.encode_message(message)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True)
        stream.write(audio_signal.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()
        st.success("✅ Sound transmitted!")

    # Live Audio Receiver (WebRTC)
    st.header("🎙️ Live Audio Receiver")
    webrtc_ctx = webrtc_streamer(
        key="receive_audio",
        mode=WebRtcMode.RECVONLY,
        audio_processor_factory=AudioReceiver
    )

    # Display received message
    st.subheader("📥 Received Message:")
    st.write(st.session_state["received_text"])


if __name__ == "__main__":
    main()
