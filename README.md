# ALEX - Advanced Learning and Execution Interface

ALEX is an extensible AI assistant framework built in Python, featuring a modular skill system, voice capabilities, and multi-language support. It's designed to be easily extensible through a robust skill system while maintaining core assistant functionalities.

## 🌟 Features

- **Modular Skill System**: Easy-to-create custom skills with built-in intent recognition
- **Voice Interaction**: Full voice command support with customizable voice responses
- **Multi-Language Support**: Built-in translation system (currently supporting English and Portuguese)
- **Flexible Interface Modes**: 
  - Command Line (cmd)
  - Web Interface
  - Voice Interface
  - API Interface (in development)
- **Process Management**: Advanced process handling with scheduling capabilities
- **Context Management**: Built-in context system for maintaining conversation state
- **Event System**: Notification and event handling system

## 🚀 Prerequisites

- Python 3.12+
- [AlexBaseServer](https://github.com/Apoll011/AlexBaseServer)
- pip package manager

## 📦 Installation

1. Install the AlexBaseServer:
```bash
git clone https://github.com/Apoll011/AlexBaseServer
cd AlexBaseServer
# Follow AlexBaseServer installation instructions
```

2. Install ALEX dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Getting Started

Run ALEX with different configurations:

```bash
# Basic start
python -m alex -s

# Start with voice mode
python -m alex -s --voice

# Start with web interface
python -m alex -s -i web

# Start with different language
python -m alex -s -l pt

# Debug mode
python -m alex -s -d
```

## 🛠️ Creating Custom Skills

ALEX uses a skill-based system for extending functionality. Here's how to create a custom skill:

```python
from core.skills import BaseSkill

class MyCustomSkill(BaseSkill):
    def init(self):
        # Register the skill with namespace@skillname format
        self.register("example@custom.skill")
        # Set if the skill can be triggered multiple times
        self.can_go_again = True

    def execute(self, intent):
        # Must call parent execute
        super().execute(intent)
        
        # Access slots if needed
        if self.slot_exists("user_input"):
            user_value = self.get("user_input")
            
        # Respond using translation system
        self.say("response_key", variable=value)
        # Or respond directly
        self.responce("Direct response")
```

### Key Skill Features:

1. **Slot Management**:
```python
# Required slots
self.require("slot_name")
# Optional slots
self.optional("slot_name")
```

2. **Context Management**:
```python
# Save context
self.alex_context.save(data, "key")
# Load context
data = self.alex_context.load("key")
```

3. **Translation Support**:
```python
# Add translations in skill's assets/locale directory
self.say("translation.key", variable="value")
```

4. **Event System**:
```python
from core.notifier import AlexEvent

event = AlexEvent("event_name", data)
self.register_event(event)
```

## 💡 Architecture

ALEX is built with several key components:
- **Process System**: Handles input processing and skill execution
- **Intent System**: Manages intent recognition and routing
- **Interface System**: Provides different interaction modes
- **Translation System**: Handles multi-language support
- **Context Manager**: Maintains conversation state
- **Event System**: Handles asynchronous events and notifications

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

> **Note**: This project is actively under development. Some features may be subject to change.