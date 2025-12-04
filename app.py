"""
TextIQ - AI-Powered Chat Assistant
Clean Design with Dark/Light Mode & Chat History
"""

import streamlit as st
import time
import os
import json
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# Import Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================
# Support both Streamlit Cloud secrets and local .env
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# AI Models (internal use only)
MODELS = {
    "Fast Mode": "gemini-2.5-flash",
    "Powerful Mode": "gemini-2.5-pro",
    "Balanced Mode": "gemini-1.5-flash"
}

DEFAULT_SYSTEM_PROMPT = """You are TextIQ, an intelligent AI assistant. You provide clear, 
accurate, and helpful responses. You are professional, friendly, and always aim to assist users 
in the best way possible."""

# Chat history file
CHAT_HISTORY_FILE = "chat_history.json"

# ============================================================================
# CHAT HISTORY FUNCTIONS
# ============================================================================

def save_chat_history():
    """Save current chat to history"""
    if not st.session_state.messages:
        return
    
    # Load existing history
    history = load_all_chats()
    
    # Create new chat entry
    chat_entry = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": st.session_state.messages[0]["content"][:50] + "..." if st.session_state.messages else "New Chat",
        "messages": st.session_state.messages.copy()
    }
    
    # Add to history
    history.append(chat_entry)
    
    # Save to file
    try:
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save chat: {str(e)}")

def load_all_chats():
    """Load all chat history"""
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def load_chat(chat_id):
    """Load a specific chat"""
    history = load_all_chats()
    for chat in history:
        if chat["id"] == chat_id:
            st.session_state.messages = chat["messages"]
            st.rerun()

def delete_chat(chat_id):
    """Delete a specific chat"""
    history = load_all_chats()
    history = [chat for chat in history if chat["id"] != chat_id]
    try:
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        st.rerun()
    except Exception as e:
        st.error(f"Failed to delete chat: {str(e)}")

# ============================================================================
# MODERN CSS WITH DARK/LIGHT MODE
# ============================================================================

