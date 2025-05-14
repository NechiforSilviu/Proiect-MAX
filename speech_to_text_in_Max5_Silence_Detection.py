# Programmed by Gregg Mazel on 1/22/2025
# Recognize speech and send to max msp

import time
from pythonosc import udp_client
import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone {index}: {name}")


# OSC client setup for Max MSP
UDP_IP = "127.0.0.1"  # IP address of Max MSP
UDP_PORT = 54321      # Port Max MSP is listening on
client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)

# Initialize the recognizer and set up the microphone
recognizer = sr.Recognizer()

MIC_INDEX = 1  # Replace with the index of your desired microphone

def recognize_and_send():
    """Recognize speech and send the result to Max MSP."""
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            print("Microphone initialized. Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Listening for speech...")

            # Capture audio only if there is speech
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Audio recorded. Recognizing speech...")

            # Perform speech recognition
            text = recognizer.recognize_google(audio)
            text_upper = text.upper()  # Convert the recognized text to uppercase

            print(f"Recognized text: {text_upper}")

            # Send to Max MSP
            print(f"Sending to Max MSP: {text_upper}")
            client.send_message("/speech", text_upper)  # Sending message to Max via OSC

            # Send bang to Max MSP
            print("Sending bang to Max MSP.")
            client.send_message("/bang", 1)  # Max interprets this as a bang

    except sr.WaitTimeoutError:
        print("No speech detected. Waiting...")
    except sr.UnknownValueError:
        print("Speech recognition failed. Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from the service; {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main loop for continuous processing
print("Starting persistent speech-to-text processing with silence detection. Press Ctrl+C to stop.")
try:
    while True:
        recognize_and_send()
        time.sleep(0.5)  # Small delay to avoid rapid looping
except KeyboardInterrupt:
    print("\nExiting. Goodbye!")
