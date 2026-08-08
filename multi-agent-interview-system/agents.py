from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import os
from llm_interface import LLMInterface


@dataclass
class AgentResult:
    """Result from an agent execution, includes handoff information."""
    agent_name: str
    output: str
    next_agent: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for all specialized agents."""
    
    def __init__(self, skill_file_path: str):
        self.skill_file_path = skill_file_path
        self.llm = LLMInterface()
        self.skill_content = self._load_skill_file()
    
    def _load_skill_file(self) -> str:
        """Load the markdown skill file as operating instructions."""
        try:
            with open(self.skill_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Skill file not found: {self.skill_file_path}")
    
    @abstractmethod
    def get_agent_name(self) -> str:
        """Return the unique name of this agent."""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute the agent's task with given context."""
        pass
    
    def _call_llm(self, user_prompt: str) -> str:
        """Call LLM with skill content as system prompt."""
        skill_name = os.path.basename(self.skill_file_path).replace('.md', '')
        system_prompt = f"""You are a specialized AI agent. Follow these instructions exactly:

SKILL: {skill_name}

{self.skill_content}

Provide clear, structured, and actionable responses."""
        response = self.llm.complete(system_prompt, user_prompt)
        return response.content


class ResumeAgent(BaseAgent):
    """Analyzes resume and job description to identify strengths and gaps."""
    
    def get_agent_name(self) -> str:
        return "resume_agent"
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        resume_text = context.get("resume_text", "")
        job_description = context.get("job_description", "")
        
        user_prompt = f"""Please analyze the following resume and job description:

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis following the skill instructions."""
        
        output = self._call_llm(user_prompt)
        
        return AgentResult(
            agent_name=self.get_agent_name(),
            output=output,
            next_agent="question_agent",
            metadata={"resume_length": len(resume_text), "jd_length": len(job_description)}
        )


class QuestionAgent(BaseAgent):
    """Generates personalized interview questions based on resume analysis."""
    
    def get_agent_name(self) -> str:
        return "question_agent"
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        resume_analysis = context.get("resume_analysis", "")
        job_description = context.get("job_description", "")
        
        user_prompt = f"""Based on this resume analysis and job description, generate interview questions:

RESUME ANALYSIS:
{resume_analysis}

JOB DESCRIPTION:
{job_description}

Generate 5-7 targeted questions following the skill instructions."""
        
        output = self._call_llm(user_prompt)
        
        return AgentResult(
            agent_name=self.get_agent_name(),
            output=output,
            next_agent="interview_agent",
            metadata={"question_count": output.count('**') // 2}
        )


class InterviewAgent(BaseAgent):
    """Conducts mock interview, evaluates responses, provides immediate feedback."""
    
    def get_agent_name(self) -> str:
        return "interview_agent"
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        questions = context.get("questions", "")
        transcript = []
        
        # Parse questions and conduct interview
        question_list = self._parse_questions(questions)
        
        for i, question in enumerate(question_list, 1):
            # In a real system, this would pause for user input
            # For demo, we simulate a response
            simulated_response = context.get(f"response_{i}", 
                "I would approach this by first understanding the requirements, then designing a scalable solution...")
            
            user_prompt = f"""Evaluate this interview response:

QUESTION {i}:
{question}

CANDIDATE RESPONSE:
{simulated_response}

Provide feedback following the skill instructions."""
            
            feedback = self._call_llm(user_prompt)
            transcript.append(f"\n--- Question {i} ---\n{question}\n\nResponse: {simulated_response}\n\nFeedback: {feedback}\n")
        
        full_transcript = "\n".join(transcript)
        
        return AgentResult(
            agent_name=self.get_agent_name(),
            output=full_transcript,
            next_agent="feedback_agent",
            metadata={"questions_asked": len(question_list)}
        )
    
    def _parse_questions(self, questions_text: str) -> list:
        """Parse questions from the generated text."""
        lines = questions_text.split('\n')
        questions = []
        current_question = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                if current_question:
                    questions.append(current_question)
                current_question = line
            elif current_question:
                current_question += " " + line
        
        if current_question:
            questions.append(current_question)
        
        return questions[:7]  # Limit to 7 questions max


class FeedbackAgent(BaseAgent):
    """Synthesizes full interview transcript into final readiness assessment."""
    
    def get_agent_name(self) -> str:
        return "feedback_agent"
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        interview_transcript = context.get("interview_transcript", "")
        resume_analysis = context.get("resume_analysis", "")
        
        user_prompt = f"""Provide a comprehensive evaluation based on:

RESUME ANALYSIS:
{resume_analysis}

INTERVIEW TRANSCRIPT:
{interview_transcript}

Synthesize this into a final readiness assessment following the skill instructions."""
        
        output = self._call_llm(user_prompt)
        
        return AgentResult(
            agent_name=self.get_agent_name(),
            output=output,
            next_agent=None,  # End of chain
            metadata={"evaluation_complete": True}
        )
