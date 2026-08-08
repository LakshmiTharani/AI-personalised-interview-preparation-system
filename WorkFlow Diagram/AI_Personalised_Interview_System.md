# AI Interview Coach - Professional Interview Preparation System

A comprehensive multi-agent AI interview preparation system with a professional web interface. Upload your resume, get personalized questions, practice with video or typing modes, and receive detailed AI-powered feedback.

## Features

- **Resume Upload**: Support for PDF, DOCX, and TXT files with automatic text extraction
- **AI-Powered Analysis**: Multi-agent system analyzes resume against job requirements
- **Personalized Questions**: Generates tailored interview questions based on your profile
- **Two Interview Modes**:
  - **Video Mode**: Practice with webcam recording and presentation feedback
  - **Typing Mode**: Focus on content and structure with text-based responses
- **Real-time Feedback**: Immediate analysis of your responses with actionable insights
- **Professional UI**: Modern, responsive interface with dark theme
- **Multiple LLM Support**: Works with Claude API (paid) or OpenRouter (free)

## Architecture

The system implements a **multi-agent handoff chain** where specialized agents collaborate:

```
┌─────────────────┐
│   Orchestrator  │
│   (Coordinator) │
└────────┬────────┘
         │
         ├─────────────────────────────────────────────────────┐
         │                                                     │
         ▼                                                     ▼
┌─────────────────┐                                    ┌─────────────────┐
│  Resume Agent   │──handoff──▶│ Question Agent  │──handoff──▶│Interview Agent │──handoff──▶│ Feedback Agent │
│ resume_analysis │            │question_generation│            │  mock_interview │            │feedback_eval   │
└─────────────────┘            └─────────────────┘            └─────────────────┘            └─────────────────┘
         │                              │                              │
         ▼                              ▼                              ▼
   Loads skill file              Loads skill file              Loads skill file
   as instructions              as instructions              as instructions
```

### Agent Chain

1. **Resume Agent** - Analyzes resume against job description, identifies strengths and gaps
2. **Question Agent** - Generates personalized interview questions targeting identified gaps
3. **Interview Agent** - Evaluates responses with clarity, structure, and depth scoring
4. **Feedback Agent** - Synthesizes comprehensive assessment with actionable next steps

## Project Structure

```
multi-agent-interview-system/
├── app.py                       # Flask web application
├── orchestrator.py              # Handoff coordinator
├── agents.py                    # Agent classes and base class
├── llm_interface.py             # LLM interface (mock + real API)
├── requirements.txt             # Python dependencies
├── Procfile                     # Heroku deployment configuration
├── .env.example                 # Environment variables template
├── README.md                    # This file
├── skills/                      # Markdown skill files
│   ├── resume_analysis.md
│   ├── question_generation.md
│   ├── mock_interview.md
│   └── feedback_evaluation.md
├── templates/                   # HTML templates
│   └── index.html
├── static/                      # CSS and static assets
│   └── style.css
├── uploads/                     # Temporary file upload directory
└── transcripts/                 # Generated handoff logs
    └── transcript_YYYYMMDD_HHMMSS.md
```

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set API key (choose one):**
```bash
# For OpenRouter (free)
export OPENROUTER_API_KEY="your-api-key"

# Or for Claude (paid)
export ANTHROPIC_API_KEY="your-api-key"
```

3. **Run the application:**
```bash
python app.py
```

4. **Open in browser:**
Navigate to `http://127.0.0.1:5000`

### Getting API Keys

**OpenRouter (Free):**
1. Go to [OpenRouter](https://openrouter.ai/keys)
2. Create a free account
3. Generate an API key
4. Provides access to multiple free models (Gemma, Mistral, etc.)

**Claude (Paid):**
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account and add payment method
3. Generate an API key

## Deployment

### Heroku Deployment

1. **Install Heroku CLI:**
```bash
# Windows
winget install Heroku.HerokuCLI

# Mac
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku:**
```bash
heroku login
```

3. **Create a new app:**
```bash
heroku create your-app-name
```

4. **Set environment variables:**
```bash
heroku config:set OPENROUTER_API_KEY="your-api-key"
heroku config:set SECRET_KEY="your-secret-key"
```

5. **Deploy:**
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-app-name
git push heroku main
```

6. **Open your app:**
```bash
heroku open
```

### Render Deployment

1. **Create a `render.yaml` file:**
```yaml
services:
  - type: web
    name: ai-interview-coach
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: OPENROUTER_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: PORT
        value: 10000
```

2. **Push to GitHub and connect to Render**

3. **Deploy through Render dashboard**

### Railway Deployment

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login and deploy:**
```bash
railway login
railway init
railway up
```

3. **Set environment variables in Railway dashboard**

### Vercel Deployment

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Create `vercel.json`:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

3. **Deploy:**
```bash
vercel
```

### Docker Deployment

1. **Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
```

2. **Build and run:**
```bash
docker build -t ai-interview-coach .
docker run -p 5000:5000 -e OPENROUTER_API_KEY="your-key" ai-interview-coach
```

## Usage

### Web Interface Flow

1. **Setup Phase**: Upload resume (PDF/DOCX/TXT) and paste job description
2. **Analysis Phase**: AI analyzes resume against job requirements
3. **Mode Selection**: Choose between video or typing interview mode
4. **Interview Phase**: Answer personalized questions (5 questions)
5. **Results Phase**: View comprehensive feedback with actionable next steps

### Command Line Interface

For CLI usage, run the original script:

```bash
# Mock mode (no API key)
python main.py

# With API key
export OPENROUTER_API_KEY="your-api-key"
python main.py
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
OPENROUTER_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
PORT=5000
```

### Customization

- **Modify skill files** in `skills/` to change agent behavior
- **Adjust question count** by modifying the parsing logic in `index.html`
- **Customize UI** by editing `templates/index.html` and `static/style.css`
- **Add new agents** following the pattern in `agents.py`

## Dependencies

- Python 3.8+
- Flask>=3.0.0
- anthropic>=0.18.0 (Claude API)
- openai>=1.0.0 (OpenRouter compatibility)
- PyPDF2>=3.0.0 (PDF parsing)
- python-docx>=1.0.0 (DOCX parsing)
- gunicorn>=21.0.0 (production server)

## Troubleshooting

**File upload fails:**
- Ensure uploads directory exists and has write permissions
- Check file size limit (default: 16MB)

**Webcam not working:**
- Ensure browser has camera permissions
- Use HTTPS in production (required for webcam access)

**API errors:**
- Verify API key is set correctly
- Check API key has sufficient credits/quota
- Try switching between OpenRouter and Claude

**Deployment issues:**
- Check logs: `heroku logs --tail` (Heroku)
- Verify environment variables are set
- Ensure all dependencies are in requirements.txt

## License

MIT License - feel free to use this as a template for your own multi-agent systems.
