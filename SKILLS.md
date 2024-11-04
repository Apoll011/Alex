# ALEX Skill Creation Guide
>This guide covers the core features of the ALEX skill system. For specific use cases or advanced implementations, refer to the existing skills in the codebase as examples.

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
        self.register("namespace@my.skill")
        
    def execute(self, intent):
        super().execute(intent)
        # Skill logic here
```
### Naming
The naming of a skill class name will depend on the minor part of its intent name major@minor its allways capital Minor and replace minor.subminor with MinorSubMinor other separators like minor_subminor will be Minor_subminor.

The same logic is applied to the folder naming. remebering minor and major are different folder and the name its in lower case, All teh rules above are applied here too. 

### File Structure

For a skill of the intent play@game its file structure would be:

```text
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
    self.voice = "Jarvis" # The name you want alex to respond with
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
        raw = self.get("slot_name", raw = True)  # Get raw input without processing like 'one' instead of 1
    
    # Slot validation
    if self.assert_equal("slot_name", "expected_value"):
        # Do something
        pass
    if self.assert_in("slot_name", ["option1", "option2"]):
        # Do something
        pass
    if self.assert_in_dict("slot_name", my_dictionary):
        # Do something
        pass
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
```

## Context Management

Managing conversation context:

```python
# Save data to context
self.context_save("context_key", data)

# Load data from context
data = self.context_load("context_key")
```

## Translation System

Working with translations:

```text
# Structure in assets/locale.en.lang:
greeting:Hello {name}!
confirm:Are you sure?
multiple.random.responce:[Responce One; Responce Two;Etc]
```

```python
# In your skill:
def execute(self, intent):
    super().execute(intent)
    
    # Using translations
    self.say("greeting", name="User")
    
    # Direct translation access
    greeting = self.get_translation("greeting", {"name": "User"})
```

## Event System

Handle asynchronous events:

Be aware the the event should be registered in alex Notification system.

```python
from core.notifier import AlexEvent

def execute(self, intent):
    super().execute(intent)
    
    # Create and register event
    event = AlexEvent.ALEX_INTERNET_CALL
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
    "hidden_config": "tw3re4yt53tw-64wets-e5rdf5ry5rt-ew", // This configs only the skill can have access
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
            "value": true,
            "default": false
        },
        "message": {
            "type": "text",
            "value": "Hello",
            "default": "Hi" // If value is null
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
    
    #Access setting values (SEtting values are avaliable only for the skill, unlike the config with the user will be able to change using an interface.)
    api_key = self.setting("hidden_config")
    
    #Save a new value on a normal setting
    self.save_setting("hidden_config", "ytuewfd-grsdv34gr-g4wrsd34gwey4twe")
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
        
        self.play_audio(audio_path) #Play that sound
    except FileNotFoundError:
        self.say("asset.not.found")
```

## User Interaction

Managing user interaction flow:

```python
def execute(self, intent):
    super().execute(intent)
    
    # Get attention before important action
    self.request_attention()  # Will call user's name and wait a few seconds before continuing
    
    # Ask question and handle response
    self.question(
        "question.key",  # Translation key for question
        self.handle_response,  # Callback function
        {"variable": "value"},  # Translation variables
        ListResponce(["cake", "pizza", "hamburger"]),  # Expected response type can be anyresponce (Litterally anything. default) boolresponce(Yes: True or No: False) etc there are a lot of responce types.
        "additional_arg"  # Extra arguments the callback function
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
    
    # Access skill directory
    skill_path = self.dir()
    
    # Access current language
    current_lang = self.get_language()
```

## Best Practices

1. **Error Handling**:
- Most of the thrown errors are handled by the Input Processor (Processor class) be its better for the skill if it caught some of the known error for a smoother user experience.

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

> **Note**: When developing skills, always:
> - Test with different language settings
> - Handle missing slots gracefully
> - Provide clear user feedback
> - Clean up resources properly
> - Document usage and requirements

