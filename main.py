import streamlit as st
from groq import Groq
import json
import hashlib
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="LexIQ - AI-Powered Coding", page_icon="🧠", layout="wide")

# --- USER AUTHENTICATION FUNCTIONS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def load_user_progress(username):
    try:
        with open(f'progress_{username}.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'completed_lessons': [],
            'quiz_scores': {},
            'code_submissions': [],
            'current_streak': 0,
            'total_points': 0,
            'last_login': datetime.now().isoformat()
        }

def save_user_progress(username, progress):
    progress['last_login'] = datetime.now().isoformat()
    with open(f'progress_{username}.json', 'w') as f:
        json.dump(progress, f, indent=2)

# --- SESSION STATE INIT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_progress = None

if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None

# --- CURRICULUM ---
CURRICULUM = {
    "Python Basics": {
        "lessons": [
            {
                "id": "variables",
                "title": "Variables & Data Types",
                "description": "Learn how to store and work with different types of data",
                "content": """
# Variables & Data Types

Variables are containers that store data. Python has several built-in data types:

**Common Data Types:**
- `int` - Whole numbers (e.g., 42, -10)
- `float` - Decimal numbers (e.g., 3.14, -0.5)
- `str` - Text (e.g., "hello", 'world')
- `bool` - True or False values

**Example:**
```python
name = "Alice"          # string
age = 25                # integer
height = 5.6            # float
is_student = True       # boolean
```

**Key Concepts:**
- Variables don't need type declaration
- Use descriptive names (snake_case)
- Case-sensitive (age ≠ Age)
""",
                "exercise": "Create variables for your name, age, and favorite number. Print them all.",
                "solution": 'name = "Your Name"\nage = 20\nfavorite_number = 7\nprint(f"Name: {name}")\nprint(f"Age: {age}")\nprint(f"Favorite Number: {favorite_number}")',
                "quiz": [
                    {
                        "question": "Which data type represents whole numbers?",
                        "options": ["float", "int", "str", "bool"],
                        "correct": 1
                    },
                    {
                        "question": "What is the correct way to assign a string to a variable?",
                        "options": ["name = Alice", "name = 'Alice'", "str name = Alice", "name == 'Alice'"],
                        "correct": 1
                    }
                ]
            },
            {
                "id": "conditionals",
                "title": "If Statements & Logic",
                "description": "Make decisions in your code using conditional statements",
                "content": """
# If Statements & Logic

Conditional statements let your program make decisions based on conditions.

**Basic If Statement:**
```python
age = 18
if age >= 18:
    print("You are an adult")
```

**If-Else:**
```python
temperature = 30
if temperature > 25:
    print("It's hot!")
else:
    print("It's comfortable")
```

**If-Elif-Else:**
```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

**Comparison Operators:**
- `==` equal to
- `!=` not equal to
- `>` greater than
- `<` less than
- `>=` greater than or equal
- `<=` less than or equal
""",
                "exercise": "Write a program that checks if a number is positive, negative, or zero.",
                "solution": 'number = 5\nif number > 0:\n    print("Positive")\nelif number < 0:\n    print("Negative")\nelse:\n    print("Zero")',
                "quiz": [
                    {
                        "question": "What operator checks if two values are equal?",
                        "options": ["=", "==", "===", "!="],
                        "correct": 1
                    },
                    {
                        "question": "What will this print: if 5 > 3: print('Yes')",
                        "options": ["Yes", "No", "Error", "Nothing"],
                        "correct": 0
                    }
                ]
            },
            {
                "id": "loops",
                "title": "Loops: For & While",
                "description": "Repeat code efficiently with loops",
                "content": """
# Loops: For & While

Loops allow you to repeat code multiple times.

**For Loop (iterate over sequence):**
```python
# Loop through numbers
for i in range(5):
    print(i)  # prints 0, 1, 2, 3, 4

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

**While Loop (repeat while condition is true):**
```python
count = 0
while count < 5:
    print(count)
    count += 1  # increment by 1
```

**Loop Control:**
- `break` - exit the loop
- `continue` - skip to next iteration

```python
for i in range(10):
    if i == 5:
        break  # stops at 5
    print(i)
```

**Key Points:**
- Use `for` when you know how many iterations
- Use `while` when repeating until a condition changes
- Be careful of infinite loops!
""",
                "exercise": "Write a for loop that prints numbers from 1 to 10, but skip 5.",
                "solution": 'for i in range(1, 11):\n    if i == 5:\n        continue\n    print(i)',
                "quiz": [
                    {
                        "question": "How many times will this loop run: for i in range(3):",
                        "options": ["2", "3", "4", "infinite"],
                        "correct": 1
                    },
                    {
                        "question": "What keyword stops a loop immediately?",
                        "options": ["stop", "end", "break", "exit"],
                        "correct": 2
                    }
                ]
            }
        ]
    },
    "Functions & Modules": {
        "lessons": [
            {
                "id": "functions",
                "title": "Creating Functions",
                "description": "Organize code into reusable functions",
                "content": """
# Creating Functions

Functions are reusable blocks of code that perform specific tasks.

**Basic Function:**
```python
def greet():
    print("Hello!")

greet()  # Call the function
```

**Function with Parameters:**
```python
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")  # Output: Hello, Alice!
```

**Return Values:**
```python
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(result)  # Output: 8
```

**Default Parameters:**
```python
def greet(name="Guest"):
    return f"Hello, {name}!"

print(greet())          # Hello, Guest!
print(greet("Bob"))     # Hello, Bob!
```

**Why Use Functions?**
- Organize code into logical pieces
- Reuse code without duplication
- Make code easier to test and debug
- Improve readability
""",
                "exercise": "Create a function called 'square' that takes a number and returns its square.",
                "solution": 'def square(number):\n    return number * number\n\nprint(square(5))  # Output: 25\nprint(square(10)) # Output: 100',
                "quiz": [
                    {
                        "question": "What keyword is used to define a function?",
                        "options": ["function", "def", "func", "define"],
                        "correct": 1
                    },
                    {
                        "question": "What does 'return' do in a function?",
                        "options": ["Prints output", "Ends function and sends back a value", "Creates a loop", "Deletes the function"],
                        "correct": 1
                    }
                ]
            }
        ]
    },
    "Data Structures": {
        "lessons": [
            {
                "id": "lists",
                "title": "Lists & Arrays",
                "description": "Store and manipulate collections of data",
                "content": """
# Lists & Arrays

Lists store multiple items in a single variable.

**Creating Lists:**
```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

**Accessing Elements:**
```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])    # apple (first item)
print(fruits[-1])   # cherry (last item)
```

**Common Operations:**
```python
# Add items
fruits.append("orange")
fruits.insert(1, "grape")

# Remove items
fruits.remove("banana")
last = fruits.pop()

# Length
print(len(fruits))

# Check existence
if "apple" in fruits:
    print("Found!")
```

**Slicing:**
```python
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])    # [1, 2, 3]
print(numbers[:3])     # [0, 1, 2]
print(numbers[3:])     # [3, 4, 5]
```
""",
                "exercise": "Create a list of 5 numbers, add a new number, remove the first one, and print the result.",
                "solution": 'numbers = [10, 20, 30, 40, 50]\nnumbers.append(60)\nnumbers.pop(0)\nprint(numbers)  # [20, 30, 40, 50, 60]',
                "quiz": [
                    {
                        "question": "What index is the first element in a list?",
                        "options": ["1", "0", "-1", "first"],
                        "correct": 1
                    },
                    {
                        "question": "Which method adds an item to the end of a list?",
                        "options": ["add()", "append()", "insert()", "push()"],
                        "correct": 1
                    }
                ]
            }
        ]
    }
}

