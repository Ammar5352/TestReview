import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


os.environ["GROQ_API_KEY"] = st.secrets["general"]["GROQ_API_KEY"]

os.environ['LANGCHAIN_API_KEY'] = st.secrets["general"]["LANGCHAIN_API_KEY"]
os.environ['LANGCHAIN_TRACING_V2'] = 'true'

criteria = st.selectbox("Select Option",options=['Using URL',"Using Manual Text"])


def review_chatbot(criteria):
    llm = ChatGroq(model="Gemma2-9b-It")
    output_parser = StrOutputParser()
    if criteria=="Using Manual Text":
        user_prompt = st.text_input("Enter Review")
        if user_prompt:
            prompt_template = ChatPromptTemplate.from_messages(
                [
                    ('system',"You are hotel ai agent. You have to read text data and you have to extract keywords which describe how hotel is like for Eg Hotel is awesome so awesome is keyword which generate positive note similar ,negative ,moderate as per your knowldege you have to provide answers.Extract only 5 Keywords eg like breakfast was awesome so here what is awesome here breakfast so it should be like Breakfast-->positive also negative also and neutral also. In last provide 1 line summary for hotel review whether it is good or not"),
                    ('user',"Question:{user_prompt}")
                ]
            )
            
            chain = prompt_template|llm|output_parser
            answer = chain.invoke({'user_prompt':user_prompt})
            st.success(answer)
            new = answer.split("\n*")
            new_res = new[1:len(new)-1]
            result_dict = {}

            for entry in new_res:
                entry = entry.strip()
                key, value = entry.split(':', 1)
                key = key.replace('*','').strip()
                value = value.replace('*','').strip()
                value = value.strip()
                result_dict[key] = value
            import pandas as pd
            df  = pd.DataFrame(list(result_dict.items()),columns=['Keywords','Sentiment'])
            def highlight_color(row):
                if row['Sentiment'][:9].strip().lower() == 'positive':
                    return ['background-color: #77dd77;color:black;font-weight:bold'] * len(row)  # Green for Positive
                elif row['Sentiment'][:8].strip().lower() in ['neutral','moderate']:
                    return ['background-color: #FBDB65;color:black;font-weight:bold'] * len(row)  # Red for Negative
                elif row['Sentiment'][:5].strip().lower() in ['mixed']:
                    return ['background-color: #FBDB65;color:black;font-weight:bold'] * len(row)  # Red for Negative
                elif row['Sentiment'][:9].strip().lower() == 'negative':
                    return ['background-color: #FF7276;color:black;font-weight:bold'] * len(row)  # Red for Negative
                
                else:
                    return [''] * len(row) 
            
            
            
        
            st.write(df.style.apply(highlight_color,axis=1))

    else:
        no_of_reviews = st.selectbox("Select How many review you want to analyze",options=[1,2,3,4,5,6,7,8,9,10])
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
        }
        url = st.text_input("Provide URL of TripAdvisor")
        prompt_template_heading = ChatPromptTemplate.from_messages(
                    [
                        ('system',"You are hotel ai agent. You have to read text data and you have to extract hotel name from URL. I will provide you URL.Only Return Hotel Name"),
                        ('user',"Question:{url}")
                    ]
                    )
        chain_header = prompt_template_heading|llm|output_parser
        response_header = chain_header.invoke({'url':url})
        col1,col2,col4,col3,col5 = st.columns([1,1,3,1,1])
        with col4:
            st.markdown(f"""<h2>{response_header}</h2>""",unsafe_allow_html=True)
        if url:
            response = requests.get(url = url,headers=headers).content
            soup = BeautifulSoup(response,'html.parser')
            print("/*/*/*/*/",soup)
            reviews = soup.find_all('span',{'class':'orRIx Ci _a C'})
            month_date = soup.find_all('span',{'class':'iSNGb _R Me S4 H3 Cj'})
            new_list= []
            date_list=[]
            for review in reviews:
                new_list.append(review.text)
            print(new_list)
            for i in range(no_of_reviews):
                print(i)
                try:
                    prompt_template = ChatPromptTemplate.from_messages(
                        [
                            ('system',"You are hotel ai agent. You have to read text data and you have to extract keywords which describe how hotel is like for Eg Hotel is awesome so awesome is keyword which generate positive note similar ,negative ,moderate as per your knowldege you have to provide answers.Extract only 5 Keywords eg like breakfast was awesome so here what is awesome here breakfast so it should be like Breakfast-->positive also negative also and neutral also. In last provide 1 line summary for hotel review whether it is good or not"),
                            ('user',f"Question:{new_list[i]}")
                        ]
                    )
                    
                    chain = prompt_template|llm|output_parser
                    answer = chain.invoke({'user_prompt':new_list[i]})
                    st.success(answer)
                    new = answer.split("\n*")
                    new_res = new[1:len(new)-1]
                    result_dict = {}

                    for entry in new_res:
                        entry = entry.strip()
                        key, value = entry.split(':', 1)
                        key = key.replace('*','').strip()
                        value = value.replace('*','').strip()
                        value = value.strip()
                        result_dict[key] = value
                    import pandas as pd
                    df  = pd.DataFrame(list(result_dict.items()),columns=['Keywords','Sentiment'])
                    def highlight_color(row):
                        if row['Sentiment'][:9].strip().lower() == 'positive':
                            return ['background-color: #77dd77;color:black;font-weight:bold'] * len(row)  # Green for Positive
                        elif row['Sentiment'][:8].strip().lower() in ['neutral','moderate']:
                            return ['background-color: #FBDB65;color:black;font-weight:bold'] * len(row)  # Red for Negative
                        elif row['Sentiment'][:5].strip().lower() in ['mixed']:
                            return ['background-color: #FBDB65;color:black;font-weight:bold'] * len(row)  # Red for Negative
                        elif row['Sentiment'][:9].strip().lower() == 'negative':
                            return ['background-color: #FF7276;color:black;font-weight:bold'] * len(row)  # Red for Negative
                        
                        else:
                            return [''] * len(row) 
                    st.write(df.style.apply(highlight_color,axis=1))
                    
                
                except:
                    st.error("Due to Website Cache Security unable to scrap data!.")
    
        
review_chatbot(criteria)