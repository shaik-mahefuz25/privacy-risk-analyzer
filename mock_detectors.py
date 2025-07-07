from typing import List, Dict
import re
# ====================
# MOCK DETECTORS
# ====================
class MockDetectors:
    @staticmethod
    def mock_spacy_detect(text: str) -> List[Dict]:
        """Mock NER detection"""
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        matches = re.finditer(name_pattern, text)
        
        entities = []
        for match in matches:
            entities.append({
                'text': match.group(),
                'label': 'PERSON',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.8,
                'sensitivity': 'high',
                'description': 'Person name'
            })
        
        return entities
    
    @staticmethod
    def mock_llm_detect(text: str) -> Dict:
        """Mock LLM analysis"""
        sensitive_keywords = ['confidential', 'private', 'personal', 'ssn', 'credit card']
        score = sum(1 for keyword in sensitive_keywords if keyword in text.lower())
        
        if score >= 3:
            risk_level = 'critical'
        elif score >= 2:
            risk_level = 'high'
        elif score >= 1:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'entities': [],
            'privacy_confidence': min(0.9, score * 0.3),
            'context_score': min(1.0, score * 0.2),
            'risk_level': risk_level,
            'combined_confidence': min(0.9, score * 0.25)
        }
