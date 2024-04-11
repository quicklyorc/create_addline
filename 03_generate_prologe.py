# 1. 라이브러리 임포트
import streamlit as st
import openai

# 2. 기능 구현 함수
def askGPT(model_name, prompt):
    messages_prompt = [{"role": "system", "content":prompt}]
    response = openai.ChatCompletion.create(
        model = model_name, messages = messages_prompt
    )
    gptResponse = response["choices"][0]["message"]["content"]
    input_tok = response['usage']["prompt_tokens"]
    output_tok = response['usage']["completion_tokens"]
    total_bill = response['usage']["prompt_tokens"] * 0.0005/1000 + response['usage']["completion_tokens"] * 0.0015/1000
    return total_bill, input_tok, output_tok, gptResponse
    

# 3. 메인 함수
def main():
    st.set_page_config(page_title="소설 프롤로그 작성 프로그램")
    # 사이드 바
    with st.sidebar:
        open_apikey = st.text_input(label='OPENAI API 키:', 
                                    placeholder='sk-......', 
                                    value='',type='password')
        if open_apikey:
            openai.api_key = open_apikey
        st.markdown("---")
        
    #메인
    #메인공간
    st.header("소설 프롤로그 작성 프로그램")
    st.markdown('---')
    col1, col2 =  st.columns(2)
    options = ['gpt-3.5-turbo-0125', 'gpt-4', 'gpt-4-turbo-2024-04-09']
    model_name = st.selectbox('모델을 선택하세요', options)
    with col1:
        genre = st.text_input("소설의 장르",placeholder=" ")
        sex = st.text_input("주인공의 성별",placeholder=" ")
    with col2:
        era = st.text_input("소설의 시대적 배경",placeholder=" ")
        job = st.text_input("주인공의 직업",placeholder=" ")
    if st.button("프롤로그 생성"):
        prompt = f'''
        Your *role*
        You are the most accomplished writer in Korea.
        Your task is to write a compelling prologue to a novel based on the information given.
        - Start by writing the name of your novel at the beginning of your prologue.
        Ex) Lord of the Rings
        Once upon a time......
        
        - Write natural sentences using grammar and vocabulary that an audience in 2020s South Korea would understand.
        - Refer to the prologues of famous Korean novels for an incredibly engaging narrative.
        - Use detailed and vivid descriptions.
        - *Write a maximum of two paragraphs!
        - ***The prologue must be written in Korean!!!***
        ***Don't forget your role!***
        
        *Information about the novel*
        - Genre of the novel:{genre}
        - The time period of the novel:{era}
        - Main character's gender:{sex}
        - Occupation of the main character:{job}
        '''
        bill, input_tok, output_tok, res = askGPT(model_name, prompt)
        st.info(res)
        paycheck = f"""
                    입력 토큰 수: {input_tok}<br>
                    출력 토큰 수: {output_tok}<br>
                    당신의 1 딸깍으로 나간 돈: {bill*1363.80:0.2f} 원
                    """
        st.markdown(paycheck, unsafe_allow_html=True)
        
if __name__=='__main__':
    main()