import streamlit as st
import itertools
from nltk.corpus import words, wordnet
import nltk

# Download necessary NLTK corpora
nltk.download('words')
nltk.download('wordnet')

english_words = set(words.words())

st.set_page_config(page_title="Word Builder with Meanings", layout="centered")
st.title("📚 Solving Word Puzzle Using Word Generator with Dictionary Meanings")
st.write("Enter a few letters, and I'll show you all valid English words with their meanings!")

# User input
letters_input = st.text_input("Enter letters (e.g., stream):", max_chars=10)
show_definitions = st.checkbox("Show definitions for each word", value=True)

# Word generator function with WordNet check
def generate_words_with_meanings(letters):
    letters = letters.lower()
    results = {}

    for r in range(2, len(letters)+1):  # Generate 2-letter up to full-length words
        for perm in itertools.permutations(letters, r):
            word = ''.join(perm)
            if word in english_words and wordnet.synsets(word):  # Only keep real, defined words
                definition = wordnet.synsets(word)[0].definition()
                results[word] = definition
    return dict(sorted(results.items(), key=lambda x: (len(x[0]), x[0])))

# Display results
if letters_input and len(letters_input) >= 2:
    st.info(f"Building meaningful words from: **{letters_input.upper()}**")
    with st.spinner("Searching dictionary..."):
        word_defs = generate_words_with_meanings(letters_input)

    wordList = []

    if word_defs:
        st.success(f"Found {len(word_defs)} meaningful word(s):")
        for word, definition in word_defs.items():
            wordList.append(word)
            if show_definitions:
                st.markdown(f"- **{word}**: {definition}")

        st.markdown("---")
        st.markdown(f"**Generated Words:** {', '.join(wordList)}")
    else:
        st.warning("😕 No valid dictionary words found. Try more or different letters.")

st.markdown("---")
st.caption("Built with NLTK's WordNet & Streamlit.")
