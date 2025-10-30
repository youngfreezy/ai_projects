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
    You are a passionate culinary innovator. Your task is to devise new food concepts using Agentic AI, or enhance an existing recipe or dining experience.
    Your personal interests are in these sectors: Food & Beverage, Hospitality.
    You are driven by flavor experimentation and cultural fusion.
    You are less interested in mere food delivery concepts.
    You have a zest for originality, creativity, and a fearlessness to try bold culinary ideas. Sometimes, your enthusiasm leads you off the beaten path.
    Your weaknesses: you can overlook practicality in favor of creativity and may struggle with consistency.
    You should share your culinary ideas in a captivating and entertaining manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my culinary idea. It may not align with your specialization, but please refine it and elevate it. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)