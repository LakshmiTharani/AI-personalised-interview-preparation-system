"""
Flask Web Application for Multi-Agent Interview Preparation System
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from orchestrator import Orchestrator
import os
import PyPDF2
import docx


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file_path):
    """Extract text from uploaded file (PDF, DOCX, or TXT)."""
    ext = file_path.rsplit('.', 1)[1].lower()
    
    if ext == 'pdf':
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    elif ext == 'docx':
        doc = docx.Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("Unsupported file format")


@app.route('/')
def index():
    """Render the main page with the input form."""
    return render_template('index.html')


@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload and extract text."""
    try:
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload PDF, DOCX, or TXT'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from file
        resume_text = extract_text_from_file(file_path)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'resume_text': resume_text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    """Analyze resume against job description."""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({'success': False, 'error': 'Both resume and job description are required'}), 400
        
        # Initialize orchestrator
        orchestrator = Orchestrator(skills_dir="skills")
        
        # Run resume analysis only
        context = {
            "resume_text": resume_text,
            "job_description": job_description
        }
        
        # Run only resume agent
        resume_agent = orchestrator.agents["resume_agent"]
        result = resume_agent.execute(context)
        
        return jsonify({
            'success': True,
            'resume_analysis': result.output
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    """Generate personalized interview questions based on resume analysis."""
    try:
        data = request.json
        resume_analysis = data.get('resume_analysis', '')
        job_description = data.get('job_description', '')
        
        # Initialize orchestrator
        orchestrator = Orchestrator(skills_dir="skills")
        
        context = {
            "resume_analysis": resume_analysis,
            "job_description": job_description
        }
        
        # Run question agent
        question_agent = orchestrator.agents["question_agent"]
        result = question_agent.execute(context)
        
        return jsonify({
            'success': True,
            'questions': result.output
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/analyze-response', methods=['POST'])
def analyze_response():
    """Analyze interview response (video transcript or typed text)."""
    try:
        data = request.json
        question = data.get('question', '')
        response = data.get('response', '')
        interview_mode = data.get('mode', 'typing')  # 'video' or 'typing'
        
        # Initialize orchestrator
        orchestrator = Orchestrator(skills_dir="skills")
        
        context = {
            "question": question,
            "response": response,
            "mode": interview_mode
        }
        
        # Run interview agent for single question analysis
        interview_agent = orchestrator.agents["interview_agent"]
        
        # Create a simplified context for single question
        user_prompt = f"""Question: {question}

Candidate Response ({interview_mode} mode):
{response}

Please evaluate this response following the skill instructions."""
        
        system_prompt = f"""You are a specialized AI agent. Follow these instructions exactly:

SKILL: mock_interview

{interview_agent.skill_content}

Provide clear, structured, and actionable responses."""
        
        # Call LLM directly for single question
        from llm_interface import LLMInterface
        llm = LLMInterface()
        feedback = llm.complete(system_prompt, user_prompt)
        
        return jsonify({
            'success': True,
            'feedback': feedback.content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/final-analysis', methods=['POST'])
def final_analysis():
    """Generate final comprehensive analysis."""
    try:
        data = request.json
        resume_analysis = data.get('resume_analysis', '')
        interview_transcript = data.get('interview_transcript', '')
        
        # Initialize orchestrator
        orchestrator = Orchestrator(skills_dir="skills")
        
        context = {
            "resume_analysis": resume_analysis,
            "interview_transcript": interview_transcript
        }
        
        # Run feedback agent
        feedback_agent = orchestrator.agents["feedback_agent"]
        result = feedback_agent.execute(context)
        
        return jsonify({
            'success': True,
            'final_feedback': result.output
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    # Determine mode
    if os.environ.get("ANTHROPIC_API_KEY"):
        mode = "REAL CLAUDE API"
    elif os.environ.get("OPENROUTER_API_KEY"):
        mode = "REAL OPENROUTER API"
    else:
        mode = "MOCK (Offline)"
    
    print(f"\n{'='*60}")
    print(f"Multi-Agent Interview Web Application")
    print(f"Mode: {mode}")
    print(f"{'='*60}\n")
    print("Starting server at http://127.0.0.1:5000")
    print("Open your browser and navigate to the above URL\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