# --- STYLING ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #0f172a, #1e293b, #334155);
    background-size: 300% 300%;
    animation: gradientMove 12s ease infinite;
    color: #f1f5f9;
}

/* Ensure text is readable with high contrast */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
.stMarkdown h4, .stMarkdown li, .stMarkdown span, div, p, label, span {
    color: #f1f5f9 !important;
}

.stChatMessage {
    color: #f1f5f9 !important;
}

.stChatMessage p {
    color: #f1f5f9 !important;
}

/* Specific elements for better readability */
.stRadio label, .stCheckbox label, .stSelectbox label {
    color: #e2e8f0 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
}

/* Sidebar text styling */
.css-1d391kg, .css-1d391kg p, .css-1d391kg label, 
[data-testid="stSidebar"], [data-testid="stSidebar"] * {
    color: #1e293b !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
    color: #0f172a !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #334155 !important;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.hero-section {
    text-align: center;
    padding: 3rem 2rem;
    background: rgba(0, 180, 216, 0.1);
    border-radius: 20px;
    margin: 2rem 0;
    backdrop-filter: blur(10px);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(120deg, #00b4d8, #0077ff, #00eaff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}

.ai-badge {
    display: inline-block;
    background: linear-gradient(90deg, #00b4d8, #0077ff);
    padding: 0.5rem 1.5rem;
    border-radius: 25px;
    font-weight: 600;
    margin: 1rem 0;
    box-shadow: 0 0 20px rgba(0, 180, 216, 0.5);
}

.feature-card {
    background: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    border-left: 4px solid #00b4d8;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
    height: 100%;
}

.feature-card:hover {
    background: rgba(255,255,255,0.12);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 180, 216, 0.3);
}

.lesson-card {
    background: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid #00b4d8;
    backdrop-filter: blur(12px);
    cursor: pointer;
    transition: all 0.3s ease;
}

.lesson-card:hover {
    background: rgba(255,255,255,0.12);
    transform: translateX(5px);
    box-shadow: 0 8px 25px rgba(0, 180, 216, 0.3);
}

.completed {
    border-left-color: #10b981;
}

.stat-box {
    background: rgba(0, 180, 216, 0.15);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(0, 180, 216, 0.3);
}

.stTextArea textarea {
    background: rgba(15, 23, 42, 0.95) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(0, 180, 216, 0.3) !important;
    border-radius: 10px !important;
    font-family: 'Fira Code', 'Courier New', monospace !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    tab-size: 4 !important;
    -moz-tab-size: 4 !important;
}

/* IDE-style code editor */
.code-editor-container {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(0, 180, 216, 0.3);
    border-radius: 10px;
    padding: 10px;
}

.line-numbers {
    color: #64748b;
    user-select: none;
    padding-right: 10px;
    border-right: 1px solid rgba(100, 116, 139, 0.3);
    font-family: 'Fira Code', monospace;
}

.stTextInput input {
    background: rgba(15, 23, 42, 0.7) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(0, 180, 216, 0.3) !important;
}

.login-container {
    max-width: 450px;
    margin: 0 auto;
    padding: 2rem;
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.progress-bar {
    background: rgba(255,255,255,0.1);
    height: 30px;
    border-radius: 15px;
    overflow: hidden;
    margin: 1rem 0;
}

.progress-fill {
    background: linear-gradient(90deg, #00b4d8, #0077ff);
    height: 100%;
    transition: width 0.5s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("""
    <div class='hero-section'>
        <h1 class='hero-title'>🧠 LexIQ</h1>
        <div class='ai-badge'>✨ AI-Powered Learning Platform</div>
        <p style='font-size: 1.2rem; margin-top: 1rem;'>Learn Python through interactive AI conversations and instant code feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", use_container_width=True):
                users = load_users()
                hashed_pw = hash_password(login_password)
                
                if login_username in users and users[login_username] == hashed_pw:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.user_progress = load_user_progress(login_username)
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        with tab2:
            st.markdown("### Create Your Account")
            signup_username = st.text_input("Choose Username", key="signup_user")
            signup_password = st.text_input("Choose Password", type="password", key="signup_pass")
            signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("Create Account", use_container_width=True):
                if not signup_username or not signup_password:
                    st.error("Please fill in all fields")
                elif signup_password != signup_confirm:
                    st.error("Passwords don't match")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    users = load_users()
                    if signup_username in users:
                        st.error("Username already exists")
                    else:
                        users[signup_username] = hash_password(signup_password)
                        save_users(users)
                        st.success("✅ Account created! Please login.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature showcase
    st.markdown("### 🚀 Why LexIQ?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h2 style='font-size: 3rem; margin: 0;'>🤖</h2>
            <h3>AI Code Assistant</h3>
            <p>Chat with AI to understand code, debug errors, and get instant explanations. Learn by asking questions naturally.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h2 style='font-size: 3rem; margin: 0;'>⚡</h2>
            <h3>Vibe-Based Learning</h3>
            <p>No rigid structure. Learn at your pace, explore what interests you, and build real projects with AI guidance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h2 style='font-size: 3rem; margin: 0;'>📈</h2>
            <h3>Track Progress</h3>
            <p>Monitor your growth, earn achievements, and see your coding journey visualized with stats and milestones.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# --- LOGGED IN - MAIN APP ---

# Save progress periodically
if st.session_state.user_progress:
    save_user_progress(st.session_state.username, st.session_state.user_progress)

# Sidebar
st.sidebar.title(f"👋 Hey, {st.session_state.username}!")
if st.sidebar.button("🚪 Logout"):
    save_user_progress(st.session_state.username, st.session_state.user_progress)
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

page = st.sidebar.radio("", ["🏠 Home", "🤖 AI Assistant", "📚 Learn", "🎯 Projects", "📊 Progress"])

# Get API key
api_key = st.sidebar.text_input("Groq API Key", type="password", help="Enter your Groq API key")
st.sidebar.markdown("[Get free API key →](https://console.groq.com/keys)")

# --- HOME PAGE ---
if page == "🏠 Home":
    st.markdown("""
    <div class='hero-section'>
        <h1 class='hero-title'>Welcome to LexIQ</h1>
        <div class='ai-badge'>🤖 Your AI Coding Companion</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <h2>{st.session_state.user_progress['total_points']}</h2>
            <p>Total Points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-box'>
            <h2>{len(st.session_state.user_progress['completed_lessons'])}</h2>
            <p>Lessons Done</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-box'>
            <h2>{st.session_state.user_progress['current_streak']}</h2>
            <p>Day Streak</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_lessons = sum(len(track['lessons']) for track in CURRICULUM.values())
        completion = len(st.session_state.user_progress['completed_lessons']) / total_lessons * 100 if total_lessons > 0 else 0
        st.markdown(f"""
        <div class='stat-box'>
            <h2>{completion:.0f}%</h2>
            <p>Complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h2>🤖 AI Assistant</h2>
            <p style='font-size: 1.1rem;'>Your main learning tool! Chat with AI to:</p>
            <ul style='text-align: left; margin-top: 1rem;'>
                <li>Explain any code you paste</li>
                <li>Debug and fix errors</li>
                <li>Get coding suggestions</li>
                <li>Ask questions naturally</li>
                <li>Build projects together</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Open AI Assistant", use_container_width=True, type="primary"):
            st.session_state.page = "🤖 AI Assistant"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h2>📚 Structured Learning</h2>
            <p style='font-size: 1.1rem;'>Optional guided path with:</p>
            <ul style='text-align: left; margin-top: 1rem;'>
                <li>Curated lessons & tutorials</li>
                <li>Practice exercises</li>
                <li>Knowledge quizzes</li>
                <li>Progress tracking</li>
                <li>Coding challenges</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📖 Browse Lessons", use_container_width=True):
            st.session_state.page = "📚 Learn"
            st.rerun()

# --- AI ASSISTANT PAGE (MAIN FEATURE) ---
elif page == "🤖 AI Assistant":
    st.title("🤖 Your AI Coding Assistant")
    st.markdown("### Learn by building - step by step!")
    
    # Initialize session states
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_code' not in st.session_state:
        st.session_state.current_code = ""
    if 'pending_changes' not in st.session_state:
        st.session_state.pending_changes = []
    if 'learning_mode' not in st.session_state:
        st.session_state.learning_mode = True
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 💬 Chat with AI")
        
        # Display chat history
        chat_container = st.container(height=400)
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about code, request features, or get help..."):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Get AI response
            if api_key:
                try:
                    client = Groq(api_key=api_key)
                    with st.spinner("Thinking..."):
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are LexIQ, a Socratic coding tutor. Your goal is to help users LEARN through discovery, not just give answers.\n\n"
                                        "CRITICAL TEACHING PHILOSOPHY:\n"
                                        "1. NEVER give complete code solutions directly - make them work for it\n"
                                        "2. Be intentionally vague at first - give hints, not answers\n"
                                        "3. Ask probing questions to guide their thinking\n"
                                        "4. Only reveal code after they've attempted to understand the concept\n"
                                        "5. Break complex tasks into tiny micro-steps\n"
                                        "6. Make them ask follow-up questions to get more detail\n"
                                        "7. When debugging, point to the AREA of the problem, not the exact fix\n"
                                        "8. Challenge their assumptions with questions\n\n"
                                        "RESPONSE PATTERN:\n"
                                        "- First response: Ask what they're trying to achieve and what they've tried\n"
                                        "- Second response: Give a conceptual hint or ask about their understanding\n"
                                        "- Third response: Maybe show a small piece of pseudocode or pattern\n"
                                        "- Fourth+ response: Only then consider showing actual code, one tiny piece at a time\n\n"
                                        "When they ask for help building something:\n"
                                        "- Ask: 'What's the first step you think we need?'\n"
                                        "- Ask: 'How would you approach this?'\n"
                                        "- Ask: 'What do you already know that might help here?'\n\n"
                                        "When debugging:\n"
                                        "- Ask: 'What do you think this error means?'\n"
                                        "- Say: 'Look at line X - what's happening there?'\n"
                                        "- Ask: 'What values do you expect vs what are you getting?'\n\n"
                                        "Format code suggestions ONLY after discussion like:\n"
                                        "CONCEPT: [explain the idea]\n"
                                        "QUESTION: [check their understanding]\n"
                                        "If they answer correctly, THEN:\n"
                                        "CODE_CHANGE:\n```python\n[tiny code snippet - 1-3 lines max]\n```\n"
                                        "WHY: [explain this specific piece]\n"
                                        "NEXT: [what should they think about next?]\n\n"
                                        f"Current code:\n{st.session_state.current_code}\n\n"
                                        "Be patient, ask questions, and make them think. Learning happens through struggle."
                                    )
                                },
                                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[-10:]]
                            ],
                            temperature=0.4,
                        )
                        ai_message = response.choices[0].message.content
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_message})
                        
                        # Check if AI suggested a code change
                        if "```python" in ai_message:
                            # Extract code snippet
                            code_start = ai_message.find("```python") + 9
                            code_end = ai_message.find("```", code_start)
                            code_snippet = ai_message[code_start:code_end].strip()
                            
                            # Extract explanation (text before code)
                            explanation = ai_message[:ai_message.find("```python")].strip()
                            
                            # Add to pending changes
                            st.session_state.pending_changes.append({
                                'explanation': explanation,
                                'code': code_snippet
                            })
                        
                        # Award points for interaction
                        st.session_state.user_progress['total_points'] += 5
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "⚠️ Please add your Groq API key in the sidebar to use the AI assistant!"
                })
                st.rerun()
    
    with col2:
        st.markdown("#### 💻 Your Code Workspace")
        
        # Code editor
        st.session_state.current_code = st.text_area(
            "Write your code here:",
            value=st.session_state.current_code,
            height=300,
            key="code_workspace"
        )
        
        # Pending changes section
        if st.session_state.pending_changes:
            st.markdown("---")
            st.markdown("#### 📝 Suggested Change")
            
            change = st.session_state.pending_changes[0]
            
            with st.container():
                st.markdown("**Understanding the change:**")
                st.info(change['explanation'])
                
                st.markdown("**Proposed code:**")
                st.code(change['code'], language='python')
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("✅ Apply Change", use_container_width=True):
                        # Apply the change to current code
                        st.session_state.current_code += "\n\n" + change['code']
                        st.session_state.pending_changes.pop(0)
                        st.session_state.user_progress['total_points'] += 10
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": "I applied the change. What's next?"
                        })
                        st.rerun()
                
                with col_b:
                    if st.button("❓ Explain More", use_container_width=True):
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": f"Can you explain this in more detail? I don't fully understand:\n```python\n{change['code']}\n```"
                        })
                        st.rerun()
                
                with col_c:
                    if st.button("❌ Skip", use_container_width=True):
                        st.session_state.pending_changes.pop(0)
                        st.rerun()
        
        # Quick action buttons
        st.markdown("---")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("🔍 Explain My Code", use_container_width=True):
                if st.session_state.current_code:
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": f"I wrote this code. Can you help me understand what it does?\n```python\n{st.session_state.current_code}\n```"
                    })
                    st.rerun()
                else:
                    st.warning("Write some code first!")
        with col_y:
            if st.button("🐛 Help Debug", use_container_width=True):
                if st.session_state.current_code:
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": f"Something's wrong with my code. Can you help me find the issue?\n```python\n{st.session_state.current_code}\n```"
                    })
                    st.rerun()
                else:
                    st.warning("Write some code first!")
    
    # Sidebar quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Quick Actions")
    
    if st.sidebar.button("🔄 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.sidebar.button("📝 New Project"):
        st.session_state.current_code = ""
        st.session_state.chat_history = []
        st.session_state.pending_changes = []
        st.rerun()
    
    st.sidebar.markdown("### 🎯 Try asking:")
    st.sidebar.markdown("""
    - "Help me build a calculator"
    - "How do I make a guessing game?"
    - "I want to create a to-do list"
    - "Why isn't my code working?"
    - "What should I learn next?"
    """)

# --- LEARN PAGE ---
elif page == "📚 Learn":
    st.title("📚 Structured Learning Path")
    st.markdown("*Optional: Use these lessons to build foundational knowledge*")
    
    for track_name, track_data in CURRICULUM.items():
        st.markdown(f"### {track_name}")
        
        for lesson in track_data['lessons']:
            is_completed = lesson['id'] in st.session_state.user_progress['completed_lessons']
            status = "✅" if is_completed else "📖"
            card_class = "lesson-card completed" if is_completed else "lesson-card"
            
            with st.container():
                st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{status} {lesson['title']}**")
                    st.markdown(f"<small>{lesson['description']}</small>", unsafe_allow_html=True)
                with col2:
                    if st.button("Open →", key=f"open_{lesson['id']}"):
                        st.session_state.current_lesson = lesson
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Display selected lesson
    if st.session_state.current_lesson:
        lesson = st.session_state.current_lesson
        st.markdown("---")
        st.markdown(f"## {lesson['title']}")
        
        st.markdown(lesson['content'])
        
        st.markdown("### 💪 Practice Exercise")
        st.info(lesson['exercise'])
        
        user_code = st.text_area("Your Solution:", height=150, key="exercise_code")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🤖 Ask AI for Help"):
                if api_key and user_code:
                    try:
                        client = Groq(api_key=api_key)
                        with st.spinner("Getting AI feedback..."):
                            response = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {"role": "system", "content": "You are a helpful coding tutor. Review student code and provide constructive feedback."},
                                    {"role": "user", "content": f"Exercise: {lesson['exercise']}\n\nStudent's code:\n{user_code}\n\nProvide feedback."}
                                ],
                                temperature=0.3,
                            )
                            st.success("AI Feedback:")
                            st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please enter API key and code.")
        
        with col2:
            if st.button("👀 Show Solution"):
                st.code(lesson['solution'], language='python')
        
        with col3:
            if st.button("✅ Mark Complete"):
                if lesson['id'] not in st.session_state.user_progress['completed_lessons']:
                    st.session_state.user_progress['completed_lessons'].append(lesson['id'])
                    st.session_state.user_progress['total_points'] += 50
                    st.success("🎉 Lesson completed! +50 points")
                    st.balloons()
                    st.rerun()
        
        # Quiz
        st.markdown("### 🎯 Knowledge Check")
        for i, q in enumerate(lesson['quiz']):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            answer = st.radio("", q['options'], key=f"q_{lesson['id']}_{i}")
            if st.button("Submit Answer", key=f"submit_{lesson['id']}_{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success("✅ Correct!")
                    st.session_state.user_progress['total_points'] += 10
                else:
                    st.error(f"❌ Wrong. Correct answer: {q['options'][q['correct']]}")

# --- PROJECTS PAGE ---
elif page == "🎯 Projects":
    st.title("🎯 Guided Projects")
    st.markdown("### Build real projects with AI guidance - you write every line!")
    
    # Initialize project session state
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = None
    if 'project_code' not in st.session_state:
        st.session_state.project_code = ""
    if 'project_chat' not in st.session_state:
        st.session_state.project_chat = []
    if 'project_progress' not in st.session_state:
        st.session_state.project_progress = 0
    if 'code_given' not in st.session_state:
        st.session_state.code_given = False
    
    projects = [
        {
            "id": "calculator",
            "title": "🧮 Calculator App",
            "difficulty": "Beginner",
            "description": "Build a basic calculator that can add, subtract, multiply, and divide numbers.",
            "skills": ["Functions", "User Input", "Conditionals", "Math Operations"],
            "starter_prompt": "Let's build a calculator together! I'll guide you step by step. First, what do you think the calculator needs to do?",
            "help_level": 5  # 5 = most help, 1 = least help
        },
        {
            "id": "guess_number",
            "title": "🎲 Number Guessing Game",
            "difficulty": "Beginner",
            "description": "Create a game where the computer picks a random number and the user tries to guess it.",
            "skills": ["Random Module", "Loops", "Conditionals", "User Input"],
            "starter_prompt": "We're building a guessing game! The computer will pick a number and the player guesses. What's the first thing we need to do?",
            "help_level": 5
        },
        {
            "id": "quiz_game",
            "title": "📝 Quiz Game",
            "difficulty": "Beginner",
            "description": "Create a multiple-choice quiz game that tracks the score.",
            "skills": ["Lists", "Dictionaries", "Loops", "Conditionals"],
            "starter_prompt": "We're building a quiz game! It will ask questions and track the score. How should we store the questions and answers?",
            "help_level": 4
        },
        {
            "id": "todo_list",
            "title": "✅ To-Do List Manager",
            "difficulty": "Intermediate",
            "description": "Build a to-do list where users can add, remove, and view tasks.",
            "skills": ["Lists", "Loops", "Functions", "String Manipulation"],
            "starter_prompt": "Let's create a to-do list app! Users should be able to add, view, and remove tasks. What data structure would work well for storing tasks?",
            "help_level": 3
        },
        {
            "id": "password_gen",
            "title": "🔐 Password Generator",
            "difficulty": "Intermediate",
            "description": "Create a tool that generates secure random passwords based on user preferences.",
            "skills": ["Random Module", "Strings", "Loops", "User Input"],
            "starter_prompt": "We're building a password generator! It should create random passwords with letters, numbers, and symbols. What's your first thought on how to approach this?",
            "help_level": 3
        },
        {
            "id": "hangman",
            "title": "🎮 Hangman Game",
            "difficulty": "Intermediate",
            "description": "Build the classic word guessing game with lives and letter tracking.",
            "skills": ["Lists", "Strings", "Loops", "Conditionals", "Game Logic"],
            "starter_prompt": "Let's make Hangman! Players guess letters to find a hidden word. What are the main components we need to track?",
            "help_level": 2
        },
        {
            "id": "contact_book",
            "title": "📇 Contact Book",
            "difficulty": "Intermediate",
            "description": "Build a contact manager to store names, phone numbers, and emails.",
            "skills": ["Dictionaries", "Lists", "Functions", "File I/O"],
            "starter_prompt": "Let's create a contact book! Users can add, search, and delete contacts. What's the best way to store contact information?",
            "help_level": 2
        },
        {
            "id": "text_adventure",
            "title": "🗺️ Text Adventure Game",
            "difficulty": "Advanced",
            "description": "Create an interactive story game where choices affect the outcome.",
            "skills": ["Functions", "Dictionaries", "Conditionals", "Game Design"],
            "starter_prompt": "We're building a text adventure! Players make choices that change the story. How should we structure the game flow?",
            "help_level": 1
        }
    ]
    
    if not st.session_state.selected_project:
        # Project selection grid
        st.markdown("### Choose Your Project")
        
        cols = st.columns(2)
        for i, project in enumerate(projects):
            with cols[i % 2]:
                difficulty_color = {
                    "Beginner": "🟢",
                    "Intermediate": "🟡", 
                    "Advanced": "🔴"
                }
                
                st.markdown(f"""
                <div class='feature-card' style='min-height: 200px;'>
                    <h3>{project['title']}</h3>
                    <p style='font-size: 0.9rem; opacity: 0.8;'>{difficulty_color[project['difficulty']]} {project['difficulty']}</p>
                    <p>{project['description']}</p>
                    <p style='font-size: 0.85rem; margin-top: 1rem;'><strong>Skills:</strong> {', '.join(project['skills'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start Project", key=f"start_{project['id']}", use_container_width=True):
                    st.session_state.selected_project = project
                    st.session_state.project_code = f"# {project['title']}\n# Let's build this together!\n\n"
                    st.session_state.project_chat = [{
                        "role": "assistant",
                        "content": project['starter_prompt']
                    }]
                    st.session_state.project_progress = 0
                    st.session_state.code_given = False
                    st.rerun()
    
    else:
        # Project workspace
        project = st.session_state.selected_project
        
        col1, col2 = st.columns([1, 1])
        
        # Back button
        if st.button("← Back to Projects"):
            st.session_state.selected_project = None
            st.session_state.project_code = ""
            st.session_state.project_chat = []
            st.session_state.project_progress = 0
            st.session_state.code_given = False
            st.rerun()
        
        st.markdown(f"## {project['title']}")
        st.markdown(f"**Goal:** {project['description']}")
        
        with col1:
            st.markdown("#### 💬 AI Guide")
            
            # Chat container
            chat_container = st.container(height=450)
            with chat_container:
                for message in st.session_state.project_chat:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask for guidance or share your progress..."):
                st.session_state.project_chat.append({"role": "user", "content": prompt})
                
                if api_key:
                    try:
                        client = Groq(api_key=api_key)
                        with st.spinner("AI is thinking..."):
                            # Determine help level based on project difficulty
                            help_level = project.get('help_level', 3)
                            
                            # Progressive help system
                            if help_level >= 4:  # Beginner projects
                                guidance_style = (
                                    "HELP LEVEL: HIGH (Beginner Project)\n"
                                    "- Give detailed explanations and clear guidance\n"
                                    "- After 2-3 good responses from student, provide starter code snippets they can type\n"
                                    "- Show code structure and patterns\n"
                                    "- Example: 'Here's how you could start: [code snippet]'\n"
                                    "- Break down into very small steps\n"
                                )
                            elif help_level == 3:  # Easy Intermediate
                                guidance_style = (
                                    "HELP LEVEL: MEDIUM (Intermediate Project)\n"
                                    "- Give conceptual guidance with some code hints\n"
                                    "- After 3-4 thoughtful responses, provide small code examples\n"
                                    "- Show patterns but make them adapt it\n"
                                    "- More questions, fewer direct answers\n"
                                )
                            elif help_level == 2:  # Hard Intermediate
                                guidance_style = (
                                    "HELP LEVEL: LOW (Challenging Project)\n"
                                    "- Mostly ask questions and give conceptual hints\n"
                                    "- Only after 5+ quality interactions, show pseudocode or minimal examples\n"
                                    "- Make them figure out most of the implementation\n"
                                    "- Focus on guiding their problem-solving process\n"
                                )
                            else:  # Advanced
                                guidance_style = (
                                    "HELP LEVEL: MINIMAL (Advanced Project)\n"
                                    "- Ask deep questions about architecture and design\n"
                                    "- Rarely give code - only high-level patterns if really stuck\n"
                                    "- Challenge them to think through edge cases\n"
                                    "- Make them discover solutions through questioning\n"
                                )
                            
                            # Check if student is making progress
                            progress_indicators = ["i think", "maybe", "should i", "how about", "what if"]
                            shows_effort = any(indicator in prompt.lower() for indicator in progress_indicators)
                            
                            system_prompt = (
                                f"You are guiding a student to build: {project['title']}\n"
                                f"Project goal: {project['description']}\n\n"
                                f"{guidance_style}\n\n"
                                "INTERACTION REWARDS SYSTEM:\n"
                                "Track student engagement:\n"
                                "- If they ask thoughtful questions → praise and guide forward\n"
                                "- If they share their thinking → acknowledge and build on it\n"
                                "- If they try something → celebrate attempt even if wrong\n"
                                "- After consistent good engagement → reward with starter code\n\n"
                                "CODE GIVING RULES:\n"
                                "When providing code:\n"
                                "1. Format it clearly so they can TYPE it (not copy-paste mentally)\n"
                                "2. Add comments explaining each part\n"
                                "3. Keep it small - 3-10 lines max\n"
                                "4. Say 'Try typing this out:' before code\n"
                                "5. Ask them to explain it back after typing\n\n"
                                "Example starter code format:\n"
                                "```python\n"
                                "# This creates our main function\n"
                                "def calculator():\n"
                                "    # We'll add the logic here\n"
                                "    pass\n"
                                "```\n\n"
                                "CRITICAL: Adjust help amount based on project difficulty.\n"
                                "Beginner = more code snippets, Advanced = mostly questions.\n\n"
                                f"""Student's engagement level: {"HIGH - they're thinking!" if shows_effort else "Check their understanding"}\n\n"""

                                f"Current student code:\n{st.session_state.project_code}\n\n"
                                "Be encouraging, adaptive, and help them build confidence through incremental success."
                            )
                            
                            response = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.project_chat[-10:]]
                                ],
                                temperature=0.5,
                            )
                            ai_message = response.choices[0].message.content
                            st.session_state.project_chat.append({"role": "assistant", "content": ai_message})
                            
                            # Track progress
                            if shows_effort:
                                st.session_state.project_progress += 1
                            
                            # Give code after sufficient engagement
                            if "```python" in ai_message:
                                st.session_state.code_given = True
                            
                            st.session_state.user_progress['total_points'] += 5
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.session_state.project_chat.append({
                        "role": "assistant",
                        "content": "⚠️ Please add your Groq API key in the sidebar!"
                    })
                    st.rerun()
        
        with col2:
            st.markdown("#### 💻 Your Code")
            
            # IDE-style code editor with JavaScript for tab support
            st.markdown("""
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                const textareas = document.querySelectorAll('textarea');
                textareas.forEach(textarea => {
                    textarea.addEventListener('keydown', function(e) {
                        // Tab key support
                        if (e.key === 'Tab') {
                            e.preventDefault();
                            const start = this.selectionStart;
                            const end = this.selectionEnd;
                            const value = this.value;
                            
                            // Insert 4 spaces
                            this.value = value.substring(0, start) + '    ' + value.substring(end);
                            this.selectionStart = this.selectionEnd = start + 4;
                        }
                        
                        // Auto-indent on Enter
                        if (e.key === 'Enter') {
                            const start = this.selectionStart;
                            const value = this.value;
                            const lines = value.substring(0, start).split('\\n');
                            const currentLine = lines[lines.length - 1];
                            
                            // Count leading spaces
                            const leadingSpaces = currentLine.match(/^\\s*/)[0];
                            
                            // Check if line ends with : (function, if, for, while, etc.)
                            const needsExtraIndent = currentLine.trim().endsWith(':');
                            
                            setTimeout(() => {
                                const newStart = this.selectionStart;
                                const indent = needsExtraIndent ? leadingSpaces + '    ' : leadingSpaces;
                                this.value = this.value.substring(0, newStart) + indent + this.value.substring(newStart);
                                this.selectionStart = this.selectionEnd = newStart + indent.length;
                            }, 0);
                        }
                    });
                });
            });
            </script>
            """, unsafe_allow_html=True)
            
            # Code editor with line numbers feel
            st.markdown("<div class='code-editor-container'>", unsafe_allow_html=True)
            st.session_state.project_code = st.text_area(
                "Type your code here (Tab for indent, Enter auto-indents):",
                value=st.session_state.project_code,
                height=450,
                key="project_workspace",
                help="💡 Use Tab key for indentation. After typing ':', press Enter to auto-indent!"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Progress indicator
            if st.session_state.project_progress > 0:
                st.info(
    f"""🎯 Engagement Level: {min(st.session_state.project_progress, 5)}/5 - 
    {'Keep going!' if st.session_state.project_progress < 5 else "You're doing great!"}"""
)

            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("💡 Give Hint", use_container_width=True):
                    st.session_state.project_chat.append({
                        "role": "user",
                        "content": "I'm stuck. Can you give me a hint about what to do next?"
                    })
                    st.rerun()
            
            with col_b:
                if st.button("✅ Check Progress", use_container_width=True):
                    st.session_state.project_chat.append({
                        "role": "user",
                        "content": f"Here's my current code. Am I on the right track?\n```python\n{st.session_state.project_code}\n```"
                    })
                    st.rerun()
            
            with col_c:
                if st.button("🎯 What's Next?", use_container_width=True):
                    st.session_state.project_chat.append({
                        "role": "user",
                        "content": "What should I work on next?"
                    })
                    st.rerun()
        
        # Progress indicator
        st.markdown("---")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown("**💪 Skills You're Building:** " + ", ".join(project['skills']))
        with col_info2:
            difficulty_info = {
                "Beginner": "🟢 More guidance & starter code",
                "Intermediate": "🟡 Moderate hints",
                "Advanced": "🔴 Minimal help - you got this!"
            }
            st.markdown("**📊 Difficulty:** " + difficulty_info.get(project['difficulty'], ""))
        
        if st.button("✅ Mark Project Complete", type="primary"):
            st.session_state.user_progress['total_points'] += 100
            st.session_state.user_progress['completed_lessons'].append(f"project_{project['id']}")
            st.success(f"🎉 Awesome! You completed {project['title']}! +100 points")
            st.balloons()
            st.session_state.selected_project = None
            st.session_state.project_code = ""
            st.session_state.project_chat = []
            st.session_state.project_progress = 0
            st.session_state.code_given = False
            st.rerun()

# --- PROGRESS PAGE ---
elif page == "📊 Progress":
    st.title("📊 Your Progress")
    
    total_lessons = sum(len(track['lessons']) for track in CURRICULUM.values())
    completed = len(st.session_state.user_progress['completed_lessons'])
    progress_pct = (completed / total_lessons * 100) if total_lessons > 0 else 0
    
    st.markdown(f"""
    <div class='progress-bar'>
        <div class='progress-fill' style='width: {progress_pct}%'>
            {progress_pct:.0f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**{completed} of {total_lessons} lessons completed**")
    
    st.markdown("---")
    st.markdown("### 🏆 Achievements")
    
    achievements = [
        ("🎯", "First Steps", "Complete your first lesson", completed >= 1),
        ("🔥", "On Fire", "Complete 5 lessons", completed >= 5),
        ("📚", "Bookworm", "Complete an entire track", completed >= 3),
        ("💯", "Code Master", "Earn 500 points", st.session_state.user_progress['total_points'] >= 500),
    ]
    
    cols = st.columns(4)
    for i, (emoji, title, desc, unlocked) in enumerate(achievements):
        with cols[i]:
            opacity = "1.0" if unlocked else "0.3"
            st.markdown(f"""
            <div style='text-align: center; opacity: {opacity}'>
                <div style='font-size: 48px'>{emoji}</div>
                <strong>{title}</strong><br>
                <small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Learning Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Points", st.session_state.user_progress['total_points'])
        st.metric("Code Submissions", len(st.session_state.user_progress['code_submissions']))
    with col2:
        st.metric("Current Streak", f"{st.session_state.user_progress['current_streak']} days")
        st.metric("Lessons Remaining", total_lessons - completed)
