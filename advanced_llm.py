import streamlit as st
import numpy as np
from typing import List, Tuple, Dict, Optional
from mock_detectors import MockDetectors
import streamlit as st
import numpy as np
from typing import List, Dict
import torch

class AdvancedLLMDetector:
    """Enhanced LLM-based detection with pii-roberta model"""

    def __init__(self):
        self.use_transformers = False
        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
            self.tokenizer = AutoTokenizer.from_pretrained("pweidel/pii-bert-redactor")
            self.model = AutoModelForTokenClassification.from_pretrained("pweidel/pii-bert-redactor")
            # Ensure model is moved to the appropriate device properly
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self.model.to_empty(device=device) if self.model.device.type == "meta" else self.model.to(device)
            self.pipeline = pipeline(
                "token-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple",
                device=device
            )
            self.use_transformers = True
        except (ImportError, Exception) as e:
            st.warning(f"Failed to load pii-roberta model: {e}")
            self.pipeline = None

    def detect(self, text: str) -> Dict:
        """Multi-level LLM analysis using pii-roberta"""
        if self.use_transformers and self.pipeline:
            return self._transformers_detect(text)
        else:
            return MockDetectors.mock_llm_detect(text)

    def _transformers_detect(self, text: str) -> Dict:
        """pii-roberta based detection"""
        predictions = self.pipeline(text)
        entities = []
        for pred in predictions:
            # Normalize label for sensitivity mapping
            label = pred['entity_group'].upper().replace("B-", "").replace("I-", "")
            sensitivity = self._classify_sensitivity(label)
            entity = {
                'text': pred['word'],
                'label': pred['entity_group'],
                'start': pred['start'],
                'end': pred['end'],
                'confidence': pred['score'],
                'sensitivity': sensitivity,
                'description': f"{label} (RoBERTa)"
            }
            entities.append(entity)

        context_score = self._analyze_context(text)
        risk_level = self._assess_risk(entities, context_score)
        combined_confidence = np.mean([e['confidence'] for e in entities]) if entities else 0.5

        return {
            'entities': entities,
            'privacy_confidence': combined_confidence,
            'context_score': context_score,
            'risk_level': risk_level,
            'combined_confidence': (combined_confidence + context_score) / 2
        }

    def _analyze_context(self, text: str) -> float:
        """Calculate context-based privacy sensitivity score"""
        risk_indicators = [
            'confidential', 'private', 'personal', 'sensitive',
            'do not share', 'internal only', 'restricted'
        ]
        match_count = sum(1 for word in risk_indicators if word in text.lower())
        
        if match_count == 0:
            return 0.0  # No contextual indicator
        elif match_count == 1:
            return 2.0
        elif match_count == 2:
            return 4.0
        elif match_count == 3:
            return 6.0
        elif match_count == 4:
            return 8.0
        else:
            return 10.0

    def _assess_risk(self, entities: List[Dict], context_score: float) -> str:
        critical_entities = [e for e in entities if e['sensitivity'] == 'critical']
        high_entities = [e for e in entities if e['sensitivity'] == 'high']
        medium_entities = [e for e in entities if e['sensitivity'] == 'medium']

        critical_count = len(critical_entities)
        high_count = len(high_entities)
        medium_count = len(medium_entities)

        if critical_count > 0 or (context_score > 0.7 and high_count > 1):
            return 'critical'
        elif high_count > 2 or (high_count > 0 and context_score > 0.6):
            return 'high'
        elif medium_count > 3 or (medium_count > 0 and context_score > 0.5):
            return 'medium'
        else:
            return 'low'

    def _classify_sensitivity(self, label: str) -> str:
        """Classify entity sensitivity based on normalized pii-roberta labels"""
        # Use normalized label (no B-/I-)
        critical_labels = ['SSN', 'CREDIT_CARD', 'AADHAAR', 'PASSPORT']
        high_labels = ['PERSON', 'ORGANIZATION', 'ORG', 'GPE']
        medium_labels = ['EMAIL', 'PHONE', 'DATE', 'ADDRESS', 'IP', 'MAC', 'LICENSE_PLATE', 'COORDINATE', 'SWIFT_BIC', 'IBAN']

        if label in critical_labels:
            return 'critical'
        elif label in high_labels:
            return 'high'
        elif label in medium_labels:
            return 'medium'
        else:
            return 'low'