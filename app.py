# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc

import pandas as pd
import neattext.functions as nfx
import datetime
import random

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import altair as alt

from utils import plot_word_frequency

@st.cache
def load_biblia(data):
    df = pd.read_csv(data)
    today = datetime.datetime.today().date().strftime('%d-%m')
    return df, today

def main():
    st.title("Sagrada Escritura")
    menu = ["Home", "Múltiplos Versículos", "Sobre"]
    df, today = load_biblia("data/BBE.csv")
    
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Busca de Versículo")
        #st.dataframe(df)
        book_list = df['b'].unique().tolist()
        book_name = st.sidebar.selectbox("Livro", book_list)
        chapter = st.sidebar.number_input("Capítulo", 1)
        verse = st.sidebar.number_input("Verse", 1)
        bible_df = df[df['b'] == book_name]
        #st.dataframe(bible_df)
        #layout
        c1, c2 = st.beta_columns([2,1])
        #Single Verse Layout
        with c1:
            try:
                selected_passage = bible_df[(bible_df['c'] == chapter) & (bible_df['v'] == verse)]
                #st.write(selected_passage)
                passge_details = "Livro {}. Capítulo {}. Versículo {}".format(book_name, chapter, verse)
                st.info(passge_details)
                passage = "{}".format(selected_passage['t'].values[0])
                st.write(passage)
            except Exception as e:
                st.warning('Livro ou Capítulo inexistente')
        with c2:
            st.success('Versículo do Dia {}'.format(today))
            chapter_list = range(10)
            verse_list = range(20)
            ch_choice = random.choice(chapter_list)
            vs_choice = random.choice(verse_list)
            random_book_name = random.choice(book_list)
            st.write("Livro {}. Capítulo {}. Versículo {}".format(random_book_name, ch_choice, vs_choice))
            rand_bible_df = df[df['b'] == random_book_name]
            try:
                randomly_selected_passage = rand_bible_df[(rand_bible_df['c']==ch_choice) & (rand_bible_df['v'] == vs_choice)]
                mytext = randomly_selected_passage['t'].values[0]
            except Exception as e:
                randomly_selected_passage = rand_bible_df[(rand_bible_df['c']==1) & (rand_bible_df['v'] == 1)]
                mytext = randomly_selected_passage['t'].values[0]
            st.write(mytext)

        search_term = st.text_input('Busca')
        with st.beta_expander('Resultado'):
            resultado_df = df[df['t'].str.contains(search_term)]
            resultado_df = resultado_df.reset_index()
            st.dataframe(resultado_df[['b','c','v','t']])



    
    elif  choice == "Múltiplos Versículos":
        st.subheader("Busca de Versículos (Vários)")
        book_list = df['b'].unique().tolist()
        book_name = st.sidebar.selectbox("Livro", book_list)
        chapter = st.sidebar.number_input('Capítutlo', 1)
        bible_df = df[df['b'] == book_name]
        chapter_df = bible_df[bible_df['c'] == chapter]
        all_verse = chapter_df['v'].unique().tolist()
        verse = st.sidebar.multiselect('Versículo', all_verse, default=1)
        passge_details = "Livro {}. Capítulo {}. Versículo {}".format(book_name, chapter, verse)
        st.info(passge_details)
        #st.dataframe(selected_passage)

        col1, col2 = st.beta_columns(2)

        with col1:
            st.info('Versículos')
            for index, row in chapter_df.iterrows():
                if row['v'] in verse:
                    st.write(row['t'])
        with col2:
            st.success('Estudos')
 
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()


