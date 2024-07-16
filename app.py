import streamlit as st
from openai import OpenAI
from streamlit.components.v1 import html

client = OpenAI(api_key=st.secrets['token'], base_url="https://api.groq.com/openai/v1")

def generate_content(system, prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

st.title("AI-Powered Blog Generator")

st.write("Enter a topic or keywords to generate a blog outline:")
user_input = st.text_input("Topic", "")

system_topic = """You are an expert content creator specializing in generating engaging blog topics and detailed outlines. 
Your task is to create a compelling blog topic and a comprehensive outline based on the given keywords and user-provided details. 
Strict Note: Don't mention any other text rather than blog details, just provide the context
Not include this kind of text that are in single quotes 'Here is a compelling blog topic and a comprehensive outline based on the given keywords:'
Just provide the title and outline the sections and keywords for the sections as please follow the structure and format of below example:

### Revolutionizing Healthcare: The Transformative Power of AI

#### Unlocking the Potential of AI in Medical Diagnosis and Treatment
AI in healthcare, AI-powered medical diagnosis, predictive analytics in healthcare, AI-assisted treatment planning

#### Enhancing Patient Outcomes with AI-Driven Precision Medicine
personalized healthcare, AI-powered drug discovery, genetic analysis and AI, AI in clinical decision support

#### Streamlining Healthcare Operations with AI-Enabled Automation
AI in healthcare administration, AI-powered workflow optimization, AI-driven patient scheduling, AI in medical billing and coding

#### Improving Patient Engagement and Experience with AI-Powered Chatbots
AI-powered virtual assistants, AI-driven patient communication, AI-enabled symptom triage, AI in telemedicine

#### Revolutionizing Medical Research with AI-Accelerated Discoveries
AI in clinical trials, AI in drug development, AI-powered biomedical research, AI in medical imaging analysis

#### Conclusion: Embracing the AI Revolution for a Healthier Future
the future of AI in healthcare, benefits of AI in healthcare, AI-driven healthcare transformation, why healthcare organizations should adopt AI
"""

def blog_topic_generator(user_input, system_topic, user_topic):
    return generate_content(system_topic, user_topic)

system_full = """
You will get the blog topic, outlines, tone, length, audience. Generate the full blog post based on these things. 
Does not write any other text than blog, just write the blog post with also mention that add image here with add image tag from your side.
Blog should be SEO Optimized and SEO Friendly.
"""

if 'outline' not in st.session_state:
    st.session_state.outline = None

if 'full_blog' not in st.session_state:
    st.session_state.full_blog = None

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Outline"):
        if user_input:
            with st.spinner("Generating outline..."):
                user_topic = f"Here is the topic: {user_input}"
                st.session_state.outline = generate_content(system_topic, user_topic)
        else:
            st.warning("Please enter a topic.")

with col2:
    if st.session_state.outline and st.button("Regenerate Outline"):
        with st.spinner("Regenerating outline..."):
            user_topic = f"Here is the topic: {user_input}"
            st.session_state.outline = generate_content(system_topic, user_topic)

if st.session_state.outline:
    st.subheader("Blog Outline")
    st.markdown(st.session_state.outline)

    st.subheader("Blog Options")
    tone_options = ["Informative", "Casual", "Professional", "Humorous", "Serious"]
    length_options = ["Short (500 words)", "Medium (1000 words)", "Long (1500+ words)"]
    audience_options = ["General", "Beginners", "Experts", "Students", "Professionals"]

    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox("Select tone:", tone_options, index=0)
    with col2:
        length = st.selectbox("Select length:", length_options, index=1)
    with col3:
        audience = st.selectbox("Select audience:", audience_options, index=0)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Full Blog"):
            with st.spinner("Generating full blog post..."):
                user_full = f"Blog Outline: {st.session_state.outline}\nTone: {tone}\nLength: {length}\nAudience: {audience}"
                st.session_state.full_blog = generate_content(system_full, user_full)

    with col2:
        if st.session_state.full_blog and st.button("Regenerate Full Blog"):
            with st.spinner("Regenerating full blog post..."):
                user_full = f"Blog Outline: {st.session_state.outline}\nTone: {tone}\nLength: {length}\nAudience: {audience}"
                st.session_state.full_blog = generate_content(system_full, user_full)

if st.session_state.full_blog:
    st.subheader("Full Blog Post")
    
    # Display the blog content
    st.markdown(st.session_state.full_blog)

st.sidebar.header("About")
st.sidebar.info("This app uses AI to generate blog topics, outlines, and full blog posts based on your input.")

st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Enter a topic or keywords in the input field.
2. Click the "Generate Outline" button.
3. Review the generated outline. Use "Regenerate Outline" if needed.
4. Select the desired tone, length, and audience.
5. Click "Generate Full Blog" to create the complete blog post.
6. Use "Regenerate Full Blog" if you want a different version.
""")
