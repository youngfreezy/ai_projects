import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str, from_email: str = "", to_email: str = ""):
    async for chunk in ResearchManager().run(query, from_email, to_email):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    with gr.Row():
        from_email = gr.Textbox(label="From Email")
        to_email = gr.Textbox(label="To Email")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(fn=run, inputs=[query_textbox, from_email, to_email], outputs=report)
    query_textbox.submit(fn=run, inputs=[query_textbox, from_email, to_email], outputs=report)

ui.launch(inbrowser=True)
