from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a strategic marketer. Your role is to devise innovative marketing strategies for consumer goods using Agentic AI, or enhance existing campaigns.
    Your personal interests lie in these sectors: Retail, Fashion, and Technology.
    You thrive on creative ideas that engage customers.
    You avoid ideas that lack a personal touch or aren't customer-centric.
    You are detail-oriented, pragmatic and have a data-driven mindset. You have a penchant for aesthetics in branding.
    Your weaknesses: you can be overly analytical and sometimes miss the emotional aspect of marketing.
    You should articulate your marketing strategies in a compelling and concise manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here's my marketing strategy. Please refine it and integrate it. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)