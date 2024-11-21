# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 15:46:14 2024

@author: f08472
"""

import streamlit as st
import PyPDF2
import re

# Interface Streamlit
st.title("Comparateur de FDP RDS")

st.write("""
Cette application vous permet de comparer deux FDP du RDS et de mettre en évidence leurs différences au niveau des additifs.
Téléchargez simplement vos fichiers ci-dessous.
""")

# Téléchargement des fichiers PDF
file1 = st.file_uploader("Téléchargez le premier fichier PDF", type=["pdf"])
file2 = st.file_uploader("Téléchargez le deuxième fichier PDF", type=["pdf"])

if file1 and file2:
    pdf_file1 = file1
    # Lire le fichier PDF
    pdf_reader1 = PyPDF2.PdfReader(pdf_file1)
    num_page = 1
    liste_additif1 = []

    expression = "^[0-9]{5}"
    pattern = re.compile(expression, re.IGNORECASE)

    for page in pdf_reader1.pages :
        # Extraire le texte de la première page
        additif_page = page.extract_text().split("\n")
        for additif in additif_page:
            if additif:
                if pattern.search(additif):
                    liste_additif1.append(pattern.search(additif).group(0))
        
    # print(liste_additif1)
    # print(len(liste_additif1))
    # print('----------------------------------')

    # Ouvrir le fichier PDF
    pdf_file2 = file2
    # Lire le fichier PDF
    pdf_reader2 = PyPDF2.PdfReader(pdf_file2)
    num_page = 1
    liste_additif2 = []

    for page in pdf_reader2.pages :
        # Extraire le texte de la première page
        additif_page = page.extract_text().split("\n")
        for additif in additif_page:
            if additif:
                if pattern.search(additif):
                    liste_additif2.append(pattern.search(additif).group(0))
        
    #print(liste_additif2)
    #print(len(liste_additif2))

    additifs_manquants1 = []
    for additif1 in liste_additif1:
        flag_trouve = 0
        for additif2 in liste_additif2:
            if additif1 == additif2:
                flag_trouve = 1
                break
        
        if flag_trouve == 0 :
            additifs_manquants1.append(additif1)

    #nom_fichier1 = file1.split("\\")[-1]
    #nom_fichier2 = file2.split("\\")[-1]

    # print(f"Additifs de {nom_fichier1} non présents dans {nom_fichier2}")
    # print(additifs_manquants1)

    additifs_manquants2 = []
    for additif2 in liste_additif2:
        flag_trouve = 0
        for additif1 in liste_additif1:
            if additif2 == additif1:
                flag_trouve = 1
                break
        
        if flag_trouve == 0 :
            additifs_manquants2.append(additif2)
    st.write("Additifs du 1er PDF non présents dans le second :")        
    st.write(additifs_manquants1)
    st.write("Additifs du second PDF non présents dans le 1er :")
    st.write(additifs_manquants2)