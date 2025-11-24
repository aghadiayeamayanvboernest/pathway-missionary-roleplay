import os
import base64
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="PathwayConnect Missionary Training",
    page_icon="images/pathway.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
try:
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
except:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Define available personas
PERSONAS = {
    "jorge": {
        "name": "Jorge Vargas",
        "description": "Jorge Vargas",
        "prompt_file": "roleplay-content/prompts/jorge-system-prompt.md",
        "hint": ""
    },
    "katra": {
        "name": "Katra",
        "description": "Katra",
        "prompt_file": "roleplay-content/prompts/katra-system-prompt.md",
        "hint": ""
    },
    "vitoria": {
        "name": "Vitoria da Silva",
        "description": "Vitoria da Silva",
        "prompt_file": "roleplay-content/prompts/vitoria-system-prompt.md",
        "hint": ""
    },
    "Aisha": {
        "name": "Aisha Okafor",
        "description": "Aisha Okafor",
        "prompt_file": "roleplay-content/prompts/aisha-system-prompt.md",
        "hint": ""
    },
        "Chipo": {
        "name": "Chipo Mwale",
        "description": "Chipo Mwale",
        "prompt_file": "roleplay-content/prompts/chipo-system-prompt.md",
        "hint": ""
    },
        "David": {
        "name": "David Tui",
        "description": "David Tui",
        "prompt_file": "roleplay-content/prompts/david-system-prompt.md",
        "hint": ""
    },
        "Maria": {
        "name": "Maria Santos",
        "description": "Maria Santos",
        "prompt_file": "roleplay-content/prompts/maria-system-prompt.md",
        "hint": ""
    },
        "Samuel": {
        "name": "Samuel Mensah",
        "description": " Samuel Mensah",
        "prompt_file": "roleplay-content/prompts/samuel-system-prompt.md",
        "hint": ""
    }
    
}

def load_system_prompt(persona_key):
    try:
        prompt_path = PERSONAS[persona_key]["prompt_file"]
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading persona prompt: {str(e)}")
        return ""

