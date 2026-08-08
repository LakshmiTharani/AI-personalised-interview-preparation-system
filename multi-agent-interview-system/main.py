"""
Multi-Agent Interview Preparation System

A coordinator that hands off control between specialized subagents,
each loading a markdown skill file as operating instructions.

Usage:
    python main.py                    # Run in mock mode (offline, deterministic)
    ANTHROPIC_API_KEY=xxx python main.py  # Run with real Claude API
"""

from orchestrator import Orchestrator


def get_sample_resume():
    """Sample resume for demonstration."""
    return """
JOHN DOE
Senior Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 5+ years of expertise in Python development,
cloud infrastructure, and building scalable distributed systems. Passionate about
clean code, system design, and mentoring junior developers.

EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Led development of microservices architecture serving 1M+ daily users
- Designed and implemented API rate limiting system reducing load by 40%
- Mentored 3 junior developers, conducting code reviews and pair programming
- Built CI/CD pipelines using GitHub Actions and Docker

Software Engineer | StartupXYZ | 2019 - 2021
- Developed RESTful APIs using Python, Flask, and PostgreSQL
- Implemented real-time data processing pipeline using Apache Kafka
- Optimized database queries, reducing response times by 60%
- Collaborated with product team to define technical requirements

EDUCATION
B.S. Computer Science, State University | 2015 - 2019
GPA: 3.7/4.0

SKILLS
- Languages: Python, JavaScript, SQL, Go
- Frameworks: Flask, Django, React
- Cloud: AWS (EC2, S3, Lambda), GCP
- Databases: PostgreSQL, MongoDB, Redis
- Tools: Docker, Kubernetes, Git, Jenkins
"""


def get_sample_job_description():
    """Sample job description for demonstration."""
    return """
Senior Software Engineer - Platform Team

We're looking for a Senior Software Engineer to join our Platform Team and help
build the next generation of our infrastructure platform.

RESPONSIBILITIES
- Design and build scalable, reliable distributed systems
- Lead technical initiatives and mentor team members
- Collaborate with cross-functional teams to deliver high-impact features
- Drive technical decisions and architecture improvements
- Contribute to engineering culture and best practices

REQUIREMENTS
- 5+ years of software development experience
- Strong proficiency in Python or similar languages
- Experience with cloud platforms (AWS, GCP, or Azure)
- Deep understanding of system design and distributed systems
- Experience with containerization and orchestration (Docker, Kubernetes)
- Strong communication and leadership skills
- Experience with machine learning frameworks is a plus

NICE TO HAVE
- Experience with microservices architecture
- Knowledge of infrastructure as code (Terraform, CloudFormation)
- Background in data engineering or real-time systems
- Experience with observability and monitoring (Prometheus, Grafana)
"""


def get_sample_responses():
    """Sample interview responses for demonstration."""
    return {
        "response_1": "I designed a microservices architecture for our e-commerce platform. The key trade-offs were between consistency and availability - we chose eventual consistency for the catalog service to handle high traffic during sales events. This allowed us to scale horizontally and maintain 99.9% uptime even during peak loads.",
        "response_2": "I had a disagreement with a teammate about whether to use a SQL or NoSQL database for a new feature. I scheduled a meeting to understand their perspective, we listed pros and cons together, and ultimately decided on PostgreSQL because the data had strong relational requirements. We maintained a good working relationship and the decision proved correct.",
        "response_3": "For a high-traffic API rate limiter, I'd use Redis with a sliding window algorithm. Store request counts with TTL, use atomic increments for thread-safety, and shard across multiple Redis instances for scalability. The key is to handle edge cases like clock skew and ensure fair distribution across shards.",
        "response_4": "I optimized a slow query by adding composite indexes on frequently filtered columns, restructuring the JOIN order, and implementing query result caching. The query went from 8 seconds to 200ms. I used EXPLAIN ANALYZE to identify the bottlenecks and validated improvements with load testing.",
        "response_5": "When mentoring a junior developer, I start by understanding their learning style and goals. I pair program on real tasks, explain my thought process aloud, and gradually increase their responsibility. I provide specific, actionable feedback and celebrate their wins to build confidence. For example, I helped a junior engineer lead their first feature deployment by breaking it down into manageable steps."
    }


def main():
    """Run the multi-agent interview preparation system."""
    print("\n" + "="*70)
    print("Multi-Agent Interview Preparation System")
    print("="*70)
    
    # Check if using real API or mock mode
    import os
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\nMode: REAL CLAUDE API")
        print("Using Anthropic API for LLM calls\n")
    elif os.environ.get("OPENROUTER_API_KEY"):
        print("\nMode: REAL OPENROUTER API")
        print("Using OpenRouter API for LLM calls (free tier available)\n")
    else:
        print("\nMode: MOCK (Offline)")
        print("Using deterministic mock LLM for testing\n")
        print("Tip: Set ANTHROPIC_API_KEY or OPENROUTER_API_KEY environment variable to use real LLM\n")
    
    # Initialize orchestrator
    orchestrator = Orchestrator(skills_dir="skills")
    
    # Prepare initial context
    context = {
        "resume_text": get_sample_resume(),
        "job_description": get_sample_job_description(),
        **get_sample_responses()
    }
    
    # Run the handoff chain
    try:
        final_context = orchestrator.run(
            initial_context=context,
            start_agent="resume_agent"
        )
        
        # Display final feedback
        print("\n" + "="*70)
        print("FINAL FEEDBACK")
        print("="*70 + "\n")
        print(final_context.get("feedback_agent_output", "No feedback available"))
        
        print("\n" + "="*70)
        print("System execution complete!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
