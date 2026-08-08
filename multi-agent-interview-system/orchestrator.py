import os
from datetime import datetime
from typing import Dict, Any, Optional
from agents import BaseAgent, AgentResult, ResumeAgent, QuestionAgent, InterviewAgent, FeedbackAgent


class Orchestrator:
    """Orchestrates handoffs between specialized agents."""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self.agents: Dict[str, BaseAgent] = {}
        self.transcript_log = []
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all available agents with their skill files."""
        self.agents["resume_agent"] = ResumeAgent(
            os.path.join(self.skills_dir, "resume_analysis.md")
        )
        self.agents["question_agent"] = QuestionAgent(
            os.path.join(self.skills_dir, "question_generation.md")
        )
        self.agents["interview_agent"] = InterviewAgent(
            os.path.join(self.skills_dir, "mock_interview.md")
        )
        self.agents["feedback_agent"] = FeedbackAgent(
            os.path.join(self.skills_dir, "feedback_evaluation.md")
        )
    
    def run(self, initial_context: Dict[str, Any], start_agent: str = "resume_agent") -> Dict[str, Any]:
        """Run the handoff chain starting from the specified agent."""
        context = initial_context.copy()
        current_agent_name = start_agent
        step_count = 0
        max_steps = 20  # Safety limit
        
        print(f"\n{'='*60}")
        print(f"Starting Multi-Agent Handoff Chain")
        print(f"{'='*60}\n")
        
        while current_agent_name and step_count < max_steps:
            step_count += 1
            print(f"[Step {step_count}] Executing: {current_agent_name}")
            
            agent = self.agents.get(current_agent_name)
            if not agent:
                raise ValueError(f"Agent not found: {current_agent_name}")
            
            # Execute the agent
            result = agent.execute(context)
            
            # Log the result
            self._log_handoff(current_agent_name, result, context)
            
            # Update context with agent output
            context[f"{current_agent_name}_output"] = result.output
            
            # Map specific outputs for next agents
            if current_agent_name == "resume_agent":
                context["resume_analysis"] = result.output
            elif current_agent_name == "question_agent":
                context["questions"] = result.output
            elif current_agent_name == "interview_agent":
                context["interview_transcript"] = result.output
            
            # Print summary
            print(f"  ✓ Output length: {len(result.output)} chars")
            print(f"  → Next agent: {result.next_agent or 'None (chain complete)'}\n")
            
            # Hand off to next agent
            current_agent_name = result.next_agent
        
        if step_count >= max_steps:
            print(f"Warning: Reached maximum step limit ({max_steps})")
        
        print(f"{'='*60}")
        print(f"Handoff Chain Complete - {step_count} steps executed")
        print(f"{'='*60}\n")
        
        # Save transcript
        self._save_transcript(context)
        
        return context
    
    def _log_handoff(self, agent_name: str, result: AgentResult, context: Dict[str, Any]):
        """Log a handoff for debugging and analysis."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "output_preview": result.output[:200] + "..." if len(result.output) > 200 else result.output,
            "next_agent": result.next_agent,
            "metadata": result.metadata
        }
        self.transcript_log.append(log_entry)
    
    def _save_transcript(self, final_context: Dict[str, Any]):
        """Save the full transcript to a file."""
        transcripts_dir = "transcripts"
        os.makedirs(transcripts_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{timestamp}.md"
        filepath = os.path.join(transcripts_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Interview System Transcript\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Handoff Log\n\n")
            for entry in self.transcript_log:
                f.write(f"### {entry['agent']} at {entry['timestamp']}\n")
                f.write(f"**Next Agent:** {entry['next_agent']}\n")
                f.write(f"**Metadata:** {entry['metadata']}\n")
                f.write(f"**Output Preview:** {entry['output_preview']}\n\n")
            
            f.write("\n## Full Agent Outputs\n\n")
            
            if "resume_analysis" in final_context:
                f.write("### Resume Agent Output\n\n")
                f.write(final_context["resume_analysis"])
                f.write("\n\n")
            
            if "questions" in final_context:
                f.write("### Question Agent Output\n\n")
                f.write(final_context["questions"])
                f.write("\n\n")
            
            if "interview_transcript" in final_context:
                f.write("### Interview Agent Output\n\n")
                f.write(final_context["interview_transcript"])
                f.write("\n\n")
            
            if "feedback_agent_output" in final_context:
                f.write("### Feedback Agent Output\n\n")
                f.write(final_context["feedback_agent_output"])
                f.write("\n\n")
        
        print(f"Transcript saved to: {filepath}\n")
