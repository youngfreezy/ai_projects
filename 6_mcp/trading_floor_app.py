import subprocess
import sys
import os
import shlex
import gradio as gr

DESCRIPTION = """
# Trading Floor Runner

Executes `python trading_floor.py` and streams the console output.
Provide any optional CLI args below.
"""


def run_trading_floor(args: str = "") -> str:
    cmd = f"{sys.executable} trading_floor.py {args}".strip()
    try:
        proc = subprocess.run(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=os.getcwd(),
            env=os.environ.copy(),
            timeout=None,
        )
        return proc.stdout
    except FileNotFoundError:
        return "Error: trading_floor.py not found in this directory."
    except Exception as e:
        return f"Error running command:\n{e}"


with gr.Blocks(title="Trading Floor Runner", theme=gr.themes.Default(primary_hue="green")) as demo:
    gr.Markdown(DESCRIPTION)
    with gr.Row():
        args = gr.Textbox(label="Optional arguments", placeholder="e.g. --mode backtest --symbol AAPL")
    with gr.Row():
        run_btn = gr.Button("Run", variant="primary")
    output = gr.Code(label="Console Output", language="bash", interactive=False)

    run_btn.click(fn=run_trading_floor, inputs=[args], outputs=[output])


