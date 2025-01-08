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
os.environ['HF_TOKEN'] = st.secrets["general"]["HF_TOKEN"]
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
            response = chain.invoke({'user_prompt':user_prompt})
            st.success(response)
    
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
        if url:
            response = requests.get(url = url,headers=headers).content
            soup = BeautifulSoup(response,'lxml')
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
                    response = chain.invoke({'user_prompt':new_list[i]})
                    st.success(response)
                except:
                    st.error("Due to Website Cache Security unable to scrap data!.")
            # for date1 in month_date:
            #     date_list.append(date1.text)
            # new_date_list=[]
            # for date_stay in date_list:
            #     new_date_list.append(date_stay.split(':')[1].strip())
        #user_prompt = "Nicely cleaned room by housekeeping staff sujata and sanju.. Would recommend business travellers to stay in this hotel as very near to the railway station. Usually other hotels in the vicinity are not clean and cossy as compared to this one in Surat."
    # user_prompt = "Staying at Ginger was a nice experience Staff Sujata,phoolmani, vishnu and kalawati was very supportive and their service in restaurant was superb with their polite and customer centric behaviour. Whatever was asked by me was made available at the restaurant. Staff behaviour was the best."
            # llm = ChatGroq(model="Gemma2-9b-It")
            # output_parser = StrOutputParser()
        
review_chatbot(criteria)