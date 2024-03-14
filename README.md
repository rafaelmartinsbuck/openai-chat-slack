# OpenAI API Chatbot with Slack

## Features

- **ChatBot Model**: Utilizes the OpenAI API to power the ChatBot model, allowing for natural language understanding and generation.
- **Slack Integration**: Integrates the ChatBot with Slack using the Slack Bolt framework, enabling communication between the Botzilla and Slack users.
- **Serverless Memorization**: Implements a serverless memorization mechanism to remember past conversations and provide contextually relevant responses.
- **Conversation Handling**: Handles incoming messages from Slack, including direct messages and messages in channels, and responds accordingly.

## Usage

1. **Setting Up OpenAI API Key**: Replace the placeholder with your OpenAI API key in the provided Python code to authenticate with the OpenAI API.
2. **Setting Up Slack Tokens**: Replace the placeholder with your Slack app tokens (`SLACK_APP_TOKEN` and `SLACK_BOT_TOKEN`) to authenticate with the Slack API.
3. **Running the Code**: Execute the Python code in a Python environment with the necessary dependencies installed. Ensure that the required libraries (`slack_bolt`, `openai`) are installed.
4. **Interacting with Botzilla**: Once the code is running, Botzilla will be active in the configured Slack workspace. Users can interact with Botzilla by sending messages in channels or direct messages.

## Dependencies

- **OpenAI Python Client**: Required for interfacing with the OpenAI API.
- **Slack Bolt**: Required for building Slack apps and handling interactions with Slack.
- **Other Libraries**: Additional libraries may be required based on the specific dependencies of the included code.
