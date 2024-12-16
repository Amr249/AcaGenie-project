import streamlit as st 

# Custom CSS
custom_css = """
<style>

    #custom-div {
    background-color: lightblue;
    padding: 20px;
    border: 2px solid blue;
    border-radius: 10px;
}

    h2{
    color: #FFFAF0;
}

    #Home-image{
    border-radius: 25px;
}

</style>
"""

# Apply CSS

st.header("AcaGenie – Your academic assistant powered by AI.")

st.write("Unlock the power of AI to simplify, enhance, and revolutionize your academic and research experience. Designed with students, professors, and researchers in mind, our suite of tools helps you save time, streamline your work, and focus on what truly matters—learning, teaching, and discovery.")

st.header("What We Offer")

st.markdown('<div id="custom-div">This is a styled div</div>', unsafe_allow_html=True)



st.write("""
1. Chat With PDF

Transform static documents into interactive conversations. Upload your PDFs, ask questions, and let our AI extract insights, clarify concepts, and provide instant answers.

2. Custom Summarization App

Cut through the clutter with tailored summaries. Whether it’s an academic paper, textbook chapter, or lecture notes, our app provides concise, accurate summaries that focus on what matters most to you.

3. Paper to Audiobook

Listen to research papers and study materials on the go! Convert your documents into high-quality audiobooks with natural-sounding voices, making it easier than ever to absorb knowledge while multitasking.

4. Text to Presentation

Turn your written content into visually engaging presentations in minutes. Perfect for professors preparing lectures, students creating class projects, or researchers showcasing their findings.

""")

st.header("Why Choose Us?")

st.write("""
AI-Powered Efficiency: Harness the latest advancements in AI to simplify complex academic tasks.
         
Designed for Academics: Tools tailored to meet the unique needs of the academic community.
         
Save Time, Work Smarter: Focus on learning and innovation while we handle the heavy lifting.
         
Accessible Anywhere: Use our tools anytime, anywhere, whether you're at your desk or on the move.
""")

st.header("Transform the Way You Work and Learn")

st.write("""

Our app is more than a tool—it’s your academic partner. Whether you're a student striving for better grades, a professor managing multiple classes, or a researcher exploring groundbreaking ideas, we’re here to empower you every step of the way.
""")