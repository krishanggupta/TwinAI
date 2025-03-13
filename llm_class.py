from openai import AzureOpenAI

#pip install openai not conda install openai

class ai2ai:
    topic=''
    max_rounds=''

    def __init__(self,user,user_description):
        self.user=user
        self.user_description=user_description
            
    def chat_with_ai(self,user_command_to_ai, ai_name='you are a hotel booking assistant',conversation_history=[],my_model='gpt-4o-mini',skip_setup=''):
        client = AzureOpenAI(
            api_version="2024-10-21",
            azure_endpoint='https://imagegenerator.openai.azure.com/',
            api_key="3de3eb8252114e1d8ee8aecf893e8187"
        )

        if user_command_to_ai.lower() in ['thank','thanks','done','bye','stop','thank you']:
            conversation_history = []  # Clear memory
            return "Conversation reset. How can I assist you next?",1
        
        
        
        # Configure the assistant only when the first iteration is there
        if skip_setup==False:
            # Append new user input to history
            conversation_history.append({"role": "user", "content": user_command_to_ai}) # Represents the input from the user..

            # Create the prompt with past conversation
            messages = [{"role": "system", "content": f'{ai_name}'}] # defines behaviour and guidelines for the assistant
            messages.extend(conversation_history)

        elif skip_setup==True:
            messages=conversation_history
            
        # Call OpenAI API
        response = client.chat.completions.create(
            model=my_model,
            messages=messages
        )
        # Extract response
        bot_reply = response.choices[0].message.content

        # Add assistant's response to history
        conversation_history.append({"role": "assistant", "content": bot_reply}) # Stores the assistant's responses.

        return bot_reply,conversation_history

    def ai_to_ai_convo(self,myobj):  

        user1=self.user
        user2=myobj.user
    
        user1_description = self.user_description
        user2_description = myobj.user_description
        
        max_rounds=self.max_rounds
        ai_type1 = f"You are {user1}"
        aim1=f"Your aim is to talk to {user2} on the topic {ai2ai.topic}. Pose as {user1_description}. Start the conversation with a greeting. Keep in mind to close the conversation within {max_rounds} prompts."

        ai_type2 = f"Your are {user2}"
        aim2=f"Your aim is to talk to the {user1} on the topic {ai2ai.topic}. Pose as {user2_description}. Start the conversation with a greeting. Keep in mind to close the conversation within {max_rounds} prompts."

        myobj.ai_type = ai_type2
        myobj.aim=aim2
        
        conversation_with_ai2=[]
        conversation_with_ai1=[]
        for i in range(ai2ai.max_rounds):
    
            if i==0:
                decision1=False
            else:
                decision1=True

            print(f'Iteration {i}')
            
            response_from_ai2, conversation_with_ai2 = self.chat_with_ai(user_command_to_ai=aim2,ai_name=ai_type2,conversation_history=conversation_with_ai2,skip_setup=decision1)
            
            print(f"{user2_description} : {response_from_ai2}")

            conversation_with_ai1.append({"role": "user", "content": response_from_ai2}) 
            response_from_ai1, conversation_with_ai1 = self.chat_with_ai(user_command_to_ai=aim1,ai_name=ai_type1,conversation_history=conversation_with_ai1,skip_setup=True)
            print(f"{user1_description} : {response_from_ai1}")

            conversation_with_ai2.append({"role": "user", "content": response_from_ai1})
            #conversation_with_ai1.append({"role": "user", "content": response_from_ai2}) 

        return conversation_with_ai1,conversation_with_ai2
        
if __name__=='__main__':
    max_rounds=5
    topic= 'room booking in the hotel' #get ___ done

    user1='AI assistant of user, Krishang'
    user1_description='Customer' #unique

    user2='AI assistant of Hotel'#/company
    user2_description='Hotel' #unique

    ai2ai.max_rounds=max_rounds
    ai2ai.topic=topic
    obj1=ai2ai(user1,user1_description)
    obj2=ai2ai(user2,user2_description)

    obj1.ai_to_ai_convo(obj2)