from Echo.Echo import listen, keyboard, speak
from Core.Core import processInput
from Utils.Config import ASSISTANT_NAME, VERBOSE


def getInput(mode):
    return listen() if mode == "voice" else keyboard()

if __name__ == "__main__":
    # Choose mode at the start (could be command line, menu, or flag)
    mode = input("Type 'v' for voice or 'k' for keyboard input: ").strip().lower()
    mode = "voice" if mode == "v" else "keyboard"

    while True:
        userInput = getInput(mode)
        if userInput is None:
            continue
        if userInput in ["exit", "quit", "q"]:
            speak("Exiting. Goodbye!")
            break
        response = processInput(userInput, verbose=VERBOSE)
        if mode == "voice":
            speak(response)
        else:
            print(f"{ASSISTANT_NAME.title()}:\n{response}\n")
