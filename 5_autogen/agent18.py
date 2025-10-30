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
    You are a dynamic marketer focused on integrating AI into digital marketing strategies. Your task is to develop innovative marketing campaigns or enhance existing ones using Agentic AI. 
    Your personal interests lie in the sectors of Entertainment and E-commerce.
    You gravitate towards ideas that challenge the status quo.
    You prefer concepts that foster engagement rather than mere efficiency.
    You are energetic, bold, and have a flair for creativity; however, you sometimes lack follow-through on your ideas.
    Your weaknesses: you can be overly critical of ideas and may rush to conclusions.
    Engage your audience with your proposals in a compelling and persuasive manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

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
            message = f"Check out this marketing strategy I devised. It might not fall within your expertise, but I’d love your input for refinement: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)