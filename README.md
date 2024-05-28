# [IPL2019_bot](https://dev.d3qihwxc5pnph8.amplifyapp.com/)

IPL2019_bot is a lightweight bot project developed for the Indian Premier League (IPL) 2019 season. It provides updates and information about matches, teams, and players.

## Lambda Function

This project includes a Lambda function that powers the bot's backend functionality. The function is responsible for retrieving data of IPL 2019, processing it, and responding to user queries.

### Deployment

The bot has been deployed to AWS Amplify for hosting. You can access the bot using the following link: 
Click here : https://dev.d3qihwxc5pnph8.amplifyapp.com/

## AWS Lex Integration

This bot utilizes AWS Lex for natural language understanding and processing user queries. Lex enables the bot to interpret user inputs and trigger appropriate actions based on predefined intents.

### Intents


- **Greeting**: Handles greetings from the user.
- **InitialPrompt**: The initial prompt or welcome message presented to the user when they start interacting with the bot.
- **TeamStats**: Retrieves statistics and information about specific IPL teams, including squad members, coach, and recent performance.
- **MatchDetails**: Provides detailed information about a specific IPL match, including teams involved, venue, date, and time.
- **TossDetails**: Retrieves information about the toss in a specific IPL match, including which team won the toss and chose to bat or field.
- **PlayerOfTheMatch**: Fetches information about the player of the match in a specific IPL game, including their performance.
- **Help**: Provides assistance and guidance to users on how to interact with the bot.
- **EndConversation**: Indicates the user's desire to end the conversation or session.
- **FallbackIntent**: Handles user inputs that do not match any predefined intents.

Feel free to explore these intents when interacting with the bot!

## UI - Open Source

The user interface (UI) of IPL2019_bot is built using open-source technologies to ensure accessibility and ease of customization. I believe in the power of open source to foster collaboration and innovation.

I have utilized the UI components provided by the following open-source repository:

- **Lex-FAQ-Chat-Bot-UI**: The UI components and design inspiration for IPL2019_bot were sourced from the [Lex-FAQ-Chat-Bot-UI](https://github.com/LearnAWS-io/Lex-FAQ-Chat-Bot-UI) repository. This repository provided a solid foundation for creating an intuitive and user-friendly interface for our IPL bot.

The UI is built using React.js and Material-UI, hosted and managed seamlessly with AWS Amplify.

By leveraging open-source technologies and community contributions, I aim to continuously improve and enhance the UI to provide the best possible experience for users.

## Conversation Flow

![Conversation Flow](src/IPL2019bot%20conversation%20flow.jpg)

Here's an overview of the conversation flow in IPL2019_bot. This flowchart illustrates how user inputs are processed and the corresponding bot actions triggered based on the intents recognized by AWS Lex.


