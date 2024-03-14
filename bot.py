import logging
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from chatbot_secret_access import SLACK_APP_TOKEN, SLACK_BOT_TOKEN, OPENAT_API_KEY
from langchain.chat_models import ChatOpenal
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, SystemMessage, MessagesPlaceholder, HumanMessagePromptTemplate

def set_openai_api_key(api_key):
    """Set OpenAI API key."""
    openai.api_key = api_key

def initialize_chat_model(api_key):
    """Initialize the ChatOpenAI model."""
    return ChatOpenal(temperature=0.0, openai_api_key=api_key)

def create_standard_template(standard):
    """Create a standard conversation template."""
    return f"You are a data scientist. **{standard}**"

def initialize_chat_prompt(template):
    """Initialize the chat prompt."""
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

def initialize_slack_app(token, name):
    """Initialize the Slack app."""
    return App(token=token, name=name)

def serverless_memorization(response, bot_id):
    """Perform serverless memorization."""
    thread_messages = [message['text'] for message in response['messages']]
    thread_users = [message['user'] for message in response['messages']]
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    input_message = ""
    output_message = ""
    counter = 0
    while counter < len(thread_messages):
        if bot_id in thread_users[counter]:
            output_message = thread_messages[counter]
            counter = 2
        else:
            if counter == 1:
                input_message = input_message + " " + thread_messages[counter].replace("<@" + bot_id + ">", "Botzilla")
            else:
                input_message = thread_messages[counter].replace("<@" + bot_id + ">", "Botzilla")
            counter = 1
        if counter == 2:
            memory.save_context({"input": input_message}, {"output": output_message})
            counter = 0
            memory.load_memory_variables({})
    return memory

def answer_message(say, message, memory, bot_id, type):
    """Answer a message."""
    input_message = message['text'].replace("<@" + bot_id + ">", "Botzilla")
    if type == "im":
        say(f"{conversation.predict(input=input_message)}", thread_ts=message['ts'])
    else:
        say(f"{conversation.predict(input=input_message)}", thread_ts=message['thread_ts'])

def get_response(message, client):
    """Get response to a message."""
    try:
        response = client.conversations_replies(channel=message['channel'], ts=message['thread_ts'])
        return response
    except:
        return 'nok'

def handle_im_message(message, say, bot_id, client):
    """Handle IM message."""
    response = get_response(message, client)
    if response != 'nok':
        memory = serverless_memorization(response, bot_id)
        answer_message(say, message, memory, bot_id, "im")
    else:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        answer_message(say, message, memory, bot_id, "im")

def handle_channel_message(message, say, bot_id, client):
    """Handle channel message."""
    response = get_response(message, client)
    if response != 'nok':
        if bot_id in response['messages'][0].get('reply_users', []):
            memory = serverless_memorization(response, bot_id)
            answer_message(say, message, memory, bot_id, "channel")
        else:
            print('Do nothing')
    else:
        print('Do nothing')

def main():
    """Main function."""
    set_openai_api_key(OPENAT_API_KEY)
    chat_model = initialize_chat_model(OPENAT_API_KEY)
    standard_template = create_standard_template("expected to solve programming, data science, data analysis, data engineering, and machine learning engineering problems with optimal solution and along with proper guidelines.")
    chat_prompt = initialize_chat_prompt(standard_template)
    slack_app = initialize_slack_app(SLACK_BOT_TOKEN, "Botzilla")

    @slack_app.message()
    def handle_message(message, say):
        bot_id = slack_app.client.auth_test().get("user_id")
        if message["channel_type"] == "im":
            handle_im_message(message, say, bot_id, slack_app.client)
        else:
            if bot_id in message['text']:
                handle_channel_message(message, say, bot_id, slack_app.client)
            else:
                print('Do nothing')

    handler = SocketModeHandler(slack_app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()