import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Adjust this value to set your desired audio threshold
volume_threshold = 4000

while True:
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)

        try:
            # Check if the audio volume exceeds the threshold
            if max(audio.get_data()) > volume_threshold:
                recognized_text = recognizer.recognize_google(audio)
                print("You said: " + recognized_text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition; {0}".format(e))
