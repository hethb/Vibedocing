import streamlit as st
from groq import Groq

# --- PAGE CONFIG ---
st.set_page_config(page_title="LexIQ", page_icon="🧠", layout="centered")

# --- BACKGROUND + STYLING + MOUSE EFFECT ---
st.markdown("""
<style>
/* Background gradient animation */
.stApp {
    background: linear-gradient(120deg, #141e30, #243b55, #1f4068, #2a5298);
    background-size: 300% 300%;
    animation: gradientMove 12s ease infinite;
    color: white;
}

/* Gradient animation keyframes */
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Mouse-following highlight */
#highlight-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle 250px at 50% 50%, rgba(56,189,248,0.3), rgba(29,78,216,0.05));
    pointer-events: none;
    z-index: -1;
    transition: background 0.05s ease;
}

/* Glass effect for containers */
.glass-box {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    margin-bottom: 2rem;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00b4d8, #0077ff);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1.3rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 0 12px rgba(0, 180, 216, 0.4);
}
.stButton>button:hover {
    background: linear-gradient(90deg, #00eaff, #0096ff);
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(0, 180, 216, 0.8);
}

/* Textarea styling (light background, dark text) */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    color: #111 !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    border-radius: 10px !important;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 14px !important;
    padding: 10px !important;
}

/* Explanation box */
.explanation-box {
    background: rgba(0, 0, 0, 0.25);
    border-left: 4px solid #00b4d8;
    border-radius: 10px;
    padding: 1.2rem;
    margin-top: 1.5rem;
    color: #f1f1f1;
    line-height: 1.6;
    box-shadow: 0 0 10px rgba(0, 180, 216, 0.4);
}
</style>

<!-- Mouse-following highlight -->
<div id="highlight-bg"></div>

<script>
document.addEventListener('mousemove', e => {
    const bg = document.getElementById('highlight-bg');
    bg.style.background = `radial-gradient(circle 250px at ${e.clientX}px ${e.clientY}px, rgba(56,189,248,0.3), rgba(29,78,216,0.05))`;
});
</script>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='glass-box'><h1>🧠 LexIQ</h1><p>Paste your code below to get smart, beginner-friendly explanations!</p></div>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")
st.sidebar.markdown("[Get your free Groq API key →](https://console.groq.com/keys)")

# --- CODE INPUT ---
code_input = st.text_area("💡 Your Python code here:", height=250, placeholder="Paste your Python code...")

# --- EXPLAIN BUTTON ---
if st.button("🔍 Explain Code"):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    elif not code_input.strip():
        st.error("Please enter some Python code to explain.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("🧩 Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are LexIQ, an AI tutor. "
                                "Explain code line by line, then summarize it simply in a short paragraph for beginners."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Explain this Python code:\n\n{code_input}"
                        }
                    ],
                    temperature=0.3,
                )
                explanation = response.choices[0].message.content
                st.markdown("### 🧾 Explanation")
                st.markdown(f"<div class='explanation-box'>{explanation}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error: {e}")
