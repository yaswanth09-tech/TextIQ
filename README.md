# TextIQ - AI Chat Assistant

TextIQ is a conversational AI application built with Streamlit and powered by Google's Gemini models. It provides an intuitive interface for interacting with AI, complete with chat history management, customizable settings, and a modern design that supports both dark and light themes.

---

## Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- A Google Gemini API key

### Installation Steps

1. **Clone or download the repository**
```bash
git clone <repository-url>
cd TextIQ
```

2. **Install required dependencies**
```bash
pip install -r requirements.txt
```

The application requires these packages:
- `streamlit>=1.32.0` - Web application framework
- `google-generativeai>=0.3.0` - Google Gemini AI integration
- `python-dotenv>=1.0.0` - Environment variable management

3. **Configure your API key**

Create a file named `.env` in the project root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

To obtain a free API key, visit [Google AI Studio](https://makersuite.google.com/app/apikey).

4. **Verify your setup (Recommended)**

Before launching the application, verify everything is configured correctly:

```bash
# Quick API key verification (5-10 seconds)
python test_api.py

# Comprehensive setup validation (15-30 seconds)
python testing.py quick
```

If all tests pass, proceed to the next step. If any tests fail, the scripts will provide specific instructions to fix the issues.

5. **Launch the application**
```bash
streamlit run app.py
```

The application will start and automatically open in your default browser at `http://localhost:8502`.

---

## Application Structure

The project follows a simple, organized structure:

```
TextIQ/
├── app.py                 # Main application code
├── test_api.py            # Quick API key verification tool
├── testing.py             # Comprehensive test suite
├── .env                   # API configuration (you create this)
├── .env.example           # Example configuration template
├── requirements.txt       # Python dependencies
├── chat_history.json      # Saved conversations (auto-generated)
├── README.md             # Documentation
└── QUICKSTART.md         # Quick setup guide
```

### Source Code Overview

The `app.py` file is structured into several key sections:

**Configuration Section** 
- Import statements and dependency checks
- Environment variable loading
- Model definitions and default settings
- Constants for chat history storage

**Chat History Functions** 
- `save_chat_history()` - Persists current conversation to JSON
- `load_all_chats()` - Retrieves all saved conversations
- `load_chat(chat_id)` - Loads a specific conversation
- `delete_chat(chat_id)` - Removes a conversation from history

**CSS Styling** 
- `load_custom_css(dark_mode)` - Applies theme-specific styles
- Dynamic color schemes for dark and light modes
- Custom chat bubble styling similar to modern messaging apps
- Responsive design elements

**AI Response Generation** 
- `generate_response()` - Handles API communication
- Message formatting for Gemini API
- Error handling for rate limits and API issues
- Response streaming and processing

**User Interface** 
- Session state initialization
- Sidebar controls and navigation
- Main chat area with message display
- Settings and history panels
- Chat input handling

---

## Features Explained

### Chat Interface

The core chat interface displays messages in a conversational format. User messages appear on the right side with a black background, while AI responses appear on the left with a light gray background. This design mimics popular messaging applications for familiarity and ease of use.

Messages are displayed chronologically, with the most recent at the bottom. Each message includes subtle animations when it appears, creating a smooth user experience.

### AI Response Modes

TextIQ offers three response modes to balance speed and capability:

**Fast Mode** (gemini-2.5-flash)
This mode prioritizes quick responses and is suitable for straightforward queries, general conversation, and situations where speed matters more than depth. It handles most common tasks efficiently.

**Powerful Mode** (gemini-2.5-pro)
For complex reasoning, detailed analysis, or tasks requiring deeper understanding, Powerful Mode provides more sophisticated responses. It takes slightly longer but delivers higher quality output for challenging queries.

**Balanced Mode** (gemini-1.5-flash)
This middle-ground option offers a good compromise between response speed and capability. It works well for most general-purpose interactions.

### Creativity Control

The temperature slider adjusts the randomness in AI responses, ranging from 0.0 to 1.5:

- **0.0 to 0.5**: More focused and deterministic responses, ideal for factual questions and precise tasks
- **0.5 to 1.0**: Balanced creativity, suitable for general conversation and most use cases
- **1.0 to 1.5**: Higher creativity and variety, better for brainstorming, creative writing, and exploring diverse perspectives

### AI Personality Customization

The system prompt defines how the AI behaves and responds. You can modify this to create specialized assistants:

- A formal business consultant for professional advice
- A casual, friendly assistant for everyday conversation
- A technical expert focused on specific domains
- A creative writing partner with imaginative responses

Changes to the system prompt take effect with the next message sent.

### Chat History Management

Every conversation is automatically saved when you start a new chat. The history system stores:
- Complete message history
- Timestamp of creation
- Preview of the first message as the chat title
- Unique identifier for each conversation

You can load previous conversations to continue them, review past interactions, or delete conversations you no longer need. All data is stored locally in `chat_history.json`.

### Theme System

The application supports two visual themes:

**Light Mode** features a clean white background with dark text, suitable for well-lit environments and users who prefer traditional interfaces.

**Dark Mode** uses dark backgrounds with light text, reducing eye strain in low-light conditions and providing a modern aesthetic many users prefer.

The theme toggle preserves your preference during your session and applies consistent styling across all interface elements.

### Settings Panel

The settings interface provides quick access to all customization options without interrupting your workflow. It includes:
- AI personality text area for system prompt editing
- Mode selector dropdown for choosing response quality
- Creativity slider for temperature adjustment
- Real-time application of settings

### Navigation Controls

Four primary buttons at the top provide quick access to main features:
- **Settings**: Opens the configuration panel
- **New Chat**: Saves current conversation and starts fresh
- **History**: Displays all saved conversations
- **Theme**: Toggles between dark and light modes

These controls are duplicated in the sidebar for convenient access regardless of where you are in the interface.

---

## Usage Guide

### Starting Your First Conversation

After launching the application, you'll see a welcome screen. Simply type your message in the chat input at the bottom of the page and press Enter. The AI will process your message and respond within a few seconds, depending on the selected mode and message complexity.

### Adjusting Settings Mid-Conversation

You can change settings at any time:
1. Click the Settings button to open the configuration panel
2. Modify the system prompt, select a different mode, or adjust creativity
3. Continue chatting - new settings apply to subsequent messages
4. Previous messages remain unchanged

### Managing Conversations

To save a conversation, click "New Chat" before starting a different topic. This automatically saves your current chat to history. To review past conversations, click "History" to see all saved chats. Click any chat to load it and continue where you left off.

To delete unwanted conversations, open the History panel and click the delete icon next to the chat you want to remove.

### Optimizing API Usage

To make the most of your API quota:
- Use Fast Mode for simple questions and quick interactions
- Reserve Powerful Mode for complex tasks that require deeper reasoning
- Lower the creativity setting for factual queries
- Increase creativity for brainstorming and creative tasks

---

---

## Testing and Verification

TextIQ includes two testing scripts to ensure your setup is correct and identify issues before running the main application.

### test_api.py - Quick API Key Verification

This lightweight script performs a rapid check of your API key configuration and connectivity.

**What it tests:**
1. Verifies `google-generativeai` package is installed
2. Checks if API key exists in `.env` file
3. Validates API key format and length
4. Tests connection to Google Gemini API
5. Lists available models
6. Sends a test message to confirm generation works

**How to use:**
```bash
python test_api.py
```

**Expected output:**
```
===========================================================
GEMINI API KEY TESTER
===========================================================

1. Checking google-generativeai package...
   ✓ Package installed

2. Checking API key...
   ✓ API key found: AIzaSyBxxx...

3. Testing API connection...
   Attempting to list available models...
   ✓ SUCCESS! Found 3 models

   Available models:
   - models/gemini-2.5-flash
   - models/gemini-2.5-pro
   - models/gemini-1.5-flash

4. Testing message generation...
   Using model: gemini-2.5-flash
   Sending test message: 'Say hi'
   ✓ Response received: Hello! How can I help you today?

===========================================================
🎉 ALL TESTS PASSED!
===========================================================

Your API key is working correctly!
You can now run your chatbot:
  streamlit run app.py
```

**Common issues it catches:**
- Missing or incorrectly formatted API key
- Package installation problems
- Network connectivity issues
- Rate limit exceeded errors
- Invalid or expired API keys

**When to use:**
- First time setup
- After updating your API key
- When experiencing connection problems
- Before running the main application

---

### testing.py - Comprehensive Test Suite

This script performs extensive validation of all application components and features.

**What it tests:**

**Core Configuration Tests:**
1. **Environment Variables** - Validates `.env` file and API key configuration
2. **Package Imports** - Checks all required dependencies are installed
3. **API Connection** - Tests real connectivity with Gemini API
4. **Chat History System** - Validates file operations for saving conversations

**Feature Validation Tests:**
5. **Session State Structure** - Verifies app.py session variables
6. **All Models** - Tests Fast Mode, Powerful Mode, and Balanced Mode individually
7. **Temperature Configuration** - Confirms creativity settings (0.0 to 1.5)
8. **File Structure** - Checks all required and optional files exist
9. **Dark Mode Feature** - Validates theme switching capability
10. **System Prompt** - Confirms AI personality configuration

**Usage options:**

**Full test suite:**
```bash
python testing.py
```
Runs all 10 tests and provides detailed results with success rate percentage.

**Quick check:**
```bash
python testing.py quick
```
Fast 5-second verification of critical setup components only. Perfect for confirming basic installation.

**Individual tests:**
```bash
python testing.py api          # Test API connection only
python testing.py models       # Test all three AI modes
python testing.py history      # Test chat history system
python testing.py env          # Test environment variables
python testing.py imports      # Test package installations
```

**Available test commands:**
- `quick` - Fast setup verification
- `env` - Environment variables
- `imports` - Package imports
- `api` - API connection
- `history` - Chat history system
- `session` - Session state structure
- `models` - All AI modes
- `temp` - Temperature configuration
- `files` - File structure
- `darkmode` - Theme feature
- `prompt` - System prompt

**Expected output (full suite):**
```
===========================================================
TEXTIQ AI CHATBOT - COMPREHENSIVE TEST SUITE
===========================================================

Testing environment variables...
✓ PASS: Environment variables configured correctly
   API Key: AIzaSyBxxx...xxxxx

Testing package imports...
✓ streamlit installed
✓ google-generativeai installed
✓ python-dotenv installed
✓ PASS: All required packages installed

Testing Google Gemini API connection...
Configuring Gemini API...
Creating test model (gemini-2.5-flash)...
Sending test request...
✓ PASS: API connection successful
   Sample response: Hello, test successful!

[... continues with all tests ...]

===========================================================
TEST SUMMARY
===========================================================
✓ PASS: Environment Variables
✓ PASS: Package Imports
✓ PASS: API Connection
✓ PASS: Chat History System
✓ PASS: Session State Structure
✓ PASS: All Models (Fast/Powerful/Balanced)
✓ PASS: Temperature Configuration
✓ PASS: File Structure
✓ PASS: Dark Mode Feature
✓ PASS: System Prompt

Results: 10/10 tests passed
Success Rate: 100.0%

🎉 PERFECT! All tests passed!

✨ Your TextIQ chatbot is ready to run!
   Command: streamlit run app.py
===========================================================
```

**What happens if tests fail:**

The script provides specific guidance based on what failed:

- **Missing API key:** Instructions to create `.env` file with proper format
- **Invalid API key:** Link to obtain a new key from Google AI Studio
- **Rate limit exceeded:** Explanation of free tier limits (60/min, 1500/day)
- **Missing packages:** Command to install dependencies
- **Permission errors:** Guidance on file access issues

---

### Recommended Testing Workflow

Follow this sequence for the smoothest setup experience:

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Create .env file with your API key
# Add: GEMINI_API_KEY=your_key_here

# Step 3: Quick API verification (5-10 seconds)
python test_api.py

# Step 4: Fast setup check (5 seconds)
python testing.py quick

# Step 5: Full validation - optional but recommended (15-30 seconds)
python testing.py

# Step 6: Launch application
streamlit run app.py
```

**Troubleshooting specific issues:**

If you encounter a specific problem, use targeted tests:

```bash
# API connection problems
python testing.py api

# Model-specific issues
python testing.py models

# Chat not saving
python testing.py history

# General configuration
python testing.py quick
```

---

### Testing File Comparison

| Feature | test_api.py | testing.py |
|---------|-------------|------------|
| **Purpose** | Quick API verification | Complete setup validation |
| **Duration** | 5-10 seconds | 15-30 seconds (full) / 5 seconds (quick) |
| **Scope** | API connectivity only | All application features |
| **Tests Run** | 4 checks | 10 comprehensive tests |
| **Best For** | First-time setup | Pre-deployment verification |
| **Output Style** | Simple pass/fail | Detailed test breakdown |
| **Use Case** | "Does my API key work?" | "Is everything configured correctly?" |

Both testing tools are designed to catch configuration problems early and provide clear, actionable solutions rather than letting errors surface during runtime.

---

## Troubleshooting

### API Key Issues

If you see "API key not configured":

1. Run the diagnostic tool:
```bash
python test_api.py
```

2. Verify that:
- The `.env` file exists in your project root directory
- The file contains `GEMINI_API_KEY=your_key_here`
- The API key is valid and properly formatted
- There are no extra spaces or quotes around the key

3. Check the API key format:
- Google Gemini keys typically start with `AIza`
- Keys are usually 39 characters long
- Contains only alphanumeric characters and hyphens

### Rate Limiting

The message "Usage limit reached" indicates you've hit API rate limits. The free tier has usage restrictions. Wait a few minutes before sending more messages, or consider upgrading your API plan for higher limits.

### Chat History Not Saving

If conversations aren't being saved:

1. Test the chat history system:
```bash
python testing.py history
```

2. Check that:
- The application has write permissions in its directory
- There's sufficient disk space available
- The `chat_history.json` file isn't locked by another process

3. Try manually creating the file:
```bash
echo "[]" > chat_history.json
```

4. Look for errors in the terminal where you launched the application

### Module Import Errors

If you encounter import errors when starting the application:

1. Run the import test:
```bash
python testing.py imports
```

2. Reinstall dependencies:
```bash
pip install --upgrade streamlit google-generativeai python-dotenv
```

3. If issues persist, try creating a fresh virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

This ensures all dependencies are properly installed and up to date.

---

## Configuration Reference

### Environment Variables

The application uses these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| GEMINI_API_KEY | Your Google Gemini API authentication key | Yes |

### Default Settings

The application includes sensible defaults:

```python
# Default AI behavior
DEFAULT_SYSTEM_PROMPT = """You are TextIQ, an intelligent AI assistant. 
You provide clear, accurate, and helpful responses. You are professional, 
friendly, and always aim to assist users in the best way possible."""

# Available models
MODELS = {
    "Fast Mode": "gemini-2.5-flash",
    "Powerful Mode": "gemini-2.5-pro",
    "Balanced Mode": "gemini-1.5-flash"
}

# Default creativity level
DEFAULT_TEMPERATURE = 0.7
```

---

## Security Considerations

### API Key Protection

Your API key should be kept confidential. The `.env` file storing your key should never be committed to version control. Add it to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### Data Privacy

All chat data is stored locally on your machine in `chat_history.json`. The application does not send data to any servers except the Google Gemini API for generating responses. Your conversations are not shared or uploaded to external services.

### Best Practices

- Rotate your API key periodically
- Don't share your `.env` file or API key with others
- Keep your dependencies updated for security patches
- Review the chat history file contents if you plan to share your device

---

## Customization Options

### Modifying Colors

To change the application's color scheme, edit the `load_custom_css()` function in `app.py`. Look for the color variable definitions around line 100:

```python
# For dark mode
bg_color = "#0f0f0f"
card_bg = "#1a1a1a"
text_color = "#ffffff"

# For light mode
bg_color = "#ffffff"
card_bg = "#ffffff"
text_color = "#000000"
```

Adjust these hex color codes to match your preferred aesthetic.

### Adding New Models

If Google releases new Gemini models, you can add them to the MODELS dictionary:

```python
MODELS = {
    "Fast Mode": "gemini-2.5-flash",
    "Powerful Mode": "gemini-2.5-pro",
    "Balanced Mode": "gemini-1.5-flash",
    "Your New Mode": "new-model-name"
}
```

### Adjusting Message Limits

To change the maximum tokens in AI responses, modify the generation config in the `generate_response()` function:

```python
generation_config={
    "temperature": temperature,
    "max_output_tokens": 2048,  # Increase or decrease as needed
}
```

---

## Technical Details

### Message Storage Format

Chat history is stored as JSON with this structure:

```json
[
  {
    "id": "20240315_143022",
    "timestamp": "2024-03-15 14:30:22",
    "title": "How do I create a Python function for...",
    "messages": [
      {"role": "user", "content": "User message here"},
      {"role": "assistant", "content": "AI response here"}
    ]
  }
]
```

### Session State Management

Streamlit's session state maintains these variables:
- `messages`: Current conversation history
- `system_prompt`: Active AI personality
- `selected_model`: Current response mode
- `temperature`: Creativity level
- `dark_mode`: Theme preference
- `show_settings`: Settings panel visibility
- `show_history`: History panel visibility

### API Communication

The application communicates with Google's Gemini API using the official Python client. Messages are formatted into a conversation history that maintains context throughout the chat session.

---

## Support and Resources

### Getting Help

If you encounter issues:
1. Check the Troubleshooting section above
2. Review error messages in the terminal where you launched the application
3. Verify your API key and internet connection
4. Ensure all dependencies are correctly installed

### Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Python-dotenv Guide](https://pypi.org/project/python-dotenv/)

---

## Future Development

Planned features for upcoming versions include:
- File upload support for documents and images
- Export functionality for chat history
- Streaming responses for real-time output
- Code syntax highlighting in messages
- Search functionality within conversations
- Multi-language interface support
- Voice input and output capabilities

---

## License

This project is available under the MIT License. You're free to use, modify, and distribute it as needed.

---

**TextIQ** - Built with Streamlit and Google Gemini AI

Live Demo
Try it now: https://textiq-chat.streamlit.app/
