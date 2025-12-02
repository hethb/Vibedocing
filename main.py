import streamlit as st
from groq import Groq
import json
import os
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="LexIQ - Learn to Code", page_icon="🧠", layout="wide")

# --- SESSION STATE INIT ---
if 'user_progress' not in st.session_state:
    st.session_state.user_progress = {
        'completed_lessons': [],
        'quiz_scores': {},
        'code_submissions': [],
        'current_streak': 0,
        'total_points': 0
    }

if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None

# --- LOAD CURRICULUM ---
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

.stat-box {
    background: rgba(0, 180, 216, 0.15);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(0, 180, 216, 0.3);
}

.code-editor {
    background: rgba(15, 23, 42, 0.95) !important;
    border: 1px solid rgba(0, 180, 216, 0.3) !important;
    border-radius: 10px !important;
    font-family: 'Fira Code', 'Source Code Pro', monospace !important;
    font-size: 14px !important;
}

.stTextArea textarea {
    background: rgba(15, 23, 42, 0.95) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(0, 180, 216, 0.3) !important;
    border-radius: 10px !important;
    font-family: 'Fira Code', monospace !important;
}

.quiz-option {
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.quiz-option:hover {
    background: rgba(0, 180, 216, 0.2);
    border-color: #00b4d8;
}

.correct-answer {
    background: rgba(16, 185, 129, 0.2) !important;
    border-color: #10b981 !important;
}

.wrong-answer {
    background: rgba(239, 68, 68, 0.2) !important;
    border-color: #ef4444 !important;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧠 LexIQ")
page = st.sidebar.radio("Navigate", ["🏠 Dashboard", "📚 Learn", "💻 Code Lab", "🎯 Practice", "📊 Progress"])

# Get API key
api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get your free key at console.groq.com")
st.sidebar.markdown("[Get API Key →](https://console.groq.com/keys)")

# --- DASHBOARD PAGE ---
if page == "🏠 Dashboard":
    st.title("Welcome to LexIQ! 🚀")
    st.markdown("### Your Personal Python Learning Platform")
    
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
    st.markdown("### 🎯 Quick Start")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Start Learning", use_container_width=True):
            st.session_state.page = "📚 Learn"
            st.rerun()
    with col2:
        if st.button("💻 Open Code Lab", use_container_width=True):
            st.session_state.page = "💻 Code Lab"
            st.rerun()

# --- LEARN PAGE ---
elif page == "📚 Learn":
    st.title("📚 Learning Path")
    
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
        
        # Content
        st.markdown(lesson['content'])
        
        # Exercise
        st.markdown("### 💪 Practice Exercise")
        st.info(lesson['exercise'])
        
        user_code = st.text_area("Your Solution:", height=150, key="exercise_code")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Check with AI"):
                if api_key and user_code:
                    try:
                        client = Groq(api_key=api_key)
                        with st.spinner("Reviewing your code..."):
                            response = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {"role": "system", "content": "You are a helpful coding tutor. Review the student's code and provide constructive feedback."},
                                    {"role": "user", "content": f"Exercise: {lesson['exercise']}\n\nStudent's code:\n{user_code}\n\nProvide feedback on correctness and suggestions."}
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
        
        # Quiz
        st.markdown("### 🎯 Knowledge Check")
        score = 0
        for i, q in enumerate(lesson['quiz']):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            answer = st.radio("", q['options'], key=f"q_{lesson['id']}_{i}")
            if st.button("Submit", key=f"submit_{lesson['id']}_{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success("✅ Correct!")
                    score += 1
                else:
                    st.error(f"❌ Wrong. Correct answer: {q['options'][q['correct']]}")
        
        if st.button("✅ Mark as Complete"):
            if lesson['id'] not in st.session_state.user_progress['completed_lessons']:
                st.session_state.user_progress['completed_lessons'].append(lesson['id'])
                st.session_state.user_progress['total_points'] += 50
                st.success("🎉 Lesson completed! +50 points")
                st.balloons()
                st.rerun()

# --- CODE LAB PAGE ---
elif page == "💻 Code Lab":
    st.title("💻 Interactive Code Lab")
    st.markdown("Write code and get instant AI explanations!")
    
    code_input = st.text_area("Write your Python code:", height=200, key="code_lab")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Explain Code", use_container_width=True):
            if api_key and code_input:
                try:
                    client = Groq(api_key=api_key)
                    with st.spinner("Analyzing..."):
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Explain code line by line for beginners."},
                                {"role": "user", "content": f"Explain:\n\n{code_input}"}
                            ],
                            temperature=0.3,
                        )
                        st.markdown("### 📖 Explanation")
                        st.info(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        if st.button("🐛 Debug Code", use_container_width=True):
            if api_key and code_input:
                try:
                    client = Groq(api_key=api_key)
                    with st.spinner("Finding bugs..."):
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Find bugs and suggest fixes."},
                                {"role": "user", "content": f"Debug:\n\n{code_input}"}
                            ],
                            temperature=0.3,
                        )
                        st.markdown("### 🐛 Debug Report")
                        st.warning(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col3:
        if st.button("✨ Improve Code", use_container_width=True):
            if api_key and code_input:
                try:
                    client = Groq(api_key=api_key)
                    with st.spinner("Optimizing..."):
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Suggest improvements for better code quality."},
                                {"role": "user", "content": f"Improve:\n\n{code_input}"}
                            ],
                            temperature=0.3,
                        )
                        st.markdown("### ✨ Improvements")
                        st.success(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- PRACTICE PAGE ---
elif page == "🎯 Practice":
    st.title("🎯 Coding Challenges")
    st.markdown("Test your skills with these challenges!")
    
    challenges = [
        {
            "title": "FizzBuzz",
            "difficulty": "Easy",
            "description": "Print numbers 1-100. For multiples of 3 print 'Fizz', for 5 print 'Buzz', for both print 'FizzBuzz'.",
            "hint": "Use modulo operator (%) to check divisibility"
        },
        {
            "title": "Palindrome Checker",
            "difficulty": "Easy",
            "description": "Write a function that checks if a string is a palindrome (reads same forwards and backwards).",
            "hint": "Compare string with its reverse"
        },
        {
            "title": "Sum of List",
            "difficulty": "Easy",
            "description": "Create a function that calculates the sum of all numbers in a list without using sum().",
            "hint": "Use a loop to add each element"
        }
    ]
    
    for challenge in challenges:
        with st.expander(f"{'🟢' if challenge['difficulty'] == 'Easy' else '🟡'} {challenge['title']} - {challenge['difficulty']}"):
            st.markdown(f"**Challenge:** {challenge['description']}")
            st.markdown(f"💡 *Hint: {challenge['hint']}*")
            
            solution = st.text_area("Your solution:", key=f"challenge_{challenge['title']}", height=150)
            
            if st.button("Submit Solution", key=f"submit_{challenge['title']}"):
                if api_key and solution:
                    try:
                        client = Groq(api_key=api_key)
                        with st.spinner("Reviewing..."):
                            response = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {"role": "system", "content": "Review coding challenge solutions. Give score out of 10 and feedback."},
                                    {"role": "user", "content": f"Challenge: {challenge['description']}\n\nSolution:\n{solution}"}
                                ],
                                temperature=0.3,
                            )
                            st.success("AI Review:")
                            st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")

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
        ("📚", "Bookworm", "Complete an entire track", False),
        ("💯", "Perfect Score", "Get 100% on a quiz", False),
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
