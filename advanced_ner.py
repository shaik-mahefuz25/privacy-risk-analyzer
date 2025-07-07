import spacy
from typing import List, Dict
from mock_detectors import MockDetectors
class AdvancedNERDetector:
    """Enhanced NER with custom entity types"""
    
    def __init__(self):
        self.use_spacy = False
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self.use_spacy = True
        except (ImportError, OSError):
            self.nlp = None
    
    def detect(self, text: str) -> List[Dict]:
        """Detect named entities with enhanced classification"""
        if self.use_spacy and self.nlp:
            return self._spacy_detect(text)
        else:
            return MockDetectors.mock_spacy_detect(text)
    
    def _spacy_detect(self, text: str) -> List[Dict]:
        """SpaCy-based detection"""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            confidence = self._calculate_ner_confidence(ent)
            sensitivity = self._classify_sensitivity(ent.label_)
            
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'confidence': confidence,
                'sensitivity': sensitivity,
                'description': spacy.explain(ent.label_) if hasattr(spacy, 'explain') else ent.label_
            })
        
        return entities
    
    def _calculate_ner_confidence(self, ent) -> float:
        """Calculate NER confidence based on various factors"""
        base_confidence = 0.8
        
        if len(ent.text) < 2:
            base_confidence -= 0.3
        elif len(ent.text) > 20:
            base_confidence -= 0.1
        
        if ent.text.isupper() or ent.text.istitle():
            base_confidence += 0.1
        
        return min(1.0, max(0.1, base_confidence))
    
    def _classify_sensitivity(self, label: str) -> str:
        """Classify entity sensitivity level"""
        high_sensitivity = ['PERSON', 'GPE', 'ORG']
        medium_sensitivity = ['DATE', 'TIME', 'MONEY', 'QUANTITY']
        
        if label in high_sensitivity:
            return 'high'
        elif label in medium_sensitivity:
            return 'medium'
        else:
            return 'low'
