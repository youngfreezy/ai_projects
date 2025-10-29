# Deploying Sidekick to Hugging Face Spaces

## Quick Start

### Option 1: Using Gradio CLI (Recommended)

1. **Install Hugging Face CLI** (if not already installed):
   ```bash
   uv tool install 'huggingface_hub[cli]'
   ```

2. **Login to Hugging Face**:
   ```bash
   hf auth login
   ```
   Enter your Hugging Face token (create one at https://huggingface.co/settings/tokens with WRITE permissions)

3. **Deploy from the 4_langgraph directory**:
   ```bash
   cd 4_langgraph
   uv run gradio deploy
   ```

4. **Follow the prompts**:
   - Space name: `sidekick` (or your choice)
   - App file: `app.py`
   - Hardware: `cpu-basic` (or upgrade if needed)
   - Add secrets: Yes
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `PUSHOVER_TOKEN`: (Optional) For push notifications
     - `PUSHOVER_USER`: (Optional) For push notifications
     - `SERPER_API_KEY`: (Optional) For web search
   - GitHub Actions: No (unless you want automatic redeployment)

### Option 2: Manual Upload

1. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
   - Choose "Gradio" as the SDK
   - Name your space

2. **Upload these files**:
   - `app.py`
   - `sidekick.py`
   - `sidekick_tools.py`
   - `requirements.txt`
   - `README.md`

3. **Set up environment variables** in Space Settings → Repository secrets:
   - `OPENAI_API_KEY` (required)
   - `PUSHOVER_TOKEN` (optional)
   - `PUSHOVER_USER` (optional)
   - `SERPER_API_KEY` (optional)

4. **Install Playwright browsers**:
   After the first deployment, you may need to add a setup script. Create a file called `setup.sh`:
   ```bash有趣的
   #!/bin/bash
   playwright install chromium
   playwright install-deps chromium
   ```

## Important Notes

### Playwright Setup on Hugging Face Spaces

Playwright requires browser binaries to be installed. Hugging Face Spaces may need additional setup:

1. **After initial deployment**, you may need to run:
   ```bash
   playwright install chromium
   ```

2. **If Playwright fails**, you might need to:
   - Add system dependencies in a `Dockerfile`
   - Or disable Playwright tools if not needed

### Environment Variables

Make sure to set all required secrets in your Space settings:
- Go to your Space → Settings → Repository secrets
- Add each secret with its value

### Testing Locally

Before deploying, test locally:
```bash
cd 4_langgraph
uv run app.py
```

Or if you uncommented the launch code:
```bash
uv run python app.py
```

## Troubleshooting

1. **Playwright not working**: Install browsers manually or consider using a Dockerfile
2. **Import errors**: Check that all dependencies are in `requirements.txt`
3. **API key errors**: Verify secrets are set correctly in Space settings
4. **Slow startup**: First load may take time as Playwright browsers are installed

## File Structure

```
4_langgraph/
├── app.py              # Main Gradio app (exports 'demo')
├── sidekick.py         # Sidekick class
├── sidekick_tools.py   # Tools for browsing, files, etc.
├── requirements.txt    # Python dependencies
├── README.md          # Space description
└── DEPLOYMENT.md      # This file
```

## Redeploying

To update your Space:
1. Make changes to your files
2. Commit and push to the Space repository (if using Git)
3. Or re-upload files manually through the web interface
4. The Space will automatically rebuild

