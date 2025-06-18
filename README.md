
---

# Voice Assistant

A modular, extensible voice assistant with multi-provider LLM support (OpenAI, Google Gemini, and more) and skill-based action management. Supports both voice and keyboard input, with simple integration for custom skills.

---

## Features

* **Voice & Keyboard Modes:** Choose your input method at runtime.
* **Multi-Provider LLM:** Seamless switch between OpenAI, Google, and others (Anthropic, Ollama coming soon).
* **SkillGraph Architecture:** Plug-and-play skills system for flexible action handling.
* **Text-to-Speech (TTS):** Customizable voice output using `pyttsx4`.
* **Environment-based Config:** Easy API key and provider management via `.env`.
* **Simple API, Modular Design:** Production-grade, extensible code.

---

## Quick Start

### 1. **Clone & Install**

```sh
git clone https://github.com/yourusername/VoiceAssistant.git
cd VoiceAssistant
pip install -r requirements.txt
```

### 2. **Environment Setup**

Create a `.env` file in the project root with your keys:

```env
PROVIDER=openai # or 'google'
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
# ANTHROPIC_API_KEY=your_anthropic_api_key (optional)
# OLLAMA_API_KEY=your_ollama_api_key (optional)
SHOW_CAPABILITIES=False
SHOW_METADATA=False
```

### 3. **Configurable Options**

Edit `.env` to set your assistant’s name, gender, speaking rate, pitch, and volume.

---

## Usage

**Run the assistant:**

```sh
python main.py
```

* At startup, select your mode:

  * Type `'v'` for voice input
  * Type `'k'` for keyboard input

Say or type your request.

* To exit: type/say `exit`, `quit`, or `q`.

---

## Directory Structure

```
VoiceAssistant/
│
├── Echo/          # Input/output (voice, keyboard, TTS)
│   └── Echo.py
├── Core/          # Main processing logic
│   └── Core.py
├── Skills/        # Skills system (User, Agent skills)
│   ├── User/
│   └── Agent/
├── Utils/         # Configs and utilities
│   ├── Config.py
│   ├── SkillGraph.py # Skill management
│   └── ...
├── VoiceAssistant.py        # Entry point
└──requirements.txt
```

---

## Extending Skills

**Add custom skills:**
Place new skill classes in `Skills/User` or `Skills/Agent`.
Skill loading and execution is fully dynamic.

---

## Environment Variables

* `PROVIDER`: Choose `"openai"` or `"google"`.
* `*_API_KEY`: Your model provider’s API key.
* `SHOW_CAPABILITIES`, `SHOW_METADATA`: Enable for debugging skill info.

---

## Dependencies

* `openai`, `google-generativeai`
* `python-dotenv`
* `pyttsx4`, `SpeechRecognition`
* `SkillsManager` (install via `pip`)
* Python 3.9+

---

## Example Usage

**Keyboard:**

```
You: What’s the weather today?
Assistant: The weather today is sunny with a high of 25°C.
```

**Voice:**

* Speak: "Hey \[Assistant Name], what's on my calendar today?"

---

## Production Notes

* **Thread-safe, singleton SkillGraph** for reliable skill management.
* **Provider-agnostic API**: Switch between LLM providers without changing code.
* **Simple, robust error handling**: Never crashes on bad input.
* **Customizable voice personality** via config.

---

## FAQ

**Q:** How do I add new LLM providers or skills?
**A:**

* Add your API client code in `Core/Core.py`.
* Add skill classes under `Skills/User` or `Skills/Agent`.

**Q:** Does it require internet access?
**A:**

* Yes, for LLM requests. Local voice input/output works offline.

**Q:** Can I run it on Windows, Linux, Mac?
**A:**

* Yes, fully cross-platform. Optimized for Windows 11 / Surface devices.

---

## Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss your proposal.

---

## License

This project is licensed under the [Apache License, Version 2.0](LICENSE).
Copyright 2025 Tristan McBride Sr.

---

**Authors:**
- Tristan McBride Sr.
- Sybil

---

**Questions or issues?** Open an issue or pull request!

---

