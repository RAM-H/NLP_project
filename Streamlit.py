import streamlit as st 

import spacy_transformers
import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
def TOKENIZE(Text):
    text=word_tokenize(Text)
    return(' '.join(text))
    

import spacy
from spacy import displacy
#nlp = spacy.load('en')



HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""



# Fetch Text From Url
@st.cache
def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text


#@st.cache(allow_output_mutation=True)

#@st.cache(suppress_st_warning=True)    
    
def main():
    st.title("Named Entity Checker")
    activities = ["NER Checker"]
    choice = st.sidebar.selectbox("Select Activity",activities)
    trained_nlp = spacy.load("models/output1198/model-best")
    if choice == 'NER Checker':
        st.subheader("Named Entity Recog with Spacy")
        raw_text = st.text_area("Enter Text Here","Type Here")
        if st.button("Analyze"):
            docx = trained_nlp(TOKENIZE(raw_text.lower()))
            html = displacy.render(docx,style="ent")
            html = html.replace("\n\n","\n")
            st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)


				
		


if __name__ == '__main__':
	main()
