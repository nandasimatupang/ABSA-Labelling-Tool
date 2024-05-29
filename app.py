import streamlit as st
import pandas as pd

# Upload data
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file")
    st.stop()

# Ensure the necessary column exists
if 'ulasan' not in df.columns:
    st.error("The 'ulasan' column is not present in the CSV file")
    st.stop()

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = 0

if 'annotations' not in st.session_state:
    st.session_state.annotations = {'sentiment': [''] * len(df), 'aspect': [''] * len(df)}

if 'edited_ulasan' not in st.session_state:
    st.session_state.edited_ulasan = df['ulasan'].tolist()

def annotate_aspect(annotation):
    st.session_state.annotations['aspect'][st.session_state.index] = annotation
    check_and_move_to_next()

def annotate_sentiment(annotation):
    st.session_state.annotations['sentiment'][st.session_state.index] = annotation
    check_and_move_to_next()

def check_and_move_to_next():
    if all(st.session_state.annotations[key][st.session_state.index] for key in st.session_state.annotations):
        st.session_state.index += 1
        if st.session_state.index >= len(df):
            st.session_state.index = 0
        st.experimental_rerun()

# Styling for buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #f0f2f6; 
    color: #262730; 
    width: 100%; 
    padding: 10px 0; 
}
div.stButton > button:first-child:focus {
    background-color: #007bff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Display current text and buttons in the same row
st.write(f"Review {st.session_state.index + 1}/{len(df)}")
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown(
        f"""
        <div style='background-color: white; color: black; padding: 10px; border: 1px solid #ddd; border-radius: 5px; height: 200px; overflow-y: auto;'>
            {df["ulasan"].iloc[st.session_state.index]}
        </div>
        """,
        unsafe_allow_html=True,
)

with col2:
    # Add buttons for aspect annotation
    st.subheader("Aspect")
    for option in ('Facilities', 'Access', 'Cleanliness', 'Scenery', 'Price'):
        if st.button(option, key=f"aspect_{option}"):
            annotate_aspect(option)

with col3:
    # Add buttons for sentiment annotation
    st.subheader("Sentiment")
    if st.button('Positive', key="sentiment_Positive"):
        annotate_sentiment('Positive')
    if st.button('Negative', key="sentiment_Negative"):
        annotate_sentiment('Negative')

# Save annotations and edited ulasan to a new CSV file and provide download button
if st.button("Save Annotations"):
    df['ulasan'] = st.session_state.edited_ulasan
    df['sentiment'] = st.session_state.annotations['sentiment']
    df['aspect'] = st.session_state.annotations['aspect']
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Annotated Data",
        data=csv,
        file_name='annotated_pantai.csv',
        mime='text/csv',
    )

# Display remaining entries
st.write(f"Remaining reviews: {len(df) - st.session_state.index}")
