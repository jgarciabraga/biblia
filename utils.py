import pandas as pd
import streamlit as st

import spacy
from spacy import displacy

import altair as alt
from collections import Counter

nlp = spacy.load('en')

def plot_word_frequency(docx, num=10):
    word_frequency = Counter(docx.split())
    most_common_tokens = dict(word_frequency.most_common(num))
    word_frequency_df = pd.DataFrame({'Palavra':most_common_tokens.keys(), 'Frequência':most_common_tokens.values()})
    c = alt.Chart(word_frequency_df).mark_bar().encode(x='palavra',y='freqência')
    st.altair_chart(c, use_container_width=True)
    
def render_entities(raw_text):
    docx = nlp(raw_text)
    html = displacy.render(docx, style='ent')