def load_custom_css(dark_mode: bool = False):
    """Load modern CSS with dark/light mode support"""
    
    if dark_mode:
        # DARK MODE COLORS
        bg_color = "#0f0f0f"
        card_bg = "#1a1a1a"
        text_color = "#ffffff"
        text_secondary = "#b0b0b0"
        border_color = "#333333"
        user_msg_bg = "#000000"
        user_msg_text = "#ffffff"
        ai_msg_bg = "#2a2a2a"  # Light gray for AI messages
        ai_msg_border = "#3a3a3a"
        sidebar_bg = "#1a1a1a"
        button_bg = "#ffffff"
        button_text = "#000000"
        button_hover_bg = "#e0e0e0"
        input_bg = "#1a1a1a"
        input_border = "#333333"
    else:
        # LIGHT MODE COLORS
        bg_color = "#ffffff"
        card_bg = "#ffffff"
        text_color = "#000000"
        text_secondary = "#6b7280"
        border_color = "#e5e7eb"
        user_msg_bg = "#000000"  # Black for user
        user_msg_text = "#ffffff"
        ai_msg_bg = "#e5e7eb"  # Light gray for AI
        ai_msg_border = "#d1d5db"
        sidebar_bg = "#f9fafb"
        button_bg = "#000000"
        button_text = "#ffffff"
        button_hover_bg = "#1f2937"
        input_bg = "#ffffff"
        input_border = "#e5e7eb"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Main background */
        .stApp {{
            background: {bg_color};
            transition: background 0.3s ease;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Main title */
        h1 {{
            font-size: 3rem !important;
            font-weight: 800 !important;
            color: {text_color};
            text-align: center;
            margin-bottom: 0.5rem !important;
            letter-spacing: -0.02em;
        }}
        
        /* Chat message container */
        .stChatMessage {{
            border-radius: 18px !important;
            padding: 1rem 1.2rem !important;
            margin: 0.5rem 0 !important;
            max-width: 70% !important;
            animation: slideUp 0.3s ease-out;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            width: fit-content !important;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Force user messages to RIGHT */
        div[data-testid="stChatMessageContainer"]:has([data-testid*="user"]) {{
            display: flex !important;
            justify-content: flex-end !important;
        }}
        
        /* Force AI messages to LEFT */
        div[data-testid="stChatMessageContainer"]:has([data-testid*="assistant"]) {{
            display: flex !important;
            justify-content: flex-start !important;
        }}
        
        /* User messages - RIGHT side, BLACK like iMessage */
        .stChatMessage[data-testid*="user"] {{
            background: #000000 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 18px 18px 4px 18px !important;
            float: right !important;
            clear: both !important;
        }}
        
        .stChatMessage[data-testid*="user"] p {{
            color: #ffffff !important;
            margin: 0 !important;
        }}
        
        .stChatMessage[data-testid*="user"] .stMarkdown {{
            color: #ffffff !important;
        }}
        
        .stChatMessage[data-testid*="user"] div {{
            color: #ffffff !important;
        }}
        
        /* AI messages - LEFT side, LIGHT GRAY like WhatsApp */
        .stChatMessage[data-testid*="assistant"] {{
            background: {ai_msg_bg} !important;
            border: 1px solid {ai_msg_border} !important;
            color: {text_color} !important;
            border-radius: 18px 18px 18px 4px !important;
            float: left !important;
            clear: both !important;
        }}
        
        .stChatMessage[data-testid*="assistant"] p {{
            color: {text_color} !important;
            margin: 0 !important;
        }}
        
        .stChatMessage[data-testid*="assistant"] div {{
            color: {text_color} !important;
        }}
        
        /* Chat message content wrapper */
        .stChatMessage > div {{
            max-width: 100% !important;
        }}
        
        /* Clear floats after each message */
        .stChatMessage::after {{
            content: "";
            display: table;
            clear: both;
        }}
        
        /* Main chat container */
        section[data-testid="stVerticalBlock"] > div {{
            display: block !important;
        }}
        
        /* Override Streamlit's flex container */
        .element-container {{
            width: 100% !important;
        }}
        
        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            border-right: 1px solid {border_color};
        }}
        
        section[data-testid="stSidebar"] > div {{
            padding-top: 1rem;
        }}
        
        /* Make sidebar toggle button more visible */
        button[kind="header"] {{
            background: {button_bg} !important;
            color: {button_text} !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }}
        
        /* Sidebar collapse button styling */
        section[data-testid="stSidebar"] button[kind="header"] {{
            display: block !important;
            visibility: visible !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: {button_bg};
            color: {button_text};
            border: 2px solid {button_bg};
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            background: {button_hover_bg};
            border-color: {button_hover_bg};
            transform: translateY(-1px);
        }}
        
        /* Small buttons */
        .small-button {{
            background: {button_bg};
            color: {button_text};
            border: 1px solid {button_bg};
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-block;
        }}
        
        .small-button:hover {{
            transform: translateY(-1px);
        }}
        
        /* Chat input */
        .stChatInputContainer {{
            background: {input_bg} !important;
            border: 2px solid {input_border} !important;
            border-radius: 16px !important;
            padding: 0.5rem !important;
        }}
        
        /* Text area */
        .stTextArea textarea {{
            background: {input_bg} !important;
            border: 2px solid {input_border} !important;
            border-radius: 12px;
            padding: 0.75rem;
            font-size: 0.95rem;
            color: {text_color};
        }}
        
        /* Select box */
        .stSelectbox > div > div {{
            background: {input_bg} !important;
            border: 2px solid {input_border} !important;
            border-radius: 12px;
            color: {text_color};
        }}
        
        /* Slider */
        .stSlider > div > div > div {{
            background: {button_bg};
        }}
        
        /* Labels */
        label {{
            color: {text_color} !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }}
        
        /* Captions */
        .stCaption {{
            color: {text_secondary} !important;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: {card_bg} !important;
            border: 2px solid {border_color} !important;
            border-radius: 12px;
            color: {text_color} !important;
            font-weight: 600 !important;
        }}
        
        /* Chat history item */
        .chat-history-item {{
            background: {card_bg};
            border: 2px solid {border_color};
            border-radius: 12px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .chat-history-item:hover {{
            border-color: {button_bg};
            transform: translateX(4px);
        }}
        
        .chat-history-title {{
            color: {text_color};
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }}
        
        .chat-history-time {{
            color: {text_secondary};
            font-size: 0.75rem;
        }}
        
        /* Divider */
        hr {{
            border: none;
            height: 1px;
            background: {border_color};
            margin: 1rem 0;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {sidebar_bg};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {border_color};
            border-radius: 5px;
        }}
        
        /* Input text */
        input {{
            color: {text_color} !important;
        }}
        
        /* Markdown */
        .stMarkdown {{
            color: {text_color};
        }}
        </style>
    """, unsafe_allow_html=True)

# ============================================================================
# RESPONSE GENERATOR
# ============================================================================

def generate_response(messages: List[Dict], system_prompt: str, model_name: str, temperature: float) -> str:
    """Generate AI response"""
    
    if not GEMINI_AVAILABLE:
        return "❌ Please install: pip install google-generativeai"
    
    if not GEMINI_API_KEY:
        return "❌ API key not configured"
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 2048,
            },
            system_instruction=system_prompt
        )
        
        history = []
        for msg in messages[:-1]:
            history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })
        
        chat = model.start_chat(history=history)
        response = chat.send_message(messages[-1]["content"])
        
        return response.text
        
    except Exception as e:
        error_msg = str(e).lower()
        
        if "quota" in error_msg or "429" in error_msg or "limit" in error_msg:
            return "⏳ Usage limit reached. Please wait a moment or get a new API key."
        else:
            return f"❌ Error: {str(e)[:100]}"

# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(
    page_title="TextIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"  # Keep sidebar open by default
)

# ============================================================================
# SESSION STATE
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Fast Mode"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# Apply theme
load_custom_css(st.session_state.dark_mode)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    # Header buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚙️", help="Settings", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
            st.session_state.show_history = False
            st.rerun()
    
    with col2:
        if st.button("📝", help="New Chat", use_container_width=True):
            if st.session_state.messages:
                save_chat_history()
            st.session_state.messages = []
            st.rerun()
    
    with col3:
        if st.button("📚", help="Chat History", use_container_width=True):
            st.session_state.show_history = not st.session_state.show_history
            st.session_state.show_settings = False
            st.rerun()
    
    st.markdown("---")
    
    # Settings Panel
    if st.session_state.show_settings:
        st.markdown("### ⚙️ Settings")
        
        # Dark mode toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**🌙 Dark Mode**")
        with col2:
            if st.button("🔄", key="dark_mode_toggle"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        st.markdown("---")
        
        # AI Personality
        st.markdown("**💭 AI Personality**")
        st.session_state.system_prompt = st.text_area(
            "Customize",
            value=st.session_state.system_prompt,
            height=100,
            label_visibility="collapsed"
        )
        
        # Mode Selection
        st.markdown("**🚀 Mode**")
        st.session_state.selected_model = st.selectbox(
            "Mode",
            options=list(MODELS.keys()),
            label_visibility="collapsed"
        )
        
        # Creativity Level
        st.markdown("**🎨 Creativity**")
        st.session_state.temperature = st.slider(
            "Creativity",
            0.0, 1.5,
            st.session_state.temperature,
            0.1,
            label_visibility="collapsed"
        )
    
    # Chat History Panel
    elif st.session_state.show_history:
        st.markdown("### 📚 Chat History")
        
        chat_history = load_all_chats()
        
        if chat_history:
            # Reverse to show newest first
            for chat in reversed(chat_history):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if st.button(
                        f"💬 {chat['title'][:30]}...",
                        key=f"load_{chat['id']}",
                        help=chat['timestamp'],
                        use_container_width=True
                    ):
                        load_chat(chat['id'])
                
                with col2:
                    if st.button("🗑️", key=f"del_{chat['id']}", help="Delete"):
                        delete_chat(chat['id'])
        else:
            st.info("No chat history yet")
    
    # Default view - Quick actions
    else:
        st.markdown("### 🚀 Quick Actions")
        st.info("Use the buttons above to:\n\n⚙️ Open Settings\n\n📝 Start New Chat\n\n📚 View History")
    
    st.markdown("---")
    
    # Clear current chat
    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================================================
# MAIN CHAT AREA
# ============================================================================

# Header with quick actions
header_col1, header_col2, header_col3, header_col4 = st.columns([1, 1, 1, 1])

with header_col1:
    if st.button("⚙️ Settings", use_container_width=True, key="main_settings"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.session_state.show_history = False

with header_col2:
    if st.button("📝 New Chat", use_container_width=True, key="main_new_chat"):
        if st.session_state.messages:
            save_chat_history()
        st.session_state.messages = []
        st.rerun()

with header_col3:
    if st.button("📚 History", use_container_width=True, key="main_history"):
        st.session_state.show_history = not st.session_state.show_history
        st.session_state.show_settings = False

with header_col4:
    if st.button("🌓 Theme", use_container_width=True, key="main_dark_mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Show settings panel in main area if toggled
if st.session_state.show_settings:
    with st.expander("⚙️ Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💭 AI Personality**")
            st.session_state.system_prompt = st.text_area(
                "Customize AI behavior",
                value=st.session_state.system_prompt,
                height=100,
                key="main_system_prompt"
            )
            
            st.markdown("**🚀 Response Mode**")
            st.session_state.selected_model = st.selectbox(
                "Select mode",
                options=list(MODELS.keys()),
                key="main_model_select"
            )
        
        with col2:
            st.markdown("**🎨 Creativity Level**")
            st.session_state.temperature = st.slider(
                "Adjust creativity",
                0.0, 1.5,
                st.session_state.temperature,
                0.1,
                key="main_temp_slider"
            )
            
            if st.session_state.temperature < 0.5:
                st.caption("🎯 Focused & Precise")
            elif st.session_state.temperature < 1.0:
                st.caption("⚖️ Balanced")
            else:
                st.caption("🎨 Creative & Diverse")

# Show history panel in main area if toggled
if st.session_state.show_history:
    with st.expander("📚 Chat History", expanded=True):
        chat_history = load_all_chats()
        
        if chat_history:
            st.markdown("**Recent Conversations:**")
            
            # Show in columns for better layout
            for i, chat in enumerate(reversed(chat_history)):
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    if st.button(
                        f"💬 {chat['title'][:40]}..." if len(chat['title']) > 40 else f"💬 {chat['title']}",
                        key=f"main_load_{chat['id']}",
                        help=f"Created: {chat['timestamp']}",
                        use_container_width=True
                    ):
                        load_chat(chat['id'])
                
                with col2:
                    if st.button("🗑️", key=f"main_del_{chat['id']}", help="Delete"):
                        delete_chat(chat['id'])
                
                if i < len(chat_history) - 1:
                    st.markdown("---")
        else:
            st.info("No chat history yet. Start a conversation and click 'New Chat' to save it!")

st.markdown("---")

# Check setup
if not GEMINI_AVAILABLE or not GEMINI_API_KEY or len(GEMINI_API_KEY) < 20:
    st.error("⚠️ Please configure your API key in .env file")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("💬 Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            model_name = MODELS[st.session_state.selected_model]
            response = generate_response(
                st.session_state.messages,
                st.session_state.system_prompt,
                model_name,
                st.session_state.temperature
            )
            st.write(response)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Welcome screen
if len(st.session_state.messages) == 0:
    # Determine colors based on dark mode
    if st.session_state.dark_mode:
        card_bg = "#1a1a1a"
        card_border = "#333333"
        title_color = "#ffffff"
        text_color = "#b0b0b0"
    else:
        card_bg = "#f9fafb"
        card_border = "#e5e7eb"
        title_color = "#000000"
        text_color = "#6b7280"
    
    # Title and subtitle
    st.markdown(f"<h1 style='color: {title_color};'>Welcome to TextIQ 👋</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.1rem; color: {text_color}; margin-bottom: 0.5rem;'>Your intelligent AI assistant ready to help with anything you need.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 0.95rem; color: {text_color}; margin-bottom: 1rem;'>💡 <strong>Tip:</strong> Use the buttons at the top - <strong>⚙️ Settings</strong>, <strong>📝 New Chat</strong>, <strong>📚 History</strong>, and <strong>🌓 Theme</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1rem; color: {text_color}; margin-bottom: 3rem;'>Start a conversation by typing a message below.</p>", unsafe_allow_html=True)
    
    # Feature cards using columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem 1rem; background: {card_bg}; border: 2px solid {card_border}; border-radius: 16px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>⚡</div>
            <div style='font-weight: 700; color: {title_color}; margin-bottom: 0.5rem; font-size: 1.1rem;'>Lightning Fast</div>
            <div style='font-size: 0.95rem; color: {text_color};'>Get instant responses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem 1rem; background: {card_bg}; border: 2px solid {card_border}; border-radius: 16px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🎯</div>
            <div style='font-weight: 700; color: {title_color}; margin-bottom: 0.5rem; font-size: 1.1rem;'>Accurate</div>
            <div style='font-size: 0.95rem; color: {text_color};'>Precise information</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem 1rem; background: {card_bg}; border: 2px solid {card_border}; border-radius: 16px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🎨</div>
            <div style='font-weight: 700; color: {title_color}; margin-bottom: 0.5rem; font-size: 1.1rem;'>Creative</div>
            <div style='font-size: 0.95rem; color: {text_color};'>Innovative solutions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem 1rem; background: {card_bg}; border: 2px solid {card_border}; border-radius: 16px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🔒</div>
            <div style='font-weight: 700; color: {title_color}; margin-bottom: 0.5rem; font-size: 1.1rem;'>Secure</div>
            <div style='font-size: 0.95rem; color: {text_color};'>Your data is safe</div>
        </div>
        """, unsafe_allow_html=True)