def load_grading_prompt():
    try:
        with open("roleplay-content/prompts/grading-system-prompt.md", 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading grading prompt: {str(e)}")
        return ""

def format_conversation_transcript(messages, persona_key):
    """
    Format the conversation transcript for evaluation.
    
    Format:
    Student: [Student Name]
    
    ## Full Conversation Transcript
    
    **Missionary:** [what the missionary said]
    
    **[Student Name]:** [what the student said]
    
    **Missionary:** [what the missionary said next]
    
    **[Student Name]:** [what the student said next]
    """
    persona_name = PERSONAS[persona_key]["name"]
    
    # Start with student identification and header
    transcript = f"**Student:** {persona_name}\n\n## Full Conversation Transcript\n\n"
    
    # Add each message in order with bold names
    for message in messages:
        if message["role"] == "user":
            transcript += f"**Missionary:** {message['content']}\n\n"
        elif message["role"] == "assistant":
            transcript += f"**{persona_name}:** {message['content']}\n\n"
    
    return transcript

# CSS
st.markdown("""
    <style>
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    .sidebar-logo img {
        width: 140px;
        height: auto;
        margin-bottom: 0.5rem;
        filter: brightness(0) saturate(100%) invert(73%) sepia(89%) saturate(1742%) hue-rotate(360deg) brightness(98%) contrast(101%);
    }
    .sidebar-title {
        font-size: 1.1em;
        font-weight: 600;
        color: #1a1a1a;
        margin: 0.5rem 0 0.3rem 0;
        line-height: 1.3;
    }
    .sidebar-subtitle {
        font-size: 0.85em;
        color: #666;
        margin: 0;
        font-weight: 400;
        line-height: 1.4;
    }
    div[data-testid="column"] button {
        transition: all 0.2s ease;
        opacity: 0.6;
    }
    div[data-testid="column"] button:hover {
        opacity: 1;
        transform: scale(1.1);
    }
    
    /* Fixed view selector at top */
    .view-selector {
        position: sticky;
        top: 0;
        background: white;
        z-index: 999;
        padding: 1rem 0;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .view-selector {
            background: rgb(14, 17, 23) !important;
            border-bottom-color: #333 !important;
        }
    }
    
    /* Force dark mode for Streamlit's dark theme */
    .stApp[data-theme="dark"] .view-selector,
    [data-testid="stAppViewContainer"][data-theme="dark"] .view-selector {
        background: rgb(14, 17, 23) !important;
        border-bottom-color: #333 !important;
    }
    
    /* Reduce sidebar spacing */
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0.5rem;
    }
    section[data-testid="stSidebar"] h3 {
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "evaluation_result" not in st.session_state:
    st.session_state.evaluation_result = None
if "evaluation_metadata" not in st.session_state:
    st.session_state.evaluation_metadata = None
if "evaluating" not in st.session_state:
    st.session_state.evaluating = False
if "show_confirm_dialog" not in st.session_state:
    st.session_state.show_confirm_dialog = False
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = "jorge"
if "current_view" not in st.session_state:
    st.session_state.current_view = "Chat"
if "show_eval_complete" not in st.session_state:
    st.session_state.show_eval_complete = False

# Sidebar
with st.sidebar:
    with open("images/byu-pw-stackedgray.svg", "r") as f:
        svg_content = f.read()
        svg_b64 = base64.b64encode(svg_content.encode()).decode()

    st.markdown(f"""
        <div class="sidebar-logo">
            <img src="data:image/svg+xml;base64,{svg_b64}" alt="BYU-Pathway Worldwide">
            <div class="sidebar-title">Missionary Training</div>
            <div class="sidebar-subtitle">Student Orientation Practice</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔗 Resources")
    st.markdown("[Missionary Assistant App](https://missionary-chat.onrender.com)")
    
    st.markdown("### Select Student")

    persona_options = [PERSONAS[key]["description"] for key in PERSONAS.keys()]
    persona_keys = list(PERSONAS.keys())
    current_index = persona_keys.index(st.session_state.selected_persona)

    selected_display = st.selectbox(
        "Choose which student you'll meet with:",
        persona_options,
        index=current_index,
        key="persona_selector"
    )

    new_persona_key = persona_keys[persona_options.index(selected_display)]
    selected_persona_info = PERSONAS[new_persona_key]

    if new_persona_key != st.session_state.selected_persona:
        st.session_state.selected_persona = new_persona_key
        st.session_state.messages = []
        st.session_state.evaluation_result = None
        st.session_state.evaluation_metadata = None
        st.rerun()

    st.markdown("### Actions")
    if st.button("🔄 Start New Conversation", type="primary", use_container_width=True):
        st.session_state.show_confirm_dialog = True
    
    # Evaluate button
    button_disabled = len(st.session_state.messages) == 0 or st.session_state.evaluating
    if st.button("📊 Evaluate", type="primary", use_container_width=True, key="evaluate_btn", disabled=button_disabled):
        if st.session_state.evaluating:
            st.warning("⚠️ An evaluation is already in progress.")
        else:
            st.session_state.evaluating = True
            with st.spinner("Evaluating..."):
                try:
                    # Load the grading system prompt
                    grading_prompt = load_grading_prompt()
                    
                    # Format the conversation transcript
                    transcript = format_conversation_transcript(
                        st.session_state.messages,
                        st.session_state.selected_persona
                    )
                    
                    # Create the evaluation request with system prompt and transcript as user message
                    eval_messages = [
                        {"role": "system", "content": grading_prompt},
                        {"role": "user", "content": transcript}
                    ]
                    
                    # Call the API
                    response = client.responses.create(
                        model="gpt-5.1",
                        input=eval_messages,
                        reasoning={"effort": "medium"}
                    )
                    
                    # Store results
                    st.session_state.evaluation_result = response.output_text
                    st.session_state.evaluation_metadata = {
                        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                        "message_count": len(st.session_state.messages),
                        "student_name": PERSONAS[st.session_state.selected_persona]["name"]
                    }
                    st.session_state.evaluating = False
                    st.session_state.current_view = "Evaluation"  # Auto-switch to Evaluation view
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.evaluating = False
            st.rerun()

    st.caption("💡 **Tip:** Take your time to build rapport and listen carefully to the student's concerns.")
    st.caption(f"**Current Student:** {PERSONAS[st.session_state.selected_persona]['name']}")

# Confirmation dialog
if st.session_state.show_confirm_dialog:
    st.warning("⚠️ Are you sure you want to start a new conversation? This will clear your current chat and evaluation.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Start New", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.evaluation_result = None
            st.session_state.evaluation_metadata = None
            st.session_state.evaluating = False
            st.session_state.show_confirm_dialog = False
            st.session_state.current_view = "Chat"
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_confirm_dialog = False
            st.rerun()
    st.stop()

# View Selector (instead of tabs)
st.markdown('<div class="view-selector">', unsafe_allow_html=True)

# Determine the index based on current_view BEFORE rendering radio
radio_index = 0 if st.session_state.current_view == "Chat" else 1

view = st.radio(
    "Select View:",
    ["💬 Chat", "📊 Evaluation"],
    index=radio_index,
    horizontal=True,
    key=f"view_radio_{st.session_state.current_view}"  # Dynamic key forces re-render
)

# Only update current_view if user manually clicked the radio (not from button)
selected_view = "Chat" if view == "💬 Chat" else "Evaluation"
if selected_view != st.session_state.current_view:
    st.session_state.current_view = selected_view
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# CHAT VIEW
if st.session_state.current_view == "Chat":
    if st.session_state.evaluating:
        st.info("🔄 Evaluation in progress...")
    
    if len(st.session_state.messages) == 0:
        st.markdown("### 👋 Welcome to Your Training Session")
        st.info(f"""
**About This Exercise:**

You're about to practice a **New Student Orientation Visit** with an AI-simulated student. This is a safe space to build your confidence and improve your communication skills.

**Your Goal:**
Help the student feel prepared, supported, and confident about starting their PathwayConnect journey.

**What to Do:**
1. **Introduce yourself** as a BYU-Pathway missionary
2. **Listen carefully** to the student's concerns and questions
3. **Answer their questions** with accurate information
4. **Provide encouragement** and connect them with resources
5. **Help them feel ready** to begin their program

**Getting Feedback:**
Click the **"📊 Evaluate"** button in the sidebar when ready for feedback.

**Ready?** Type your opening message below to begin the orientation visit.
        """)
    else:
        for idx, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                cols = st.columns([0.9, 0.05, 0.05])
                with cols[1]:
                    if st.button("⎘", key=f"copy_{idx}", help="Copy message", use_container_width=True):
                        st.toast("Copied!", icon="✅")
                if message["role"] == "assistant":
                    with cols[2]:
                        if st.button("↻", key=f"regen_{idx}", help="Regenerate response", use_container_width=True):
                            st.session_state.messages = st.session_state.messages[:idx]
                            st.rerun()

    # Generate response
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    system_prompt = load_system_prompt(st.session_state.selected_persona)
                    api_messages = [{"role": "system", "content": system_prompt}]
                    api_messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages])
                    response = client.responses.create(
                        model="gpt-5.1",
                        input=api_messages,
                        reasoning={"effort": "none"}
                    )
                    assistant_message = response.output_text
                    st.markdown(assistant_message)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                    st.rerun()
                except Exception as e:
                    error_message = f"Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
                    st.rerun()

    # Chat input - only shown in Chat view
    if prompt := st.chat_input("What would you like to say?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# EVALUATION VIEW
elif st.session_state.current_view == "Evaluation":
    if st.session_state.evaluation_result:
        st.markdown("## 📊 Your Evaluation Results")
        meta = st.session_state.evaluation_metadata
        st.caption(f"**Student:** {meta['student_name']} | **Messages:** {meta['message_count']} | **Evaluated:** {meta['timestamp']}")
        
        # Option to view the original transcript - at the top
        with st.expander("📄 View Conversation Transcript Sent for Evaluation"):
            transcript = format_conversation_transcript(
                st.session_state.messages,
                st.session_state.selected_persona
            )
            st.markdown(transcript)
        
        st.divider()
        st.markdown(st.session_state.evaluation_result)
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 Continue Conversation", type="primary", use_container_width=True):
                st.session_state.current_view = "Chat"
                st.rerun()
        with col2:
            if st.button("🔄 Start New Conversation", use_container_width=True):
                st.session_state.show_confirm_dialog = True
                st.rerun()
    else:
        st.info("📋 No evaluation yet - start chatting and click **Evaluate** in the sidebar when ready.")
        st.markdown("""
        ### How Evaluations Work
        
        When you request an evaluation, The model will:
        - Review your complete conversation history
        - Assess your communication approach and effectiveness
        - Provide constructive feedback on your strengths and areas for improvement
        - Offer specific suggestions to enhance your skills
        
        You can request evaluations multiple times during a conversation.
        
        **Tip:** Try to have at least a few exchanges with the student before requesting your first evaluation.
        """)