import streamlit as st
from traceback import TracebackException
from llm_class import ai2ai
from sound2text import MyAIAgent
import threading
import concurrent.futures
import time

st.cache_data.clear()
#GUI
#Setting up page configuration
st.set_page_config(
    page_title="AI talking to AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Setting up tabs
tab2, tab3 = st.tabs([
                    'User1 Page',
                    'User2 Page'])
# Setting up lists
topic_list=['Room booking in the hotel']
topic_list+=['Custom']

try:
    get_max_rounds=st.sidebar.number_input("Select the maximum iterations",min_value=0,key='itr')
    get_topic=st.sidebar.selectbox("Select the topic from a pre-defined list", topic_list,0)
    api_key=st.sidebar.text_input('enter api key',key='api_itr')
       
    if get_topic=='Custom':
            topic=st.sidebar.text_input(label="Enter your topic of discussion:",key='top2')

    # with tab1: #To be done by both
    #     # st.title("Select the topic of discussion")
    #     # Select number of days to analyse
    #     get_max_rounds=st.sidebar.number_input("Select the maximum iterations",min_value=0,key='itr')
    #     get_topic=st.sidebar.selectbox("Select the topic from a pre-defined list", topic_list,0)
       
    #     if get_topic=='Custom':
    #         topic=st.sidebar.text_input(label="Enter your topic of discussion:",key='top2')


    with tab2: #Go to this by user1
        
        user1=st.text_input(label="Enter name of user1 (AI assistant of user, Krishang)")
        user1_description=st.text_input(label="Enter host of user1 (Customer)")
        user2=st.text_input(label="Enter name of user2 (AI assistant of hotel)")
        user2_description=st.text_input(label="Enter host of user2 (Hotel)")

        button1=st.button('Start Conversation with User2')
        topic = st.session_state.get("topic", 'genAI')
        max_rounds = st.session_state.get("maxi",10)
        obj1=ai2ai(user1,user1_description)
        ai2ai.max_rounds=max_rounds
        ai2ai.topic=topic
        obj_1=MyAIAgent()

        ai_type1 = f"You are {user1}"
        aim1=f"Your aim is to talk to {user2} on the topic {ai2ai.topic}. Pose as {user1_description}. Start the conversation with a greeting. Keep in mind to close the conversation within {max_rounds} prompts."
        conversation_with_ai1=[]

        if button1:
            st.text('Start')
            for i in range(obj1.max_rounds):
                if i==0:
                    response_from_ai1, conversation_with_ai1 = obj1.chat_with_ai(api_key,user_command_to_ai=aim1,ai_name=ai_type1,conversation_history=conversation_with_ai1,skip_setup=False)
                else:
                    response_from_ai1, conversation_with_ai1 = obj1.chat_with_ai(api_key,user_command_to_ai=aim1,ai_name=ai_type1,conversation_history=conversation_with_ai1,skip_setup=True)

                print(f"{user2_description} : {response_from_ai1}")
                st.text(f"{user1_description} : {response_from_ai1}")

                with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(obj_1.send_message,response_from_ai1)
                #obj_1.send_message(response_from_ai1)
                #response_from_ai2=obj_1.receive_message()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(obj_1.receive_message)
                        response_from_ai2 = future.result()  # This will hold the return value

                conversation_with_ai1.append({"role": "user", "content": response_from_ai2})
            
            obj_1.p.terminate()


    with tab3: #Go to this by user2 starts first
        #user1=st.text_input(label="Enter name of user1 (AI assistant of user, Krishang)")
        #user1_description=st.text_input(label="Enter host of user1 (Customer)")
        user2=st.text_input(label="Enter name of user2 (AI assistant of hotel)",key='tab2')
        user2_description=st.text_input(label="Enter host of user2 (Hotel)",key='tab2_desc')

        button2=st.button('Start Conversation with User1')
        topic = st.session_state.get("topic", 'genAI')
        max_rounds = st.session_state.get("maxi",10)
        ai2ai.max_rounds=max_rounds
        ai2ai.topic=topic
        obj2=ai2ai(user2,user2_description)
        obj_2=MyAIAgent()


        ai_type2 = f"Your are {user2}"
        aim2=f"Your aim is to talk to the {user1} on the topic {ai2ai.topic}. Pose as {user2_description}. Start the conversation with a greeting. Keep in mind to close the conversation within {max_rounds} prompts."
        conversation_with_ai2=[]


        if button2:
                st.text('Start')
                for i in range(obj2.max_rounds):
                    st.text('Listening')
                    #response_from_ai1=threading.Thread(target=obj_1.receive_message())
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(obj_2.receive_message)
                        response_from_ai1 = future.result()  # This will hold the return value

                    conversation_with_ai2.append({"role": "user", "content": response_from_ai1}) 
                    response_from_ai2, conversation_with_ai2 = obj1.chat_with_ai(api_key,user_command_to_ai=aim2,ai_name=ai_type2,conversation_history=conversation_with_ai2,skip_setup=False)
                    print(f"{user2_description} : {response_from_ai2}")
                    st.text(f"{user2_description} : {response_from_ai2}")
                    
                    time.sleep(10)
                    #obj_2.send_message(response_from_ai2)
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(obj_2.send_message,response_from_ai2)
                    st.text('Sending')
                
                obj_2.p.terminate()


except Exception as e:
    st.text(e)
    print(e)
