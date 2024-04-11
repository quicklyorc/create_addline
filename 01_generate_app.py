# 1. 라이브러리 임포트
import streamlit as st
import openai


# 2. 기능 구현 함수
def askGPT(prompt):
    messages_prompt = [{"role": "system", "content":prompt}]
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0125", messages = messages_prompt
    )
    gptResponse = response["choices"][0]["message"]["content"]
    return gptResponse

# 3. 메인 함수
def main():
    st.set_page_config(page_title="광고 문구 생성 프로그램")
    # 사이드 바
    with st.sidebar:
        open_apikey = st.text_input(label='OPENAI API 키:', 
                                    placeholder='sk-......', 
                                    value='',type='password')
        if open_apikey:
            openai.api_key = open_apikey
        st.markdown("----------")
        
    #메인
    #메인공간
    st.header("광고 문구 생성 프로그램")
    st.markdown('---')
    col1, col2 =  st.columns(2)
    with col1:
        name = st.text_input("제품명",placeholder=" ")
        strenghth = st.text_input("제품 특징",placeholder=" ")
        keyword = st.text_input("필수 포함 키워드",placeholder=" ")
    with col2:
        com_name = st.text_input("브랜드 명",placeholder="Apple, 올리브영..")
        tone_manner = st.text_input("톤엔 메너",placeholder="발랄하게, 유머러스하게, 감성적으로..")
        value = st.text_input("브랜드 핵심 가치",placeholder="필요 시 입력")
    if st.button("광고 문구 생성"):
        prompt = f'''
        아래 내용을 참고해서 1~2줄짜리 광구문구 5개 작성해줘
        - 제품명: {name}
        - 브렌드 명: {com_name}
        - 브렌드 핵심 가치: {value}
        - 제품 특징: {strenghth}
        - 톤엔 매너: {tone_manner}
        - 필수 포함 키워드: {keyword}
        '''
        st.info(askGPT(prompt))
if __name__=='__main__':
    main()