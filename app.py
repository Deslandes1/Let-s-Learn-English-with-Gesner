import streamlit as st
import asyncio
import edge_tts
import tempfile
import base64
import os
import random

# ------------------------------
# PAGE CONFIG & LOGIN
# ------------------------------
st.set_page_config(page_title="Let's Learn English with Gesner", layout="wide")

# Colorful CSS with WHITE BACKGROUND for main content area
def set_colorful_style():
    st.markdown(
        """
        <style>
        /* Overall app background (the outer area) remains dark */
        .stApp {
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e);
        }
        /* Main content container (where tabs and lesson content go) – white background */
        .main-content {
            background-color: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: 1rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        /* Header stays colorful */
        .main-header {
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb);
            padding: 1.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .main-header h1 {
            color: white;
            text-shadow: 2px 2px 4px #000000;
            font-size: 2.5rem;
            margin: 0;
        }
        .main-header p {
            color: #fff5cc;
            font-size: 1.2rem;
            margin: 0;
        }
        /* All text inside main content area should be dark (black/dark gray) */
        .main-content .stMarkdown,
        .main-content .stText,
        .main-content .stRadio label,
        .main-content .stSelectbox label,
        .main-content .stTextInput label {
            color: #1e1e2f !important;
        }
        .main-content .stText {
            color: #1e1e2f !important;
            font-size: 1rem;
        }
        /* Quiz radio button options – light background with dark text */
        .main-content .stRadio [role="radiogroup"] label {
            background: #f0f0f0;
            border-radius: 10px;
            padding: 0.3rem;
            margin: 0.2rem 0;
            color: #1e1e2f !important;
        }
        /* Buttons */
        .stButton button {
            background-color: #ff6b6b;
            color: white;
            border-radius: 30px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #feca57;
            color: black;
        }
        /* Sidebar remains dark with original styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e);
        }
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stText,
        section[data-testid="stSidebar"] label {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_logo():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="3"/>
                <defs>
                    <linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#ff007f;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#ffcc00;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#00ffcc;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
        """,
        unsafe_allow_html=True
    )

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_colorful_style()
    st.title("🔐 Login Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center; color: white;'>Let's Learn English with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #FFD700;'>Book 1 – Lessons 1 to 20</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

# ------------------------------
# AFTER LOGIN – MAIN APP
# ------------------------------
set_colorful_style()

st.markdown("""
<div class="main-header">
    <h1>📘 Let's Learn English with Gesner</h1>
    <p>Book 1 – 20 interactive lessons | Everyday conversations | Vocabulary | Grammar | Pronunciation | Quizzes</p>
</div>
""", unsafe_allow_html=True)

# Wrap the entire lesson content in a div with class "main-content" to apply white background
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ------------------------------
# SIDEBAR – LESSON SELECTOR & COMPANY INFO
# ------------------------------
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Select Lesson")
    lesson_number = st.selectbox("Lesson", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Your Progress")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lesson {lesson_number} of 20 completed")
    st.markdown("---")
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$1,200 USD** (full Book 1 – 20 lessons, includes source code)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All Rights Reserved")

# ------------------------------
# LESSON DATA GENERATION (20 lessons)
# ------------------------------
topics = [
    "Introducing Yourself", "Daily Routine", "At the Supermarket", "Ordering Food", "Asking for Directions",
    "Talking about Family", "At the Doctor's Office", "Job Interview", "Planning a Trip", "Weather and Seasons",
    "Shopping for Clothes", "At the Bank", "Using Public Transport", "Renting an Apartment", "Celebrating a Birthday",
    "Going to the Movies", "At the Gym", "Making a Phone Call", "Writing an Email", "Discussing Hobbies"
]

def generate_conversations(topic):
    conv1 = f"A: Hello! How are you doing today?\nB: I'm great, thanks! I'm learning about {topic}.\nA: That's wonderful. Can you tell me more?\nB: Sure! I practice every day."
    conv2 = f"A: Excuse me, could you help me with {topic}?\nB: Of course! What do you need to know?\nA: I want to improve my English.\nB: That's a great goal. Keep practicing!"
    conv3 = f"A: Hi, I'm new here. Can you explain {topic} to me?\nB: Absolutely! It's very useful for everyday life.\nA: Thank you so much!\nB: You're welcome. Let's practice together."
    return [conv1, conv2, conv3]

def generate_vocabulary(topic):
    base_words = ["hello", "goodbye", "please", "thank you", "yes", "no", "maybe", "always", "sometimes", "never",
                  "quickly", "slowly", "carefully", "happily", "sadly", "loudly", "quietly", "brightly", "darkly", "softly"]
    topic_words = [topic.lower().replace(" ", "_") + str(i) for i in range(1, 6)]
    all_words = base_words[:15] + topic_words
    return all_words[:20]

def generate_grammar_rules(topic):
    rules = [
        "1. Use present simple for facts and routines.",
        "2. Use 'to be' (am/is/are) to describe states.",
        "3. Use 'have/has' to show possession.",
        "4. Use 'can' to express ability.",
        "5. Use 'do/does' for questions in present simple.",
        "6. Use adverbs of frequency (always, sometimes, never) before the main verb.",
        "7. Use prepositions of place (in, on, at) correctly.",
        "8. Use 'there is/there are' to say something exists.",
        "9. Use 'would like' for polite requests.",
        "10. Use 'going to' for future plans."
    ]
    random.shuffle(rules)
    return rules

def generate_pronunciation_sentences(topic):
    sentences = [
        f"I am learning about {topic} today.",
        f"Could you please explain {topic} to me?",
        f"Practicing {topic} helps me improve my English.",
        f"Let's talk about {topic} together.",
        f"Understanding {topic} is very useful."
    ]
    return sentences

def generate_quiz_questions(topic, conv_texts):
    questions = [
        {"question": "What is the main topic of this lesson?", "options": [topic, "Sports", "Music", "Movies"], "answer": topic},
        {"question": "Which word means 'to say thank you'?", "options": ["Please", "Sorry", "Thank you", "Excuse me"], "answer": "Thank you"},
        {"question": "How do you ask for help politely?", "options": ["Give me help", "Help now", "Could you help me please?", "You must help"], "answer": "Could you help me please?"},
        {"question": "What does 'always' mean?", "options": ["Never", "Sometimes", "Every time", "Rarely"], "answer": "Every time"},
        {"question": "Which sentence is correct?", "options": ["He go to school", "He goes to school", "He going to school", "He gone to school"], "answer": "He goes to school"}
    ]
    return questions

@st.cache_data
def get_lesson_data(lesson_num):
    topic = topics[lesson_num - 1]
    convs = generate_conversations(topic)
    vocab = generate_vocabulary(topic)
    grammar = generate_grammar_rules(topic)
    pron_sentences = generate_pronunciation_sentences(topic)
    quiz = generate_quiz_questions(topic, convs)
    return {
        "topic": topic,
        "conversations": convs,
        "vocabulary": vocab,
        "grammar": grammar,
        "pronunciation": pron_sentences,
        "quiz": quiz
    }

# ------------------------------
# DISPLAY LESSON CONTENT
# ------------------------------
lesson_data = get_lesson_data(lesson_number)

st.markdown(f"## 📖 Lesson {lesson_number}: {lesson_data['topic']}")

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversations", "📚 Vocabulary", "📖 Grammar", "🎧 Pronunciation", "❓ Quiz"])

# Helper to generate audio from text
async def text_to_audio(text, filename):
    await edge_tts.Communicate(text, "en-US-GuyNeural").save(filename)

def play_audio(text, key):
    if st.button(f"🔊 Play Audio", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            asyncio.run(text_to_audio(text, tmp.name))
            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

# Tab 1: Conversations
with tab1:
    for i, conv in enumerate(lesson_data["conversations"], 1):
        st.markdown(f"**Conversation {i}**")
        st.text(conv)
        play_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

# Tab 2: Vocabulary
with tab2:
    cols = st.columns(4)
    for idx, word in enumerate(lesson_data["vocabulary"]):
        with cols[idx % 4]:
            st.markdown(f"**{word.capitalize()}**")
            play_audio(word, f"vocab_{lesson_number}_{idx}")

# Tab 3: Grammar
with tab3:
    for rule in lesson_data["grammar"]:
        st.markdown(f"- {rule}")

# Tab 4: Pronunciation (listen and repeat)
with tab4:
    st.markdown("Listen to each sentence, then repeat aloud.")
    for idx, sentence in enumerate(lesson_data["pronunciation"]):
        st.markdown(f"**Sentence {idx+1}:** {sentence}")
        play_audio(sentence, f"pron_{lesson_number}_{idx}")
        st.markdown("---")

# Tab 5: Quiz
with tab5:
    st.markdown("Test your understanding of this lesson.")
    if f"quiz_answers_{lesson_number}" not in st.session_state:
        st.session_state[f"quiz_answers_{lesson_number}"] = {}
    score = 0
    for q_idx, q in enumerate(lesson_data["quiz"]):
        st.markdown(f"**{q_idx+1}. {q['question']}**")
        answer = st.radio("Choose an answer:", q["options"], key=f"quiz_{lesson_number}_{q_idx}", label_visibility="hidden")
        st.session_state[f"quiz_answers_{lesson_number}"][q_idx] = answer
        if answer == q["answer"]:
            score += 1
    if st.button("Check Answers", key=f"check_{lesson_number}"):
        st.success(f"You got {score} out of {len(lesson_data['quiz'])} correct!")
        if score == len(lesson_data['quiz']):
            st.balloons()
            st.markdown("🎉 Perfect! You've mastered this lesson.")

# Close the main-content div
st.markdown('</div>', unsafe_allow_html=True)

# After lesson 20, show contact info
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Congratulations! You have completed Book 1.")
    st.markdown("""
    ### 📞 To continue with Book 2, please contact us:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Book 2 will contain more advanced conversations, vocabulary, grammar, and real‑life simulations.
    """)
