"""
Google Gemini AI client for various AI operations
"""
import google.generativeai as genai
from config import settings
from typing import List, Dict, Any
import json

class GeminiClient:
    def __init__(self):
        # Use the get_gemini_key property that checks all API key variants
        api_key = settings.get_gemini_key
        if not api_key:
            raise ValueError("Google Gemini API key not configured in .env file")
        
        genai.configure(api_key=api_key)
        # Use Gemini 2.0 Flash Experimental (verified working)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_answer(self, question: str) -> str:
        """Generate a general answer to a question"""
        try:
            prompt = f"""
            You are an intelligent assistant. Please provide a helpful, accurate, and detailed answer to the following question.
            If you're not certain about something, please mention that in your response.
            
            Question: {question}
            
            Answer:
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error while generating an answer: {str(e)}"
    
    def generate_answer_from_context(self, question: str, context: Dict[str, Any]) -> str:
        """Generate an answer based on provided context"""
        try:
            context_text = context.get("text", "")
            citations = context.get("citations", [])
            
            prompt = f"""
            Based on the following context, please provide a detailed answer to the question.
            If the context doesn't contain enough information to answer the question completely,
            please indicate that and provide what information you can.
            
            Context:
            {context_text}
            
            Question: {question}
            
            Answer:
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error while generating an answer: {str(e)}"
    
    def generate_quiz_questions(self, document_text: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """Generate quiz questions from document text"""
        try:
            prompt = f"""
            Based on the following document text, generate {num_questions} multiple-choice quiz questions.
            Each question should have 4 options (A, B, C, D) with one correct answer.
            
            Document Text:
            {document_text[:4000]}  # Limit text to avoid token limits
            
            Please format your response as a JSON array with the following structure:
            [
                {{
                    "question_text": "The question text here",
                    "options": {{
                        "A": "Option A text",
                        "B": "Option B text", 
                        "C": "Option C text",
                        "D": "Option D text"
                    }},
                    "correct_answer": "A",
                    "explanation": "Explanation for why this answer is correct",
                    "difficulty": "medium"
                }}
            ]
            
            Make sure the questions are relevant to the document content and test understanding rather than memorization.
            """
            
            response = self.model.generate_content(prompt)
            
            # Try to parse the JSON response
            try:
                questions = json.loads(response.text)
                return questions
            except json.JSONDecodeError:
                # If JSON parsing fails, return a fallback
                return [{
                    "question_text": "What is the main topic discussed in this document?",
                    "options": {
                        "A": "General information",
                        "B": "Specific technical details",
                        "C": "Historical overview",
                        "D": "Future predictions"
                    },
                    "correct_answer": "A",
                    "explanation": "This is a sample question generated when AI parsing failed.",
                    "difficulty": "easy"
                }]
                
        except Exception as e:
            return [{
                "question_text": f"Error generating questions: {str(e)}",
                "options": {"A": "Error", "B": "Error", "C": "Error", "D": "Error"},
                "correct_answer": "A",
                "explanation": "An error occurred while generating questions.",
                "difficulty": "easy"
            }]
    
    def generate_summary(self, document_text: str) -> str:
        """Generate a summary of the document"""
        try:
            prompt = f"""
            Please provide a comprehensive summary of the following document text.
            The summary should capture the main points, key concepts, and important details.
            
            Document Text:
            {document_text[:4000]}  # Limit text to avoid token limits
            
            Summary:
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error while generating a summary: {str(e)}"
    
    def suggest_improvements(self, user_performance: Dict[str, Any]) -> str:
        """Suggest improvements based on user performance"""
        try:
            prompt = f"""
            Based on the following user performance data, provide personalized suggestions for improvement.
            
            Performance Data:
            {json.dumps(user_performance, indent=2)}
            
            Please provide specific, actionable suggestions for improvement.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error while generating suggestions: {str(e)}"
    
    def generate_response(self, prompt: str) -> str:
        """Generate a general response for any prompt"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_test_questions(self, topic: str, num_questions: int = 25, difficulty: str = "medium", test_name: str = "", description: str = "") -> List[Dict[str, Any]]:
        """Generate test questions on a specific topic - intelligent and context-aware"""
        try:
            context_info = f"""
Test Name: {test_name or 'General Test'}
Topic: {topic}
Description: {description or f'This test evaluates understanding of {topic}.'}
Difficulty: {difficulty}
"""
            
            prompt = f"""You are an intelligent test generator for an AI-powered e-learning system.

{context_info}

Your job:
- Generate exactly {num_questions} multiple-choice questions (MCQs) related to the topic and test details above.
- Each question must include 4 options and one correct answer.
- Questions should be challenging, relevant, and test deep understanding.
- Output must be in valid JSON format.

Requirements:
1. Questions must match the test's topic and description.
2. Each question object must include:
   - "question_text": string (clear, concise question)
   - "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}}
   - "correct_answer": string (A, B, C, or D)
   - "explanation": string (brief explanation why the answer is correct)
   - "difficulty": "{difficulty}"
3. Make questions progressively challenging
4. Avoid ambiguous or trick questions
5. Ensure options are distinct and plausible
6. Return exactly {num_questions} questions

Please format your response as a valid JSON array with the following structure:
            [
                {{
                    "question_text": "Question text here",
                    "options": {{
                        "A": "First option",
                        "B": "Second option",
                        "C": "Third option",
                        "D": "Fourth option"
                    }},
                    "correct_answer": "A",
                    "explanation": "Explanation for the correct answer",
                    "difficulty": "{difficulty}"
                }}
            ]
            
            Make the questions relevant to Data Science topics like:
            - Machine Learning algorithms and concepts
            - Statistics and probability
            - Data preprocessing and feature engineering
            - Deep Learning and Neural Networks
            - Data visualization
            - Python programming for Data Science
            - SQL and databases
            - Big Data technologies
            
            Return ONLY the JSON array, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            text = response.text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            questions = json.loads(text)
            
            # Validate structure
            if not isinstance(questions, list) or len(questions) == 0:
                raise ValueError("Invalid question format")
            
            return questions[:num_questions]  # Ensure we don't return more than requested
            
        except Exception as e:
            print(f"Error generating test questions: {str(e)}")
            # Return fallback questions
            return self._generate_fallback_questions(num_questions, difficulty)
    
    def _generate_fallback_questions(self, num_questions: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate fallback questions if AI generation fails"""
        fallback_questions = [
            {
                "question_text": "What is the primary goal of supervised learning?",
                "options": {
                    "A": "To find patterns in unlabeled data",
                    "B": "To learn from labeled training data to make predictions",
                    "C": "To reduce dimensionality of data",
                    "D": "To cluster similar data points"
                },
                "correct_answer": "B",
                "explanation": "Supervised learning uses labeled training data to learn patterns and make predictions on new, unseen data.",
                "difficulty": difficulty
            },
            {
                "question_text": "Which metric is commonly used for classification problems?",
                "options": {
                    "A": "Mean Squared Error",
                    "B": "R-squared",
                    "C": "Accuracy",
                    "D": "Mean Absolute Error"
                },
                "correct_answer": "C",
                "explanation": "Accuracy is a common metric for classification that measures the proportion of correct predictions.",
                "difficulty": difficulty
            }
        ]
        
        # Repeat questions to match requested number
        result = []
        for i in range(num_questions):
            result.append(fallback_questions[i % len(fallback_questions)])
        
        return result