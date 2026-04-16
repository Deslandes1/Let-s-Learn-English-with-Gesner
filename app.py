import streamlit as st
import asyncio
import tempfile
import base64
import os

# ----- Audio Setup -----
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

st.set_page_config(page_title="Let's Learn English with Gesner", layout="wide")

def set_colorful_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e); }
        .main-header { background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        .stText { color: white !important; font-size: 1rem; background: transparent !important; }
        .stTabs [role="tab"] { color: white !important; background: rgba(255,255,255,0.1); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: rgba(255,255,255,0.3); color: white !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #ff6b6b; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #feca57; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #1a0b2e, #2d1b4e); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #2d1b4e; border: 1px solid #ffcc00; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span { color: white !important; }
        div[data-baseweb="popover"] ul { background-color: #2d1b4e; border: 1px solid #ffcc00; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #2d1b4e; }
        div[data-baseweb="popover"] li:hover { background-color: #ff6b6b; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff007f"/>
                    <stop offset="50%" stop-color="#ffcc00"/>
                    <stop offset="100%" stop-color="#00ffcc"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_colorful_style()
    st.title("🔐 Access Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn English with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #FFD700;'>Book 1 – Lessons 1 to 20</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

set_colorful_style()
st.markdown("""
<div class="main-header">
    <h1>📘 Let's Learn English with Gesner</h1>
    <p>Book 1 – 20 interactive lessons | Daily conversations | Vocabulary | Grammar | Pronunciation | Quizzes</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Select a lesson")
    lesson_number = st.selectbox("Lesson", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Your progress")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lesson {lesson_number} of 20 completed")
    st.markdown("---")
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$299 USD** (full book – 20 lessons, source code included)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ----- Lesson topics (English) -----
topics = [
    "Introduce Yourself", "Daily Routine", "At the Supermarket", "Ordering Food", "Asking for Directions",
    "Talking About Family", "At the Doctor's Office", "Job Interview", "Planning a Trip", "Weather and Seasons",
    "Buying Clothes", "At the Bank", "Using Public Transport", "Renting an Apartment", "Celebrating a Birthday",
    "Going to the Cinema", "At the Gym", "Making a Phone Call", "Writing an Email", "Talking About Hobbies"
]

def generate_conversations(topic):
    conv1 = f"A: Hello! How are you today?\nB: I'm fine, thank you! I am learning about {topic}.\nA: That's wonderful. Can you tell me more?\nB: Sure! I practice every day."
    conv2 = f"A: Excuse me, could you help me with {topic}?\nB: Of course! What do you need to know?\nA: I want to improve my English.\nB: That's a great goal. Keep practicing!"
    conv3 = f"A: Hi, I'm new here. Can you explain {topic}?\nB: Absolutely! It's very useful for daily life.\nA: Thank you very much!\nB: You're welcome. Let's practice together."
    return [conv1, conv2, conv3]

def generate_vocabulary(topic):
    base_words = ["hello", "goodbye", "please", "thank you", "yes", "no", "maybe", "always", "sometimes", "never",
                  "quickly", "slowly", "carefully", "happily", "sadly", "out loud", "quietly", "brightly", "darkly", "softly"]
    topic_words = [topic.lower().replace(" ", "_") + str(i) for i in range(1, 6)]
    all_words = base_words[:15] + topic_words
    return all_words[:20]

def get_grammar_rules():
    return [
        {
            "rule": "1. Use the present simple for facts and routines.",
            "examples": [
                "I work every day.",
                "She studies English.",
                "The sun rises in the morning."
            ]
        },
        {
            "rule": "2. Use 'to be' and 'to have' correctly.",
            "examples": [
                "She is intelligent.",
                "I have a car.",
                "They are happy."
            ]
        },
        {
            "rule": "3. Use 'can' to express ability or permission.",
            "examples": [
                "I can speak English.",
                "Can I open the window?",
                "She cannot come today."
            ]
        },
        {
            "rule": "4. Use adverbs of frequency (always, sometimes, never) before the main verb.",
            "examples": [
                "I always eat breakfast at 8.",
                "Sometimes I go to the cinema.",
                "I never arrive late."
            ]
        },
        {
            "rule": "5. Use prepositions of place (in, on, under) correctly.",
            "examples": [
                "The book is on the table.",
                "The cat is under the chair.",
                "She lives in London."
            ]
        },
        {
            "rule": "6. Use 'there is / there are' to say something exists.",
            "examples": [
                "There is a restaurant nearby.",
                "There are many people here.",
                "Is there milk in the fridge?"
            ]
        },
        {
            "rule": "7. Use 'would like' for polite requests.",
            "examples": [
                "I would like a coffee, please.",
                "Would you like to visit Spain?",
                "She would like to learn more."
            ]
        },
        {
            "rule": "8. Use 'going to' for future plans.",
            "examples": [
                "I am going to travel tomorrow.",
                "They are going to eat pizza.",
                "Are you going to study tonight?"
            ]
        },
        {
            "rule": "9. Use the past simple for completed actions.",
            "examples": [
                "I visited Paris last year.",
                "She watched a movie yesterday.",
                "They played football on Sunday."
            ]
        },
        {
            "rule": "10. Use 'should' for advice.",
            "examples": [
                "You should see a doctor.",
                "We should study more.",
                "He should call his mother."
            ]
        }
    ]

def generate_pronunciation_sentences(topic):
    return [
        f"I am learning about {topic} today.",
        f"Could you explain {topic} to me, please?",
        f"Practicing {topic} helps me improve my English.",
        f"Let's talk about {topic} together.",
        f"Understanding {topic} is very useful."
    ]

def generate_quiz_questions(topic):
    return [
        {"question": "What is the main topic of this lesson?", "options": [topic, "Sports", "Music", "Movies"], "answer": topic},
        {"question": "Which word means 'give thanks'?", "options": ["Please", "Sorry", "Thank you", "Excuse me"], "answer": "Thank you"},
        {"question": "How do you politely ask for help?", "options": ["Give me help", "Help now", "Could you help me, please?", "You must help"], "answer": "Could you help me, please?"},
        {"question": "What does 'always' mean?", "options": ["Never", "Sometimes", "Every time", "Rarely"], "answer": "Every time"},
        {"question": "Which sentence is correct?", "options": ["He go to school", "He goes to school", "He going to school", "He gone to school"], "answer": "He goes to school"}
    ]

@st.cache_data
def get_lesson_data(num_lesson):
    topic = topics[num_lesson - 1]
    return {
        "topic": topic,
        "conversations": generate_conversations(topic),
        "vocabulary": generate_vocabulary(topic),
        "grammar": get_grammar_rules(),
        "pronunciation": generate_pronunciation_sentences(topic),
        "quiz": generate_quiz_questions(topic)
    }

lesson_data = get_lesson_data(lesson_number)
st.markdown(f"## 📖 Lesson {lesson_number}: {lesson_data['topic']}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversations", "📚 Vocabulary", "📖 Grammar", "🎧 Pronunciation", "❓ Quiz"])

# ----- Audio function -----
async def save_speech(text, file_path):
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    await communicate.save(file_path)

def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(text, tmp.name))
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Audio error: {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ----- TAB 1: CONVERSATIONS -----
with tab1:
    for i, conv in enumerate(lesson_data["conversations"], 1):
        st.markdown(f"**Conversation {i}**")
        st.text(conv)
        play_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

# ----- TAB 2: VOCABULARY -----
with tab2:
    cols = st.columns(4)
    for idx, word in enumerate(lesson_data["vocabulary"]):
        with cols[idx % 4]:
            st.markdown(f"**{word.capitalize()}**")
            play_audio(word, f"vocab_{lesson_number}_{idx}")

# ----- TAB 3: GRAMMAR -----
with tab3:
    st.subheader("💡 Grammar Rules (with examples and audio)")
    for idx, item in enumerate(lesson_data["grammar"]):
        st.markdown(f"**{item['rule']}**")
        play_audio(item['rule'], f"gram_rule_{lesson_number}_{idx}")
        st.markdown("**Examples:**")
        for ex_idx, ex in enumerate(item['examples']):
            col_ex, col_btn = st.columns([4, 1])
            col_ex.write(f"• {ex}")
            with col_btn:
                play_audio(ex, f"gram_ex_{lesson_number}_{idx}_{ex_idx}")
        st.markdown("---")
    
    st.markdown("---")
    st.subheader("🌟 The Basics")
    with st.expander("🔤 The English Alphabet", expanded=True):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letter in enumerate(alphabet):
            with cols[i % 7]:
                st.write(f"### {letter}")
                play_audio(letter, f"alpha_{letter}_{lesson_number}")

    with st.expander("🔢 Numbers (Cardinal & Ordinal)"):
        st.markdown("**Cardinal Numbers (1 to 10)**")
        cardinals = [
            ("1", "one"), ("2", "two"), ("3", "three"), ("4", "four"),
            ("5", "five"), ("6", "six"), ("7", "seven"), ("8", "eight"),
            ("9", "nine"), ("10", "ten")
        ]
        cols_card = st.columns(5)
        for idx, (num, word) in enumerate(cardinals):
            with cols_card[idx % 5]:
                st.write(f"**{num}** – {word}")
                play_audio(word, f"card_{num}_{lesson_number}")
        
        st.markdown("---")
        st.markdown("**Ordinal Numbers (1st to 10th)**")
        ordinals = [
            ("1st", "first"), ("2nd", "second"), ("3rd", "third"), ("4th", "fourth"),
            ("5th", "fifth"), ("6th", "sixth"), ("7th", "seventh"), ("8th", "eighth"),
            ("9th", "ninth"), ("10th", "tenth")
        ]
        cols_ord = st.columns(5)
        for idx, (num, word) in enumerate(ordinals):
            with cols_ord[idx % 5]:
                st.write(f"**{num}** – {word}")
                play_audio(word, f"ord_{num}_{lesson_number}")

    with st.expander("🗣️ Top Idiomatic Expressions"):
        idioms = [
            {"phrase": "Piece of cake", "meaning": "Something very easy to do."},
            {"phrase": "Break a leg", "meaning": "Good luck!"},
            {"phrase": "Hit the books", "meaning": "To study hard."}
        ]
        for idx, item in enumerate(idioms):
            st.markdown(f"**{item['phrase']}**")
            st.caption(item['meaning'])
            play_audio(f"{item['phrase']}. It means: {item['meaning']}", f"idiom_{idx}_{lesson_number}")
            st.markdown("---")

# ----- TAB 4: PRONUNCIATION -----
with tab4:
    st.markdown("Listen to each sentence, then repeat out loud.")
    for idx, sentence in enumerate(lesson_data["pronunciation"]):
        st.markdown(f"**Sentence {idx+1}:** {sentence}")
        play_audio(sentence, f"pron_{lesson_number}_{idx}")
        st.markdown("---")

# ----- TAB 5: QUIZ (with audio for questions, options, and correct answers) -----
with tab5:
    st.markdown("Test your understanding of this lesson.")
    
    quiz_key = f"quiz_answers_{lesson_number}"
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = {}
    
    questions = lesson_data["quiz"]
    
    for q_idx, q in enumerate(questions):
        st.markdown(f"**{q_idx+1}. {q['question']}**")
        play_audio(q['question'], f"quiz_question_{lesson_number}_{q_idx}")
        
        selected = st.session_state[quiz_key].get(q_idx, None)
        for opt_idx, opt in enumerate(q['options']):
            col_text, col_audio = st.columns([5, 1])
            with col_text:
                if st.button(opt, key=f"select_{lesson_number}_{q_idx}_{opt_idx}"):
                    st.session_state[quiz_key][q_idx] = opt
                    st.rerun()
            with col_audio:
                play_audio(opt, f"quiz_opt_{lesson_number}_{q_idx}_{opt_idx}")
            st.markdown("---")
        if selected:
            st.success(f"Selected: {selected}")
        else:
            st.info("You have not selected an answer yet. Click on an option above.")
        st.markdown("---")
    
    if st.button("Check answers", key=f"check_{lesson_number}"):
        score = 0
        for q_idx, q in enumerate(questions):
            if st.session_state[quiz_key].get(q_idx) == q["answer"]:
                score += 1
        st.success(f"You got {score} out of {len(questions)} correct!")
        if score == len(questions):
            st.balloons()
            st.markdown("🎉 Perfect! You have mastered this lesson.")
        else:
            with st.expander("Show correct answers"):
                for q_idx, q in enumerate(questions):
                    col_text, col_audio = st.columns([5, 1])
                    with col_text:
                        st.write(f"{q_idx+1}. {q['question']} → Correct answer: {q['answer']}")
                    with col_audio:
                        correct_text = f"{q['question']} Correct answer: {q['answer']}"
                        play_audio(correct_text, f"correct_ans_{lesson_number}_{q_idx}")

# ----- END OF BOOK -----
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Congratulations! You have completed Book 1.")
    st.markdown("""
    ### 📞 To continue with Book 2, contact us:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Book 2 will contain more advanced conversations, vocabulary, grammar, and real‑life simulations.
    """)
