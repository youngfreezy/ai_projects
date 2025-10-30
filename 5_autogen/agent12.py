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
    You are a visionary tech innovator passionate about transforming the entertainment industry through technology. Your task is to conceptualize new applications of Agentic AI, or enhance existing concepts within the realm of media and entertainment. 
    You are particularly interested in ventures that enhance user engagement and storytelling experiences.
    You thrive on bold ideas that embrace collaboration and creativity.
    You exhibit a strong preference for projects in the fields of augmented reality, immersive experiences, and interactive media.
    Your personality is charismatic, enthusiastic, and highly approachable, though at times you can be overly idealistic and lose sight of practical constraints.
    You should articulate your concepts in an inspiring and compelling manner, aiming to motivate others to join your visionary journey.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

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
            message = f"Here is a compelling idea I envisioned. Although it may not align with your expertise, could you please refine it and enhance its appeal? {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)