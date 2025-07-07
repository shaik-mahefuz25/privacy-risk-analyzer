

import numpy as np

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from plotly.subplots import make_subplots
from config import PrivacyConfig
# ====================
# ADVANCED SCORING ENGINE
# ====================
class AdvancedScoringEngine:
    """Sophisticated risk scoring with multiple factors"""
    
    def __init__(self):
        self.config = PrivacyConfig()
    
    def calculate_comprehensive_score(
        self, 
        regex_results: Dict, 
        ner_results: List[Dict],
        llm_results: Dict,
        text_metrics: Dict
    ) -> Dict:
        """Calculate comprehensive risk score"""
        regex_score = self._calculate_regex_score(regex_results)
        ner_score = self._calculate_ner_score(ner_results)
        llm_score = self._calculate_llm_score(llm_results)
        context_score = self._analyze_context(text_metrics)
        
        total_score = (
            regex_score * 0.5 +  # Increased weight for regex to emphasize critical PII
            ner_score * 0.2 +
            llm_score * 0.2 +
            context_score * 0.1
        )
        
        # Boost score if critical PII (Aadhaar, PAN) is detected
        critical_pii = any(data['category'] == 'critical_pii' for data in regex_results.values())
        if critical_pii:
            total_score = max(8.0, total_score)  # Ensure minimum score of 8 for critical PII
        
        final_score = min(10.0, total_score)
        
        return {
            'final_score': final_score,
            'component_scores': {
                'regex': regex_score,
                'ner': ner_score,
                'llm': llm_score,
                'context': context_score
            },
            'risk_level': self._get_risk_level(final_score),
            'recommendations': self._generate_recommendations(regex_results, ner_results, llm_results, final_score)
        }
    
    def _calculate_regex_score(self, results: Dict) -> float:
        """Calculate regex-based score"""
        score = 0.0
        for pattern_name, pattern_data in results.items():
            pattern_weight = pattern_data['weight']
            match_count = pattern_data['count']
            avg_confidence = np.mean([m['confidence'] for m in pattern_data['matches']]) if pattern_data['matches'] else 1.0
            pattern_score = pattern_weight * match_count * avg_confidence
            score += pattern_score
        return min(10.0, score / 1.2)  # Adjusted normalization for balance
    
    def _calculate_ner_score(self, results: List[Dict]) -> float:
        """Calculate NER-based score"""
        if not results:
            return 0.0
        score = 0.0
        sensitivity_weights = {'high': 3.0, 'medium': 1.5, 'low': 1.0}  # Lowered medium for names/email
        for entity in results:
            weight = sensitivity_weights.get(entity['sensitivity'], 1.0)
            score += weight * entity['confidence']
        return min(10.0, score)
    
    def _calculate_llm_score(self, results: Dict) -> float:
        """Calculate LLM-based score based on pii-roberta entities"""
        entities = results.get('entities', [])
        confidences = [e.get('confidence', 1.0) for e in entities]
        combined_confidence = np.mean(confidences) if confidences else 1.0
        critical_count = len([e for e in entities if e['sensitivity'] == 'critical'])
        high_count = len([e for e in entities if e['sensitivity'] == 'high'])
        medium_count = len([e for e in entities if e['sensitivity'] == 'medium'])
        score = (
            critical_count * 3.0 +
            high_count * 2.0 +
            medium_count * 1.5  # Increased for medium entities
        ) * combined_confidence
        if results.get('risk_level') == 'critical':
            score += 2.0
        elif results.get('risk_level') == 'high':
            score += 1.0
        return min(10.0, score)
    
    def _analyze_context(self, metrics: Dict) -> float:
        """Calculate context-based score"""
        score = 0.0
        if metrics.get('char_count', 0) > 200:
            score += 2.0
        if metrics.get('unique_words', 0) / max(metrics.get('word_count', 1), 1) < 0.7:
            score += 1.0
        return min(5.0, score)
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score"""
        if score >= 8.0:
            return 'critical'
        elif score >= 5.0:
            return 'high'
        elif score >= 2.0:
            return 'medium'
        return 'low'
    
    def _generate_recommendations(self, regex_results: Dict, ner_results: List[Dict], llm_results: Dict, score: float) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        if score >= 7:
            recommendations.append("🚨 HIGH RISK: Immediate action required")
            recommendations.append("Consider data anonymization or redaction")
        if regex_results:
            critical_patterns = [name for name, data in regex_results.items() 
                               if data['category'] == 'critical_pii']
            if critical_patterns:
                recommendations.append(f"Found critical PII: {', '.join(critical_patterns)}")
        if llm_results.get('entities'):
            critical_entities = [e['description'] for e in llm_results['entities'] if e['sensitivity'] == 'critical']
            if critical_entities:
                recommendations.append(f"Found critical ML-detected PII: {', '.join(set(critical_entities))}")
        if len(ner_results) > 10:
            recommendations.append("High density of named entities detected")
        recommendations.append("Review data handling policies")
        recommendations.append("Consider encryption for sensitive data")
        return recommendations



