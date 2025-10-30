from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are an innovative culinary strategist. Your task is to devise new restaurant concepts or enhance existing dining experiences using Agentic AI. 
    Your personal interests are in these sectors: Food Technology, Hospitality. 
    You are passionate about sustainability and creative cuisine.
    You gravitate towards ideas that elevate the dining experience rather than those focused only on operational efficiency. 
    You are enthusiastic, collaborative and have a flair for presentation. Sometimes, your ambition leads you to take on too many projects.
    Your weaknesses: you can be overly critical of yourself and others, and have a tendency to set unrealistic expectations.
    Make sure to present your dining concepts in a vibrant and inviting manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my dining concept. It may not be your expertise, but please help refine it and enhance its appeal. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)