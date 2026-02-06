import streamlit as st
from recommender import JobAIRecommender

st.set_page_config(
    page_title="PathPilot an AI based Career Recommendation System",
    page_icon="💼",
    layout="wide"
)

RESULTS_PER_LOAD = 6

@st.cache_resource
def load_ai():
    return JobAIRecommender("data")

ai = load_ai()

# ---------------- SESSION STATE ----------------
if "all_results" not in st.session_state:
    st.session_state.all_results = []

if "visible_count" not in st.session_state:
    st.session_state.visible_count = RESULTS_PER_LOAD

# ---------------- UI ----------------
st.title("💼 PathPilot an AI based Career Recommendation System")
st.markdown("### NLP-powered career recommendations using lightweight AI")

# ---------------- PART 1 ----------------
st.header("🔹 Part 1: Independent Search")

col1, col2, col3 = st.columns(3)

with col1:
    interest = st.text_input("Interest", placeholder="Technology, Healthcare")

with col2:
    skills = st.text_input("Skills", placeholder="Python, Java, SQL")

with col3:
    job_name = st.text_input("Job Name", placeholder="Software, Data Analyst")

search_clicked = st.button("🔍 Search")

query = None
if search_clicked:
    query = " ".join(filter(None, [interest, skills, job_name]))

# ---------------- PART 2 ----------------
st.header("🔹 Part 2: Smart AI Search")

smart_query = st.text_input(
    "Describe your interests, skills, or desired job",
    placeholder="I like Python, data analysis and problem solving"
)

ai_clicked = st.button("🤖 AI Recommend")

if ai_clicked:
    query = smart_query

# ---------------- SEARCH HANDLER ----------------
if query:
    st.session_state.all_results = ai.recommend(
        query, top_k=len(ai.jobs)
    )
    st.session_state.visible_count = RESULTS_PER_LOAD

# ---------------- RESULTS ----------------
if st.session_state.all_results:
    st.subheader("🎯 Recommended Careers")

    visible_results = st.session_state.all_results[
        : st.session_state.visible_count
    ]

    for job in visible_results:
        with st.container():
            st.markdown(f"## {job['name']} ({job['category']})")
            st.markdown(f"**Overview:** {job['overview']}")
            st.markdown(f"**Demand:** {job['demand']}")

            colA, colB = st.columns(2)
            with colA:
                st.markdown("### ✅ Advantages")
                for a in job["advantages"]:
                    st.write(f"- {a}")

            with colB:
                st.markdown("### ⚠️ Disadvantages")
                for d in job["disadvantages"]:
                    st.write(f"- {d}")

            st.markdown("### 🛠️ Required Skills")
            req = job["required_skills"]
            st.markdown(f"**Basic:** {', '.join(req['basic'])}")
            st.markdown(f"**Intermediate:** {', '.join(req['intermediate'])}")
            st.markdown(f"**Advanced:** {', '.join(req['advanced'])}")
            st.markdown(f"**Professional:** {', '.join(req['professional'])}")

            st.markdown(f"**Related Skills:** {', '.join(job['related_skills'])}")

            st.progress(min(job["score"], 1.0))
            st.markdown("---")

    # -------- LOAD MORE --------
    if st.session_state.visible_count < len(st.session_state.all_results):
        if st.button("⬇️ See more results"):
            st.session_state.visible_count += RESULTS_PER_LOAD
            st.rerun()

# ---------------- RESET ----------------
if st.button("🔄 Reset"):
    st.session_state.all_results = []
    st.session_state.visible_count = RESULTS_PER_LOAD
    st.rerun()


