AI Personalized Interview Agent
This README documents the multi-agent workflow that powers the AI Interview Intelligence Coach — how a request moves through the system, who handles it at each step, and how the system personalizes future sessions.

## ARCHITECTURE

1. Entry — a request comes in through the FastAPI gateway and is handed to the Supervisor Agent.
2. Routing — the Supervisor reads the current session state and decides which Coordinator should handle it:
          Profile Coordinator — resume upload, company/JD research
          Interview Coordinator — live mock interview (questions, coding, voice, vision, emotion)
          Learning Coordinator — plan generation, progress dashboard
3. Coordinator dispatch — the chosen Coordinator calls its own sub-agents:
          Profile: Resume Agent → Company Research Agent
          Interview: Question Generator, Coding Interview Agent, Voice Analysis Agent, Vision Analysis Agent, Emotion Detection Agent all run and feed into a shared Evaluation Agent, which passes its scoring to the Feedback Agent
          Learning: Learning Planner Agent, Dashboard Agent — the Planner reads the latest Feedback Agent output ("weak topics inform next plan")
4. Memory write — every agent that produces a durable result (Resume Agent, Company Research Agent, Feedback Agent, Planner Agent, Dashboard Agent) writes to the Memory Agent, which persists to PostgreSQL (structured history) and ChromaDB (embeddings for RAG).
5. Digital Twin update — the Memory Agent's accumulated history is distilled into the Digital Twin (confidence, coding style, weak/strong topics, preferred difficulty, learning speed).
6. Personalization loop — the Digital Twin feeds back into the Supervisor Agent, so routing, question difficulty, and plan generation on the next session are shaped by everything learned so far.

## Why this FLOW
Supervisor + Coordinators + sub-agents keeps each agent single-purpose and testable in isolation, instead of one monolithic prompt trying to do everything.
Shared Memory Agent means every coordinator writes to the same place, so the Digital Twin always has a complete picture rather than fragmented, coordinator-specific memory.
Feedback loop into the Supervisor is what makes the system stateful across sessions — without it, this would just be a stateless quiz flow.
