# 🚀 Quick Start Guide

Get your Llama 3 AI Chatbot running in 5 minutes!

## Option 1: Automated Setup (Recommended)

### For Mac/Linux:
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Edit .env file with your API key
nano .env

# Run the app
streamlit run app.py
```

### For Windows:
```batch
# Run setup
setup.bat

# Edit .env file with your API key (open in Notepad)
notepad .env

# Run the app
streamlit run app.py
```

---

## Option 2: Manual Setup

### Step 1: Create Virtual Environment
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your HuggingFace API key
# Get key from: https://huggingface.co/settings/tokens
```

### Step 4: Run Application
```bash
streamlit run app.py
```

### Step 5: Open Browser
Navigate to: `http://localhost:8501`

---

## Getting Your HuggingFace API Key

1. Go to [HuggingFace](https://huggingface.co/)
2. Sign up for a free account
3. Navigate to [Settings → Access Tokens](https://huggingface.co/settings/tokens)
4. Click "New token"
5. Name it (e.g., "llama3-chatbot")
6. Select "Read" permission
7. Click "Generate"
8. Copy the token (starts with `hf_`)
9. Paste it in your `.env` file:
   ```
   HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## Troubleshooting

### "Model is loading" error
**Solution**: Wait 20-30 seconds and try again. Free tier models need to wake up.

### "Rate limit exceeded"
**Solution**: Wait a few minutes. Free API has usage limits.

### "No module named 'streamlit'"
**Solution**: Activate virtual environment first:
```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Port 8501 already in use
**Solution**: Run on different port:
```bash
streamlit run app.py --server.port 8502
```

---

## First Time Using Streamlit?

After running `streamlit run app.py`, you'll see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

Open the Local URL in your browser to access the chatbot!

---

## Testing the Chatbot

Try these example prompts:

1. **Simple conversation**: "Hello! What can you help me with?"
2. **Technical question**: "Explain machine learning in simple terms"
3. **Creative task**: "Write a short poem about coding"
4. **Summarization**: Upload a text file using the sidebar

---

## Next Steps

- ⚙️ Customize the system prompt in the sidebar
- 🔧 Try different temperature settings (0.1 = focused, 2.0 = creative)
- 🤖 Switch between fast (8B) and accurate (70B) models
- 📄 Upload text files for summarization
- 💾 Export your chat history (coming soon!)

---

**Need Help?** Check the full [README.md](README.md) for detailed documentation.