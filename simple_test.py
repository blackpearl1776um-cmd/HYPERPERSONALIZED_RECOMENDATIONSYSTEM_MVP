import streamlit as st

st.title("🌱 TEST - Sustainable Shopping Assistant")
st.write("If you see this, everything is working!")
st.success("🎉 SUCCESS! All dependencies are installed!")

# Test basic functionality
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello {name}! The app is working perfectly!")