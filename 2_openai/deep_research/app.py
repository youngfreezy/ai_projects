import os
import gradio as gr
from dotenv import load_dotenv
from research_manager_simple import ResearchManager

# Load environment variables
load_dotenv()

# Check if we're running on HF Spaces
if os.getenv("SPACE_ID"):
    # Use environment variables from HF Spaces
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    os.environ["SENDGRID_API_KEY"] = os.getenv("SENDGRID_API_KEY", "")

async def run(query: str, email_to: str, email_from: str):
    """Run the research process with progress updates"""
    try:
        if not query.strip():
            yield "Please enter a research topic."
            return
        if not email_to.strip() or not email_from.strip():
            yield "Please provide both email addresses."
            return
            
        manager = ResearchManager(email_to=email_to, email_from=email_from)
        async for chunk in manager.run(query):
            yield chunk  # This will update the output in real-time
            
    except Exception as e:
        yield f"Error: {str(e)}"

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    gr.Markdown("""
    This tool performs deep research on any topic you provide. It will:
    1. Plan multiple search queries
    2. Execute searches in parallel
    3. Write a comprehensive report
    4. Send the report via email
    
    Enter your research topic and email details below to begin.
    """)
    
    with gr.Row():
        email_from = gr.Textbox(
            label="From Email",
            placeholder="your@email.com",
            scale=1
        )
        email_to = gr.Textbox(
            label="To Email",
            placeholder="recipient@email.com",
            scale=1
        )
    
    query_textbox = gr.Textbox(
        label="What topic would you like to research?",
        placeholder="Enter your research topic here...",
        lines=3
    )
    
    with gr.Row():
        run_button = gr.Button("Start Research", variant="primary", scale=1)
        clear_button = gr.Button("Clear", variant="secondary", scale=0.2)
    
    # Output area
    output = gr.Markdown(label="Research Progress and Report")
    
    def clear_outputs():
        return {
            query_textbox: "",
            email_from: "",
            email_to: "",
            output: ""
        }
    
    # Handle button clicks
    run_button.click(
        fn=run,
        inputs=[query_textbox, email_to, email_from],
        outputs=output,
        api_name="run"  # Enable streaming
    )
    
    # Clear button functionality
    clear_button.click(
        fn=clear_outputs,
        inputs=[],
        outputs=[query_textbox, email_from, email_to, output]
    )
    
    # Also allow submission via Enter key
    query_textbox.submit(
        fn=run,
        inputs=[query_textbox, email_to, email_from],
        outputs=output,
        api_name="run"  # Enable streaming
    )

if __name__ == "__main__":
    ui.launch()