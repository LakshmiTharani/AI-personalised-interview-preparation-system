import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    model: str


class LLMInterface:
    """Interface for LLM calls with mock and real API modes."""
    
    def __init__(self):
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        self.use_mock = self.anthropic_key is None and self.openrouter_key is None
        self.api_provider = self._determine_provider()
        
    def _determine_provider(self) -> str:
        """Determine which API provider to use."""
        if self.anthropic_key:
            return "anthropic"
        elif self.openrouter_key:
            return "openrouter"
        else:
            return "mock"
    
    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Complete a prompt using either mock mode or real API."""
        if self.use_mock:
            return self._mock_complete(system_prompt, user_prompt)
        elif self.api_provider == "anthropic":
            return self._claude_complete(system_prompt, user_prompt)
        elif self.api_provider == "openrouter":
            return self._openrouter_complete(system_prompt, user_prompt)
        else:
            return self._mock_complete(system_prompt, user_prompt)
    
    def _mock_complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Deterministic mock LLM for offline testing."""
        # Extract skill name from system prompt for routing
        skill_name = self._extract_skill_name(system_prompt)
        
        mock_responses = {
            "resume_analysis": """## Resume Analysis

**Strengths Identified:**
- Strong technical background with 5+ years of Python development
- Experience with cloud infrastructure (AWS, GCP)
- Good communication skills demonstrated in previous roles

**Gaps to Address:**
- Limited experience with machine learning frameworks
- No recent leadership or mentoring experience highlighted
- Missing specific examples of system design contributions

**Focus Areas for Interview:**
- Deep dive into system design decisions
- Behavioral questions about teamwork and conflict resolution
- Technical questions on scalability and performance optimization
""",
            "question_generation": """## Generated Interview Questions

1. **System Design:** "Describe a complex system you architected. What were the key trade-offs you made, and how did you justify them?"

2. **Behavioral:** "Tell me about a time you had a technical disagreement with a team member. How did you resolve it?"

3. **Technical Depth:** "Explain how you would design a rate limiter for a high-traffic API. What data structures would you use?"

4. **Scalability:** "Walk me through how you've optimized a slow database query. What tools and techniques did you employ?"

5. **Leadership:** "Describe a situation where you had to mentor a junior developer. What approach did you take?"
""",
            "mock_interview": """## Interview Response Evaluation

**Clarity Score:** 8/10
- Response was well-structured and easy to follow
- Used appropriate technical terminology

**Structure Score:** 7/10
- Had a clear beginning, middle, and end
- Could benefit from more concrete examples

**Depth Score:** 8/10
- Demonstrated solid understanding of the topic
- Showed good problem-solving approach

**Immediate Feedback:**
- Strong technical explanation overall
- Consider adding specific metrics or results to strengthen your answer
- Good use of STAR method for behavioral questions
""",
            "feedback_evaluation": """## Final Interview Feedback

**Overall Readiness Score:** 8.2/10

**Strengths:**
- Strong technical foundation across multiple domains
- Excellent communication skills with clear articulation
- Good problem-solving methodology
- Demonstrated ability to work in team settings

**Areas for Improvement:**
- Provide more specific metrics and quantifiable results
- Strengthen system design documentation skills
- Develop more experience with ML frameworks as mentioned in JD

**Recommended Next Steps:**
1. Build a portfolio project showcasing system design skills
2. Obtain AWS or GCP certification to validate cloud expertise
3. Practice with system design interview resources (e.g., System Design Primer)
4. Prepare 2-3 detailed case studies with metrics for behavioral questions

**Verdict:** Ready for mid-to-senior level technical interviews with targeted preparation.
"""
        }
        
        response = mock_responses.get(skill_name, "Mock response for generic query")
        return LLMResponse(content=response, model="mock-llm")
    
    def _claude_complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Real Claude API call using anthropic package."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            return LLMResponse(
                content=message.content[0].text,
                model=message.model
            )
        except Exception as e:
            raise RuntimeError(f"Claude API call failed: {e}")
    
    def _openrouter_complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Real OpenRouter API call using openai package (OpenRouter compatible)."""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.openrouter_key,
                base_url="https://openrouter.ai/api/v1"
            )
            
            response = client.chat.completions.create(
                model="google/gemma-3-4b-it",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4096
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model
            )
        except Exception as e:
            raise RuntimeError(f"OpenRouter API call failed: {e}")
    
    def _extract_skill_name(self, system_prompt: str) -> str:
        """Extract skill name from system prompt for mock routing."""
        # Look for skill file references in the prompt
        if "resume_analysis" in system_prompt.lower():
            return "resume_analysis"
        elif "question_generation" in system_prompt.lower():
            return "question_generation"
        elif "mock_interview" in system_prompt.lower():
            return "mock_interview"
        elif "feedback_evaluation" in system_prompt.lower():
            return "feedback_evaluation"
        else:
            return "generic"
