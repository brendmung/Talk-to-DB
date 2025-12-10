# core/ai.py

import json
from typing import List, Dict, Any
import requests

class AIResponseGenerator:
    """Generates natural language responses using LLM"""
    
    def __init__(self, api_url: str, model: str = "gpt-4o"):
        self.api_url = api_url
        self.model = model
    
    def generate_response(self, question: str, results: List[Dict], context: str = "") -> str:
        """Generate natural language response"""
        
        system_prompt = context or """You are a helpful database assistant. 
Answer user questions based on the provided data.

When responding:
- Be conversational and friendly
- Highlight the most relevant results
- Mention key details from the data
- If no good matches, suggest alternatives
- Use natural language, not robotic responses"""
        
        # Prepare content, ensuring non-serializable objects (like ObjectIds if not handled) are stringified
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"User Question: {question}\n\nRelevant Data:\n{json.dumps(results, indent=2, default=str)}"
                }
            ]
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            elif "message" in result:
                # Handle error messages from API if structure is non-standard
                return str(result)
            else:
                return str(result)
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
