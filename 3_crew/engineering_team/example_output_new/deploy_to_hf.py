import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo

# Load environment variables
load_dotenv()

# Get HF token from environment
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    print("ERROR: HF_TOKEN not found in .env file")
    exit(1)

# Create API instance
api = HfApi(token=hf_token)

# Create the Space
repo_id = "fareezaiahmed/trading-app-gradio"
try:
    create_repo(repo_id=repo_id, repo_type="space", space_sdk="gradio", exist_ok=True, token=hf_token)
    print(f"Space created: {repo_id}")
except Exception as e:
    print(f"Space creation failed: {e}")
    exit(1)

# Upload files
try:
    api.upload_file(
        path_or_fileobj="app.py",
        path_in_repo="app.py",
        repo_id=repo_id,
        repo_type="space",
        token=hf_token,
    )
    print("✓ Uploaded app.py")
    
    api.upload_file(
        path_or_fileobj="accounts.py",
        path_in_repo="accounts.py",
        repo_id=repo_id,
        repo_type="space",
        token=hf_token,
    )
    print("✓ Uploaded accounts.py")
    
    # Create and upload requirements.txt
    requirements = "gradio\npython-dotenv"
    api.upload_file(
        path_or_fileobj=requirements.encode(),
        path_in_repo="requirements.txt",
        repo_id=repo_id,
        repo_type="space",
        token=hf_token,
    )
    print("✓ Uploaded requirements.txt")
    
    # Create and upload README.md
    readme = """---
title: Trading Simulation Platform
emoji: 💹
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Trading Simulation Platform

## Description
This Gradio web app allows users to simulate trading by creating accounts, depositing and withdrawing funds, buying and selling shares, and viewing reports on their portfolio.
"""
    api.upload_file(
        path_or_fileobj=readme.encode(),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="space",
        token=hf_token,
    )
    print("✓ Uploaded README.md")
    
    print(f"\n✅ Deployment successful!")
    print(f"🌐 Live URL: https://huggingface.co/spaces/{repo_id}")
    
except Exception as e:
    print(f"Upload failed: {e}")
    exit(1)

