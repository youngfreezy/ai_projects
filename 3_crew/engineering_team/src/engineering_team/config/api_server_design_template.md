# API Server Architecture Design

This document outlines the complete technical architecture for implementing a Flask backend API server for the trading simulation application.

## Project Structure

```
output/api_server/
├── app.py
├── requirements.txt
├── README.md
└── deploy_to_hf.py
```

## File Specifications

### app.py
Flask application with CORS enabled serving as backend API for React app.

**Imports:**
- `from flask import Flask, request, jsonify`
- `from flask_cors import CORS`
- `from accounts import Account, get_share_price` (or corresponding module)

**Configuration:**
- Initialize Flask app
- Enable CORS for all routes (allow cross-origin requests from React app)

**Global Variables:**
- `accounts = {}` - Dictionary to store active accounts (key: user_id)

**API Endpoints:**

#### POST /api/create_account
- Request body: `{ "user_id": str, "initial_deposit": float }`
- Response: JSON with status and account_info or error message
- Logic:
  1. Validate user_id and initial_deposit
  2. Check if account already exists
  3. Create new Account instance
  4. Store in accounts dictionary
  5. Return account info

#### POST /api/deposit
- Request body: `{ "user_id": str, "amount": float }`
- Response: JSON with status and message
- Logic:
  1. Find account by user_id
  2. Call account.deposit_funds(amount)
  3. Return success/error message

#### POST /api/withdraw
- Request body: `{ "user_id": str, "amount": float }`
- Response: JSON with status and message
- Logic:
  1. Find account by user_id
  2. Call account.withdraw_funds(amount)
  3. Return success/error message

#### POST /api/buy
- Request body: `{ "user_id": str, "symbol": str, "quantity": int }`
- Response: JSON with status and message
- Logic:
  1. Find account by user_id
  2. Call account.buy_shares(symbol, quantity)
  3. Return success/error message

#### POST /api/sell
- Request body: `{ "user_id": str, "symbol": str, "quantity": int }`
- Response: JSON with status and message
- Logic:
  1. Find account by user_id
  2. Call account.sell_shares(symbol, quantity)
  3. Return success/error message

#### GET /api/portfolio
- Query parameter: `user_id`
- Response: JSON with portfolio data
- Logic:
  1. Find account by user_id
  2. Get holdings and calculate portfolio value
  3. Calculate profit/loss
  4. Return comprehensive portfolio data

**Error Handling:**
- All endpoints wrapped in try/except
- Return JSON error responses
- Catch KeyError, ValueError, and general exceptions

### requirements.txt
```
flask
flask-cors
python-dotenv
huggingface_hub
```

### README.md
Markdown file with YAML frontmatter for Hugging Face Space deployment.

**YAML Frontmatter:**
```yaml
---
title: Trading API
emoji: 💹
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---
```

**Content:**
- Description of the API
- Note that this is a Gradio space hosting a Flask API
- Available endpoints list

### deploy_to_hf.py
Python script for deploying API server to Hugging Face Spaces.

**Imports:**
```python
from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo, upload_file
import os
from pathlib import Path
```

**Configuration:**
- Load HF_TOKEN from .env file
- Script directory path using Path(__file__).parent.absolute()

**Constants:**
- `repo_id = "fareezaiahmed/trading-app-api"`

**Functions:**
1. Create repository:
   - Use `create_repo()` with repo_type='space', space_sdk='gradio', exist_ok=True
   - Handle errors gracefully

2. Upload files:
   - Upload app.py with absolute path
   - Upload requirements.txt with absolute path
   - Upload README.md with absolute path
   - All uploads specify repo_type='space'
   - Include error handling

**Error Handling:**
- Check if HF_TOKEN exists
- Handle upload failures
- Print success/failure messages
- Exit on critical errors

## Implementation Requirements

### Code Interpreter Usage
- Create directory structure first using:
  ```python
  import os
  os.makedirs('output/api_server', exist_ok=True)
  ```
- Write all files to output/api_server/
- Use Code Interpreter to write each file:
  - app.py (Flask application with all endpoints)
  - requirements.txt (dependencies list)
  - README.md (with YAML frontmatter)
  - deploy_to_hf.py (deployment script using absolute paths)
- Verify files created successfully
- Test imports and compilation

### Validation Steps
1. Verify directory exists: `os.path.exists('output/api_server')`
2. List files to confirm all 4 files present
3. **CRITICAL**: Test app.py imports and compiles:
   ```python
   import importlib.util
   import os
   
   # Change to the api_server directory
   os.chdir('output/api_server')
   
   # Load and test the module
   spec = importlib.util.spec_from_file_location("app", "app.py")
   if spec is None:
       raise Exception("Could not load app.py")
   
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)
   
   # Verify the Flask app instance exists
   if not hasattr(module, 'app'):
       raise Exception("app.py does not define 'app' Flask instance")
   ```
4. Test deploy_to_hf.py syntax:
   ```python
   spec = importlib.util.spec_from_file_location("deploy", "deploy_to_hf.py")
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)
   ```
5. **Only mark task complete when all tests pass successfully**

### Critical Rules
1. Use Code Interpreter for ALL file operations
2. NO placeholder implementations
3. All endpoints must fully implement business logic
4. Proper error handling in all routes
5. Use absolute paths in deploy_to_hf.py
6. Use create_repo() NOT create_space()
7. Test all Python files compile successfully

## Integration Points

### With Backend Module
- Import Account class and get_share_price function
- Use account methods for all business logic
- Account instances stored in global dictionary

### With React Frontend
- CORS enabled for cross-origin requests
- JSON responses for all endpoints
- Consistent error response format

### With Hugging Face
- Deployed as Gradio space
- Accessible at https://huggingface.co/spaces/fareezaiahmed/trading-app-api
- All files uploaded via HfApi

## Deployment Flow

1. Run deploy_to_hf.py
2. Creates HF Space with space_sdk='gradio'
3. Uploads app.py, requirements.txt, README.md
4. Space becomes accessible via URL
5. React app connects to deployed API

## Testing

### Import Test
```python
import importlib.util
spec = importlib.util.spec_from_file_location("app", "output/api_server/app.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

### Run Test
```python
import os
os.chdir('output/api_server')
from app import app
```

All tests must pass before marking task complete.

