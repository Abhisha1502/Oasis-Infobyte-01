import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# You can change index for different voices (0 for male, 1 for female on most systems)
# Experiment with voices[0].id or voices[1].id based on what sounds best
engine.setProperty('voice', voices[1].id)

def speak(audio):
    """Speaks the given audio string."""
    engine.say(audio)
    engine.runAndWait()

def recognize_speech():
    """Listens for audio input from the microphone and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        # Adjust for ambient noise for 1 second. This helps filter out background noise.
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        recognizer.pause_threshold = 1 # Seconds of non-speaking audio before a phrase is considered complete
        audio = recognizer.listen(source)

    try:
        print("Audio captured. Attempting to recognize...")
        # Use 'en-in' for Indian English, or 'en-us' for US English, etc.
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio (UnknownValueError)")
        return "None"
    except sr.RequestError as e:
        # This usually means no internet connection or Google API issues
        print(f"Could not request results from Google Speech Recognition service; check your internet connection or API limits: {e}")
        return "None"
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred during speech recognition: {e}")
        print("Say that again please...")
        return "None"
    return query.lower()

def run_assistant():
    """Main function to run the voice assistant."""
    speak("Hello! How can I help you today?")
    while True:
        query = recognize_speech()

        # Handle "None" return from recognize_speech to avoid errors
        if query == "none":
            continue # Skip to the next iteration if nothing was recognized

        if "hello" in query:
            speak("Hello there! Nice to meet you.")

        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "date" in query:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today's date is {current_date}")

        elif "search" in query:
            speak("What do you want me to search for?")
            search_query = recognize_speech()
            if search_query != "none":
                speak(f"Searching for {search_query} on the web.")
                pywhatkit.search(search_query)

        elif "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye! Have a great day.")
            break
        
        else: # Optional: give feedback if command is not understood
            print("Command not recognized. Please try again.")
            # speak("I didn't understand that command. Can you please repeat?")

if __name__ == "__main__":
    run_assistant()


    