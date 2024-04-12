import streamlit as st
import re
import openai
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from googletrans import Translator
from langchain.callbacks import get_openai_callback

# 영어 번역
def google_trans(messages):
    google = Translator()
    result = google.translate(messages, dest="ko")

    return result.text

# Youtube URL 체크
def youtube_url_check(url):
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)(\&ab_channel=[\w\d]+)?$'
    match = re.match(pattern, url)
    return match is not None


# 메인 함수
def main():

    st.set_page_config(page_title="YouTube Summerize", layout="wide")
    st.header(" 📹영어 YouTube 내용 요약/대본 번역기")
    st.markdown('---')
    #URL 입력받기
    st.subheader("YouTube URL을 입력하세요")
    youtube_video_url = st.text_input("  ",placeholder="https://www.youtube.com/watch?v=**********")

    with st.sidebar:
        # Open AI API 키 입력받기
        open_apikey = st.text_input(label='OPENAI API 키', placeholder='Enter Your API Key', value='',type='password')
        
        if open_apikey:
            st.session_state["OPENAI_API"] = open_apikey 
        st.markdown('---')
        
        options = ['gpt-3.5-turbo-0125', 'gpt-4', 'gpt-4-turbo-2024-04-09']
        model_name = st.selectbox('모델을 선택하세요', options)
        
        tok_bill = st.checkbox("입출력 토큰수 & 비용 확인")
        
    if st.button("스크립트 요약"):
        if not youtube_url_check(youtube_video_url):
            st.error("YouTube URL을 확인하세요.")
        else:
            switch_on = True
            width = 50
            side = width/2
            _, container, _ = st.columns([side, width, side])
            # 입력받은 유튜브 영상 보여주기
            container.video(data=youtube_video_url)
            
            # 대본 추출하기
            loader = YoutubeLoader.from_youtube_url(youtube_video_url)
            transcript = loader.load()
        
            st.subheader("요약 결과")
            

            with get_openai_callback() as cb:
                # LLM 모델 설정
                llm = ChatOpenAI(temperature=0,
                        openai_api_key=st.session_state["OPENAI_API"],
                        max_tokens=3000,
                        model_name=model_name,
                        request_timeout=120
                    )
                
                # 요약 프롬프트 설정
                prompt = PromptTemplate(
                    template="""Summarize the youtube video whose transcript is provided within backticks \
                    ```{text}```
                    """, input_variables=["text"]
                )
                combine_prompt = PromptTemplate(
                    template="""Combine all the youtube video transcripts  provided within backticks \
                    ```{text}```
                    Provide a concise summary between 8 to 10 sentences.
                    """, input_variables=["text"]
                )

                # 대본 쪼개기
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
                text = text_splitter.split_documents(transcript)

                #요약 실행
                chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False,
                                            map_prompt=prompt, combine_prompt=combine_prompt)
                summerzie_txt = chain.run(text)
                bill = f"""
                        입력 토큰 수: {cb.prompt_tokens}<br>
                        출력 토큰 수: {cb.completion_tokens}<br>
                        사용된 금액: {cb.total_cost*1363.80:0.2f} 원
                        """
            st.success(summerzie_txt)
            #번역하기   
            transe = google_trans(summerzie_txt)
            st.subheader("요약 번역 결과")
            st.info(transe)
            
            if tok_bill:
                st.markdown(bill, unsafe_allow_html=True)
if __name__=="__main__":
    main()
