# ALEX Skill Creation Guide

## Table of Contents
- [Basic Structure](#basic-structure)
- [Registration & Initialization](#registration--initialization)
- [Slot Management](#slot-management)
- [Response System](#response-system)
- [Context Management](#context-management)
- [Translation System](#translation-system)
- [Event System](#event-system)
- [API Integration](#api-integration)
- [Configuration Management](#configuration-management)
- [Asset Management](#asset-management)
- [User Interaction](#user-interaction)
- [Advanced Features](#advanced-features)

## Basic Structure


Every ALEX skill must inherit from `BaseSkill`:

```python
from core.skills import BaseSkill

class MySkill(BaseSkill):
    def init(self):
        self.register("namespace@skill.name")
        
    def execute(self, intent):
        super().execute(intent)
        # Skill logic here
```
### Naming
The naming of a skill class name will depend on the minor part of its intent name major@minor its allways capital Minor and replace minor.subminor with MinorSubMinor other separators like minor_subminor will be Minor_subminor

### File Structure

For a skill of the intent play@game its file structure would be:

```commandline
skills/
    - (...)
    - play/
        - (Other play skills)
        - game/
            - asset/
                - locale.en.lang
                - locale.pt.lang
                - asset.png
            - .config
            - __main__.py
```

## Registration & Initialization

```python
def init(self):
    # Basic registration
    self.register("namespace@skill.name")
    
    # Control repeat behavior
    self.can_go_again = False  # Prevent skill from being triggered multiple times when user ask for repeat an action like generate another number
    self.can_repeat_responce = False  # Prevent last response from being saved and being said when user ask to alex reapeat the last sentence in case he does not hear properly
```

## Slot Management

Slots are input parameters for your skill:

```python
def execute(self, intent):
    super().execute(intent)
    
    # Required slots - will raise SkillSlotNotFound if missing
    self.require("slot_name")
    self.require("number_slot", SlotNumberValue)
    
    # Optional slots - won't raise if missing
    self.optional("optional_slot")
    
    # Accessing slot values
    if self.slot_exists("slot_name"):
        value = self.get("slot_name")  # Get processed value
        raw = self.get_raw_slot_value("slot_name")  # Get raw input without processing like 'one' instead of 1
    
    # Slot validation
    if self.assert_equal("slot_name", "expected_value"):
        # Do something
        
    if self.assert_in("slot_name", ["option1", "option2"]):
        # Do something
        
    if self.assert_in_dict("slot_name", my_dictionary):
        # Do something
```

## Response System

Multiple ways to respond to users:

```python
# Direct response
self.responce("Hello user!")

# Translated response
self.responce_translated("greeting.key", {"name": "User"})

# Shorthand for translated response
self.say("greeting.key", name="User")

# Advanced response with intent data
self.speak({
    "message": "Custom message",
    "custom_data": "value" # Like name witch will send a messege under another name  not Alex
})
```

## Context Management

Managing conversation context:

```python
# Save data to context
self.alex_context.save(data, "context_key")

# Load data from context
data = self.alex_context.load("context_key")
```

## Translation System

Working with translations:

```text
# Structure in assets/locale.en.json:
greeting:Hello {name}!
confirm:Are you sure?
muiltiple.random.responce:[Responce One; Responce Two;Etc]
```

```python
# In your skill:
def execute(self, intent):
    super().execute(intent)
    
    # Using translations
    self.say("greeting", name="User")
    
    # Direct translation access
    greeting = self.translate.get_translation("greeting", {"name": "User"})
```

## Event System

Handle asynchronous events:

Be aware the the event should be registered in alex Notification system.

```python
from core.notifier import AlexEvent

def execute(self, intent):
    super().execute(intent)
    
    # Create and register event
    event = AlexEvent("custom_event", {
        "data": "value",
        "timestamp": "2024-01-01"
    })
    self.register_event(event)
```

## API Integration

Making API calls:

```python
from core.client import ApiMethod

def execute(self, intent):
    super().execute(intent)
    
    # GET request
    response = self.api("endpoint/path")
    
    # POST request with data
    response = self.api(
        "endpoint/path", 
        method=ApiMethod.POST, 
        data="value",
        another_data=1
    )
```

## Configuration Management

Managing skill settings:

```json5
// Structure in .config file:
{
    "name_author": "Tiago",
    "hidden_config": "sfteryyer-64wets-e5rdf5ryrtew" // This configs only the skill can have access
    "config": { // Values that user will be able to change using an app (UNDER CONTRUCTION)
        "timeout": {
            "type": "number",
            "value": 30,
            "default": 60,
            "min": 0, // Optional
            "max": 120 // Optional
        },
        "enabled": {
            "type": "bool",
            "value": 1,
            "default": 0
        },
        "message": {
            "type": "text",
            "value": "Hello",
            "default": "Hi"
        }
    }
}
```
```python
# In your skill:
def execute(self, intent):
    super().execute(intent)
    
    # Access config values
    timeout = self.config("timeout")
    enabled = self.config("enabled")
    message = self.config("message")
    api_key = self.skill_settings["hidden_config"]
    
    # Save updated settings
    self.skill_settings["config"]["timeout"]["value"] = 45
    self.save_settings()
```

## Asset Management

Working with skill assets:

Assets are saved under the asset folder.

```python
def execute(self, intent):
    super().execute(intent)
    
    # Access asset file path
    try:
        audio_path = self.get_asset("sound.mp3")
        image_path = self.get_asset("icon.png")
    except FileNotFoundError:
        self.say("asset.not.found")
```

## User Interaction

Managing user interaction flow:

```python
def execute(self, intent):
    super().execute(intent)
    
    # Ask question and handle response
    self.question(
        "question.key",  # Translation key for question
        self.handle_response,  # Callback function
        {"variable": "value"},  # Translation variables
        ListResponce(["cake", "pizza", "etc"]),  # Expected response type can be anyresponce boolresponce etc there are a lot of responce types.
        "additional_arg"  # Extra arguments for callback
    )

def handle_response(self, responce, additional_arg):
    if responce == "cake": #Responce will be formated accordingly if asked for a BoolResponce respnce would be True or False deppending on the awnser 
        self.say("cake.response")
    else:
        self.say("pizza.response")
```

## Advanced Features

Additional useful features:

```python
def execute(self, intent):
    super().execute(intent)
    
    # Get attention before important action
    self.request_attention()  # Will call user's name and wait
    
    # Access alex instance
    alex = self.alex()
    
    # Access skill directory
    skill_path = self.skill_dir
    
    # Access current language
    current_lang = self.language
```

## Best Practices

1. **Error Handling**:
- Most of the trown erros are handled by the Input Processor (Processor class) be its better for the skill if it caught some of the known error for a smoother user experience.

2. **Translation Organization**:
- Keep translations in locale files
- Include all supported languages

3. **Context Management**:
- Clean up context when done
- Use descriptive context keys
- Don't store sensitive data

4. **Skill Settings**:
- Include default values
- Validate configuration values
- Document configuration options

5. **Documentation**:
```python
class MySkill(BaseSkill):
    """
    Skill Description
    
    Intents:
        - namespace@skill.name: Main intent
    
    Slots:
        - user_input: User provided input
        - action: Required action to perform
    
    Configuration:
        - timeout: Operation timeout in seconds
        - enabled: Feature toggle
    """
```

---

**Note**: When developing skills, always:
- Test with different language settings
- Handle missing slots gracefully
- Provide clear user feedback
- Clean up resources properly
- Document usage and requirements

This guide covers the core features of the ALEX skill system. For specific use cases or advanced implementations, refer to the existing skills in the codebase as examples.