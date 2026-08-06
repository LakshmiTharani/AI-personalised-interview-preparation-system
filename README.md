AI Personalized Interview Agent

An AI-powered interview coaching system that conducts personalized mock interviews, evaluates candidate responses, and provides intelligent feedback using a multi-agent architecture.

The project simulates a real interview experience by combining multiple specialized AI agents that collaborate through a handoff mechanism to generate personalized questions, evaluate answers, and provide actionable insights for interview preparation.

Features

- Personalized interview experience
- Multi-Agent AI Architecture
- Agent Handoff Mechanism
- Real-time interview simulation
- AI-powered answer evaluation
- Performance scoring
- Personalized improvement suggestions
- Automatic interview report generation
- Modular and scalable workflow

System Architecture

The application follows a Multi-Agent Architecture, where every agent has a dedicated responsibility.

### Main Interview Agent
- Coordinates the entire interview process
- Maintains interview flow
- Routes tasks to specialized agents

### Skill Detection Agent
- Identifies candidate skills
- Selects appropriate interview domain
- Personalizes interview questions

### Question Generation Agent
- Generates technical and behavioral questions
- Adjusts difficulty based on candidate profile

### Evaluation Agent
- Evaluates candidate responses
- Scores answers using predefined criteria
- Measures communication and technical quality

### Feedback Agent
- Provides strengths and weaknesses
- Suggests areas for improvement
- Generates actionable recommendations

### Report Generation Agent
- Creates a complete interview summary
- Displays scores and detailed feedback
- Generates the final interview report

## Agent Handoff Workflow

The project uses an intelligent handoff mechanism between agents.

Candidate Information
        │
        ▼
Main Interview Agent
        │
        ▼
Skill Detection Agent
        │
        ▼
Question Generation Agent
        │
        ▼
Candidate Response
        │
        ▼
Evaluation Agent
        │
        ▼
Feedback Agent
        │
        ▼
Report Generation Agent
        │
        ▼
Final Interview Report

Each agent completes its specialized task and hands control to the next agent, creating a seamless interview experience.

## Technologies Used

- Python
- OpenAI API
- Multi-Agent AI Framework
- Prompt Engineering
- LLM-based Evaluation
- Agent Orchestration
- JSON
- REST APIs

## Project Structure

AI-Personalized-Interview-Agent/
│
├── agents/
│   ├── interview_agent.py
│   ├── skill_agent.py
│   ├── question_agent.py
│   ├── evaluation_agent.py
│   ├── feedback_agent.py
│   └── report_agent.py
│
├── prompts/
│
├── utils/
│
├── reports/
│
├── app.py
│
├── requirements.txt
│
└── README.md

## Installation

Clone the repository

```bash
git clone https://github.com/your-username/AI-Personalized-Interview-Agent.git
```

Move into the project

```bash
cd AI-Personalized-Interview-Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Add your OpenAI API key

```bash
OPENAI_API_KEY=your_api_key
```

Run the project

```bash
python app.py
```
## Workflow

1. User starts the interview.
2. Candidate information is collected.
3. Skills are identified.
4. Questions are generated.
5. Candidate answers each question.
6. AI evaluates responses.
7. Feedback is generated.
8. Performance report is created.

## Future Improvements

- Voice-based interview support
- Resume parsing
- Video interview analysis
- Emotion detection
- Adaptive difficulty levels
- Company-specific interview modes
- Dashboard analytics
- Interview history tracking

## Author

Lakshmi Tharani M S
If you found this project useful, feel free to STAR the repository.
