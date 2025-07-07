import streamlit as st
import pandas as pd

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import PrivacyConfig


# ====================
# VISUALIZATION COMPONENTS
# ====================

class PrivacyVisualizer:
    """Advanced visualization for privacy analysis results"""
    
    @staticmethod
    def create_risk_dashboard(scoring_results: Dict, regex_results: Dict, ner_results: List[Dict], llm_results: Dict):
        """Create comprehensive risk dashboard"""
        
        # Risk Score Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = scoring_results['final_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Privacy Risk Score"},
            delta = {'reference': 5},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 3], 'color': "lightgreen"},
                    {'range': [3, 6], 'color': "yellow"},
                    {'range': [6, 8], 'color': "orange"},
                    {'range': [8, 10], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 8
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Component Scores Breakdown
        components = list(scoring_results['component_scores'].keys())
        scores = list(scoring_results['component_scores'].values())
        
        fig_bar = px.bar(
            x=components,
            y=scores,
            title="Risk Score Components",
            color=scores,
            color_continuous_scale="RdYlGn_r"
        )
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # PII Distribution
        pii_types = []
        pii_counts = []
        pii_weights = []
        
        for pattern_name, data in regex_results.items():
            pii_types.append(pattern_name)
            pii_counts.append(data['count'])
            pii_weights.append(data['weight'])
        
        for entity in llm_results.get('entities', []):
            pii_types.append(entity['description'])
            pii_counts.append(1)
            pii_weights.append(PrivacyConfig.RISK_WEIGHTS.get(entity['sensitivity'], 1.0))
        
        if pii_types:
            fig_scatter = px.scatter(
                x=pii_counts,
                y=pii_weights,
                size=pii_counts,
                hover_name=pii_types,
                title="PII Detection Overview",
                labels={'x': 'Count', 'y': 'Risk Weight'}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    @staticmethod
    def create_trend_analysis(historical_data: List[Dict]):
        """Create trend analysis visualization"""
        if not historical_data:
            st.info("No historical data available for trend analysis")
            return
        
        df = pd.DataFrame(historical_data)
        
        fig = px.line(
            df,
            x='timestamp',
            y='risk_score',
            title="Privacy Risk Trends Over Time",
            markers=True
        )
        
        fig.add_hline(y=6, line_dash="dash", line_color="orange", 
                     annotation_text="High Risk Threshold")
        
        st.plotly_chart(fig, use_container_width=True)
