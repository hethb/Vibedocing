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
    color: white;
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
    font-family: 'Fira Code', monospace !important;
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

page = st.sidebar.radio("", ["🏠 Home", "🤖 AI Assistant", "📚 Learn", "🎯 Challenges", "📊 Progress"])

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
    st.markdown("### Paste code, ask questions, get help - learn by doing!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Paste code or ask a question..."):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        if api_key:
            try:
                client = Groq(api_key=api_key)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are LexIQ, a friendly AI coding tutor. "
                                        "Help users learn Python by explaining code clearly, debugging errors, "
                                        "answering questions, and providing guidance. Be conversational and encouraging. "
                                        "When explaining code, break it down line by line. "
                                        "When debugging, identify the issue and suggest fixes. "
                                        "Always encourage learning by asking if they have follow-up questions."
                                    )
                                },
                                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                            ],
                            temperature=0.4,
                        )
                        ai_message = response.choices[0].message.content
                        st.markdown(ai_message)
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_message})
                        
                        # Award points for interaction
                        st.session_state.user_progress['total_points'] += 5
                        st.session_state.user_progress['code_submissions'].append({
                            'timestamp': datetime.now().isoformat(),
                            'prompt': prompt
                        })
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            with st.chat_message("assistant"):
                st.warning("⚠️ Please add your Groq API key in the sidebar to use the AI assistant!")
    
    # Sidebar quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Quick Actions")
    
    if st.sidebar.button("🔄 New Conversation"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.sidebar.markdown("### 🎯 Try asking:")
    st.sidebar.markdown("""
    - "Explain this code: [paste code]"
    - "How do I create a function?"
    - "Debug this error: [error message]"
    - "What's the difference between lists and tuples?"
    - "Help me build a calculator"
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
                        ai_feedback = response.choices[0].message['content']
                        st.success("AI Feedback:")
                        st.markdown(ai_feedback)

                    except Exception as e:
                        st.error(f"Error: {e}")
