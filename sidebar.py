import streamlit as st
import json
import pandas as pd
import numpy as np
import re # Added for TextProcessor
import fitz # Added for TextProcessor
from datetime import datetime
from typing import Dict

# ====================
# CONFIGURATION (Assuming PrivacyConfig is defined elsewhere, e.g., in config.py)
# If PrivacyConfig is not a separate file, you'll need to define it here or inline its values.
# For this rewrite, I'll assume it's imported or its values are mocked for demonstration.
# If config.py exists, ensure it's in the same directory or accessible via PYTHONPATH.
class PrivacyConfig:
    MAX_FILE_SIZE = 5 # MB
    RISK_WEIGHTS = {
        "financial": 9.0,
        "government_id": 10.0,
        "contact_info": 7.0,
        "personal_identifier": 6.0,
        "location": 5.0,
        "date_time": 3.0,
        "technical_id": 4.0,
        "default": 1.0
    }
    # Add other configurations as needed based on your original config.py
    # Example:
    # PII_PATTERNS = { ... }
    # NER_LABELS = { ... }

# ====================
# TEXT PROCESSING UTILITIES
# ====================

class TextProcessor:
    """Advanced text processing and analysis utilities."""
    
    @staticmethod
    def extract_text_from_file(uploaded_file) -> str:
        """
        Extracts text content from various uploaded file formats.
        Supports: plain text, CSV, JSON, PDF.
        """
        try:
            file_type = uploaded_file.type
            if file_type == "text/plain":
                # Decode as UTF-8, ignoring errors for robustness
                return str(uploaded_file.read(), "utf-8", errors="ignore")
            elif file_type == "text/csv":
                # Read CSV into a DataFrame and convert to string representation
                df = pd.read_csv(uploaded_file)
                return df.to_string()
            elif file_type == "application/json":
                # Load JSON data and dump it as a formatted string
                data = json.load(uploaded_file)
                return json.dumps(data, indent=2)
            elif file_type == "application/pdf":
                # Use PyMuPDF (fitz) to extract text from PDF
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                return text
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Placeholder for DOCX. Requires python-docx or similar.
                # For simplicity, returning a warning. In a real app, integrate docx library.
                st.warning("DOCX file type detected. Text extraction for DOCX is not fully implemented in this demo.")
                return ""
            else:
                st.warning(f"Unsupported file type: {file_type}. Please upload TXT, CSV, JSON, or PDF.")
                return ""
        except Exception as e:
            st.error(f"Error reading file: {e}. Please ensure the file is valid and not corrupted.")
            return ""
    
    @staticmethod
    def calculate_text_metrics(text: str) -> Dict:
        """
        Calculates various metrics for the given text, such as character count,
        word count, line count, unique words, and a simple readability score.
        """
        words = text.split()
        # Filter out empty strings from words list if any
        words = [word for word in words if word.strip()] 
        
        # Count sentences by common punctuation marks
        sentences = len(re.split(r'[.!?]+', text)) -1 # -1 to account for trailing empty string
        if sentences < 0: sentences = 0 # Ensure non-negative sentence count

        return {
            'char_count': len(text),
            'word_count': len(words),
            'line_count': len(text.split('\n')),
            'unique_words': len(set(words)),
            'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
            'readability_score': TextProcessor._calculate_readability(text)
        }
    
    @staticmethod
    def _calculate_readability(text: str) -> float:
        """
        Calculates a simple readability score (e.g., Flesch-Kincaid style approximation).
        This is a simplified version for demonstration.
        """
        sentences = len(re.split(r'[.!?]+', text)) -1
        if sentences < 0: sentences = 0
        words = len(text.split())
        
        if sentences == 0 or words == 0:
            return 0.0 # Return 0 if no sentences or words to avoid division by zero
        
        # A very basic readability approximation
        avg_sentence_length = words / sentences
        # A simple formula, adjust as needed. Max/min to keep it within a reasonable range.
        return max(0.0, min(100.0, 206.835 - 1.015 * avg_sentence_length))


# ====================
# SIDEBAR AND UI FUNCTIONS
# ====================

def _render_sidebar():
    """
    Renders the Streamlit sidebar with input options and analysis settings.
    Returns the chosen input method and any associated data (e.g., uploaded file).
    """
    st.sidebar.header("🛡️ Privacy Guardian")

    # Display overall risk score in sidebar if results are available
    if st.session_state.current_results:
        results = st.session_state.current_results
        st.sidebar.metric(
            "Risk Score", 
            f"{results['scoring']['final_score']:.1f}/10",
            delta=f"{results['scoring']['risk_level'].upper()}",
            delta_color="inverse" # Invert color for delta (e.g., lower risk is good)
        )

    st.sidebar.subheader("📁 Input Options")

    # Radio buttons for choosing input method
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Text Input", "File Upload", "URL Analysis"],
        key="input_method_radio" # Added a key for stability
    )

    url = ""

    if input_method == "URL Analysis":
        url = st.sidebar.text_input("Enter URL to analyze:", key="sidebar_url_input")
        # A button here would trigger fetching, but the main app handles analysis trigger
        # if url and st.sidebar.button("Fetch & Analyze URL"):
        #     st.sidebar.info("URL analysis feature coming soon!")

    st.sidebar.subheader("🔧 Analysis Options")

    # Multiselect for detection methods
    detection_methods = st.sidebar.multiselect(
        "Detection Methods:",
        ["Regex Patterns", "Named Entity Recognition", "LLM Analysis"],
        default=["Regex Patterns", "Named Entity Recognition", "LLM Analysis"],
        key="detection_methods_multiselect"
    )

    # Slider for sensitivity threshold
    sensitivity_threshold = st.sidebar.slider(
        "Sensitivity Threshold:",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Lower values = more sensitive detection (may increase false positives)",
        key="sensitivity_threshold_slider"
    )

    # Expander for advanced options
    with st.sidebar.expander("⚡ Advanced Options"):
        enable_context_analysis = st.checkbox("Context Analysis", value=True, key="context_analysis_checkbox")
        enable_similarity_check = st.checkbox("Similarity Detection", value=False, key="similarity_similarity_check") # Changed key for uniqueness
        export_format = st.selectbox("Export Format:", ["JSON", "CSV", "PDF"], key="export_format_selectbox")

    # Display recent analyses from history
    if st.session_state.analysis_history:
        st.sidebar.subheader("📝 Recent Analyses")
        # Display up to the last 3 analyses
        for i, analysis in enumerate(st.session_state.analysis_history[-3:]):
            timestamp = analysis.get('timestamp', 'Unknown')
            risk_score = analysis.get('risk_score', 0)
            st.sidebar.write(f"🕒 {timestamp}: Risk {risk_score:.1f}")

    # Return the selected input method and its associated data
    # The uploaded_file is no longer passed from sidebar, it's handled in app.py
    if input_method == "Text Input":
        return "text", None
    elif input_method == "File Upload":
        return "file", None # No file object returned from sidebar anymore
    elif input_method == "URL Analysis":
        return "url", url
    # Default return if no method is selected or initial state
    return "text", None # Default to text input if nothing is explicitly chosen

def _render_analysis_tab(self):
    """
    Renders the content for the 'Analysis' tab in the main application area.
    This tab now primarily displays the analysis results.
    """
    # This function is now called when the "Analysis" tab is active in the bottom results section.
    # It should only display results, not input fields.
    if st.session_state.current_results:
        self._display_analysis_results(st.session_state.current_results) # Display results directly here
    else:
        st.info("No analysis results to display yet. Perform an analysis using the input options above.")


def _render_dashboard_tab(self):
    """
    Renders the content for the 'Dashboard' tab, providing a visual summary
    of the privacy analysis results.
    """
    st.subheader("📊 Risk Analysis Dashboard")
    
    if not st.session_state.current_results:
        st.info("👆 Perform an analysis first to see the dashboard.")
        return
    
    results = st.session_state.current_results
    
    # Display key metrics at the top of the dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = results['scoring']['final_score']
        st.metric(
            "Overall Risk Score",
            f"{score:.1f}/10",
            delta=results['scoring']['risk_level'].upper(),
            delta_color="inverse"
        )
    
    with col2:
        # Calculate total PII instances from regex and LLM detections
        pii_count = sum(data['count'] for data in results['regex'].values()) + len(results['llm'].get('entities', []))
        st.metric("Total PII Instances", pii_count)
    
    with col3:
        entity_count = len(results['ner'])
        st.metric("Named Entities Detected", entity_count)
    
    with col4:
        recommendations_count = len(results['scoring']['recommendations'])
        st.metric("Recommendations Provided", recommendations_count)
    
    # Use the visualizer to create a comprehensive risk dashboard
    self.visualizer.create_risk_dashboard(
        results['scoring'],
        results['regex'],
        results['ner'],
        results['llm']
    )
    
    # Display detected PII types and Named Entities in separate columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Detected PII Types (Categorized)")
        pii_data = []
        # Aggregate regex detection results
        for pattern_name, data in results['regex'].items():
            pii_data.append({
                'Type': data['description'],
                'Count': data['count'],
                'Weight': data['weight'],
                'Category': data['category']
            })
        # Aggregate LLM detection results
        for entity in results['llm'].get('entities', []):
            pii_data.append({
                'Type': entity['description'],
                'Count': 1, # Each LLM entity is a single instance
                'Weight': PrivacyConfig.RISK_WEIGHTS.get(entity['sensitivity'], 1.0),
                'Category': entity['sensitivity']
            })
        
        if pii_data:
            df_pii = pd.DataFrame(pii_data)
            # Display PII data as a sortable table
            st.dataframe(df_pii, use_container_width=True)
        else:
            st.info("No PII patterns detected by Regex or LLM in this analysis.")
    
    with col2:
        st.subheader("🏷️ Named Entities (NER)")
        if results['ner']:
            entity_data = []
            # Display top 10 named entities for brevity
            for entity in results['ner'][:10]:
                entity_data.append({
                    'Entity Text': entity['text'],
                    'Entity Type': entity['label'],
                    'Confidence': f"{entity['confidence']:.2f}",
                    'Sensitivity': entity['sensitivity']
                })
            
            df_entities = pd.DataFrame(entity_data)
            # Display named entities as a sortable table
            st.dataframe(df_entities, use_container_width=True)
        else:
            st.info("No named entities detected by NER in this analysis.")

def _render_trends_tab(self):
    """
    Renders the content for the 'Trends' tab, showing historical analysis data
    and overall trends in privacy risk.
    """
    st.subheader("📈 Privacy Risk Trends")
    
    if len(st.session_state.analysis_history) < 2:
        st.info("Perform at least two analyses to see trend data and analysis history.")
        return
    
    self.visualizer.create_trend_analysis(st.session_state.analysis_history)
    
    # Display summary statistics for historical analyses
    col1, col2, col3 = st.columns(3)
    
    scores = [analysis['risk_score'] for analysis in st.session_state.analysis_history]
    
    with col1:
        st.metric("Average Risk Score", f"{np.mean(scores):.1f}")
    
    with col2:
        st.metric("Highest Risk Score", f"{np.max(scores):.1f}")
    
    with col3:
        st.metric("Total Analyses Performed", len(st.session_state.analysis_history))
    
    st.subheader("📋 Analysis History")
    history_data = []
    # Prepare data for display in a DataFrame
    for analysis in st.session_state.analysis_history:
        history_data.append({
            'Timestamp': analysis['timestamp'],
            'Risk Score': f"{analysis['risk_score']:.1f}",
            'Risk Level': analysis['risk_level'],
            'PII Count': analysis.get('pii_count', 0),
            'Text Length': analysis.get('text_length', 0)
        })
    
    df_history = pd.DataFrame(history_data)
    # Display the analysis history as a sortable table
    st.dataframe(df_history, use_container_width=True)

def _render_settings_tab(self):
    """
    Renders the content for the 'Settings' tab, allowing users to configure
    detection parameters, export options, and manage data.
    """
    st.subheader("⚙️ System Settings")
    
    st.subheader("🔧 Detection Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Risk Weight Configuration**")
        new_weights = {}
        # Sliders to adjust risk weights for different categories
        for category, weight in PrivacyConfig.RISK_WEIGHTS.items():
            new_weights[category] = st.slider(
                f"{category.replace('_', ' ').title()}:",
                min_value=0.1,
                max_value=10.0,
                value=weight,
                step=0.1,
                key=f"weight_slider_{category}" # Unique key for each slider
            )
        # In a real application, you would save these new_weights to PrivacyConfig
        # For this demo, they are just displayed.
        st.info("Changes to risk weights are for display only in this demo. Implement persistence to save.")
    
    with col2:
        st.write("**Detection Thresholds**")
        confidence_threshold = st.slider(
            "Minimum Confidence for ML Detections:",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.05,
            key="confidence_threshold_slider"
        )
        context_window = st.slider(
            "Context Window Size (for context analysis):",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
            key="context_window_slider"
        )
    
    st.subheader("📤 Export Settings")
    export_options = st.multiselect(
        "Include in exports:",
        ["Raw detections", "Risk scores", "Recommendations", "Context", "Timestamps"],
        default=["Risk scores", "Recommendations"],
        key="export_options_multiselect"
    )
    
    st.subheader("ℹ️ System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Loaded Components:**")
        # Display status of various detection components
        st.write(f"• SpaCy NER: {'✅' if hasattr(self, 'ner_detector') and self.ner_detector.use_spacy else '❌'}")
        st.write(f"• Transformers (LLM): {'✅' if hasattr(self, 'llm_detector') and self.llm_detector.use_transformers else '❌'}")
        st.write(f"• Advanced Regex Patterns: ✅")
    
    with col2:
        st.write("**Performance Stats:**")
        st.write(f"• Analyses Performed: {len(st.session_state.analysis_history)}")
        st.write(f"• Avg Processing Time: ~2-5 seconds (estimate)")
        st.write(f"• Defined Pattern Count: {len(self.regex_detector.patterns) if hasattr(self, 'regex_detector') else 'N/A'}")
    
    st.subheader("🗑️ Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        # Button to clear all analysis history
        if st.button("Clear Analysis History", key="clear_history_button"):
            st.session_state.analysis_history = []
            st.session_state.current_results = None # Also clear current results
            st.session_state.analysis_ran = False # Reset auto-analysis flag
            st.success("Analysis history and current results cleared!")
            st.rerun() # Rerun to update the UI
    
    with col2:
        # Button to reset only the current analysis results
        if st.button("Reset Current Results", key="reset_current_button"):
            st.session_state.current_results = None
            st.session_state.analysis_ran = False # Reset auto-analysis flag
            st.success("Current results cleared!")
            st.rerun() # Rerun to update the UI

def _perform_analysis(self, text: str) -> Dict:
    """
    Performs a comprehensive privacy analysis on the given text using
    regex, NER, and LLM detectors, then calculates a final risk score.
    """
    # Calculate text metrics first
    text_metrics = TextProcessor.calculate_text_metrics(text)
    
    # Perform detections using different methods
    regex_results = self.regex_detector.detect(text)
    ner_results = self.ner_detector.detect(text)
    llm_results = self.llm_detector.detect(text)
    
    # Calculate the comprehensive risk score based on all detection results
    scoring_results = self.scoring_engine.calculate_comprehensive_score(
        regex_results, ner_results, llm_results, text_metrics
    )
    
    # Return a dictionary containing all analysis outputs
    return {
        'text_metrics': text_metrics,
        'regex': regex_results,
        'ner': ner_results,
        'llm': llm_results,
        'scoring': scoring_results,
        'timestamp': datetime.now().isoformat() # Timestamp for when the analysis was performed
    }

def _display_analysis_results(self, results: Dict):
    """
    Displays the comprehensive analysis results in a user-friendly format,
    including overall risk, component scores, detected patterns, and recommendations.
    """
    st.subheader("📊 Analysis Summary")
    score = results['scoring']['final_score']
    risk_level = results['scoring']['risk_level']
    
    # Define a color map for different risk levels for visual emphasis
    risk_color_map = {
        'low': 'green',
        'medium': 'orange',
        'high': 'red',
        'critical': 'darkred'
    }
    
    # Display overall risk score and level using custom markdown for styling
    st.markdown(f"""
    <div class="metric-card risk-{risk_level}">
        <h3>🎯 Overall Risk Score: {score:.1f}/10</h3>
        <p><strong>Risk Level:</strong> <span style="color: {risk_color_map[risk_level]}; text-transform: uppercase; font-weight: bold;">{risk_level}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📈 Component Analysis & Text Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Detection Components Scores:**")
        # Display scores from each detection component
        for component, comp_score in results['scoring']['component_scores'].items():
            st.write(f"• **{component.replace('_', ' ').title()}:** {comp_score:.1f}/10")
    
    with col2:
        st.write("**Text Metrics:**")
        metrics = results['text_metrics']
        # Display various text-related metrics
        st.write(f"• **Characters:** {metrics['char_count']:,}")
        st.write(f"• **Words:** {metrics['word_count']:,}")
        st.write(f"• **Unique words:** {metrics['unique_words']:,}")
        st.write(f"• **Lines:** {metrics['line_count']:,}")
        st.write(f"• **Avg. Word Length:** {metrics['avg_word_length']:.2f}")
        st.write(f"• **Readability Score:** {metrics['readability_score']:.1f}")
    
    # Display detected PII patterns from Regex
    if results['regex']:
        st.subheader("🔍 Detected PII Patterns (Regex)")
        for pattern_name, data in results['regex'].items():
            # Use expanders to show details for each pattern type
            with st.expander(f"**{data['description']}** ({data['count']} found)"):
                st.write(f"**Risk Weight:** {data['weight']}")
                st.write(f"**Category:** {data['category']}")
                # Display up to 3 matches for brevity, with value and context
                for i, match in enumerate(data['matches'][:3]):
                    st.write(f"**Match {i+1}:**")
                    st.code(f"Value: {match['value']}")
                    st.write(f"Confidence: {match['confidence']:.2f}")
                    st.write(f"Context: ...{match['context']}...")
                    st.markdown("---") # Separator between matches
                if len(data['matches']) > 3:
                    st.info(f"And {len(data['matches']) - 3} more matches...")
    
    if results['llm'].get('entities'):
        st.subheader("🤖 ML-Detected PII (LLM/RoBERTa)")
        for i, entity in enumerate(results['llm']['entities'][:3]):
            # Use expanders for each ML-detected entity
            with st.expander(f"**{entity['description']}** (Type: {entity['label']})"):
                st.write(f"**Text:** {entity['text']}")
                st.write(f"**Type:** {entity['label']}")
                st.write(f"**Confidence:** {entity['confidence']:.2f}")
                st.write(f"**Sensitivity:** {entity['sensitivity']}")
                st.markdown("---")
        if len(results['llm']['entities']) > 3:
            st.info(f"And {len(results['llm']['entities']) - 3} more ML-detected entities...")
    
    st.subheader("💡 Recommendations")
    if results['scoring']['recommendations']:
        # List out privacy recommendations
        for i, recommendation in enumerate(results['scoring']['recommendations']):
            st.write(f"{i+1}. {recommendation}")
    else:
        st.info("No specific recommendations generated for this analysis. The text appears to have low privacy risk.")
    
    st.subheader("📤 Export Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Button to download results as JSON
        if st.button("📄 Export as JSON", use_container_width=True):
            json_data = json.dumps(results, indent=2, default=str) # Use default=str for datetime objects
            st.download_button(
                "Download JSON",
                json_data,
                "privacy_analysis.json",
                "application/json",
                key="download_json_button"
            )
    
    with col2:
        # Button to download a summary as CSV
        if st.button("📊 Export as CSV", use_container_width=True):
            summary_data = {
                'Metric': ['Risk Score', 'Risk Level', 'PII Patterns (Regex)', 'ML Entities (LLM)', 'Named Entities (NER)'],
                'Value': [
                    results['scoring']['final_score'],
                    results['scoring']['risk_level'],
                    len(results['regex']),
                    len(results['llm'].get('entities', [])),
                    len(results['ner'])
                ]
            }
            df = pd.DataFrame(summary_data)
            csv_data = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv_data,
                "privacy_summary.csv",
                "text/csv",
                key="download_csv_button"
            )
    
    with col3:
        # Button to copy a summary to clipboard (simulated with st.code)
        if st.button("📋 Copy Summary", use_container_width=True):
            summary = f"""
            Privacy Analysis Summary
            Risk Score: {score:.1f}/10 ({risk_level.upper()})
            PII Patterns (Regex): {len(results['regex'])}
            ML Entities (LLM): {len(results['llm'].get('entities', []))}
            Named Entities (NER): {len(results['ner'])}
            Text Length: {results['text_metrics']['char_count']} chars
            Analysis Time: {results['timestamp']}
            """.strip()
            st.code(summary, language="text") # Display summary in a code block for easy copying
            st.success("Summary copied to clipboard (displayed above for manual copy).")


def _add_to_history(self, text: str, results: Dict):
    """
    Adds the current analysis entry to the session state history list.
    This history is used for the 'Trends' tab.
    """
    analysis_entry = {
        'timestamp': results['timestamp'],
        'risk_score': results['scoring']['final_score'],
        'risk_level': results['scoring']['risk_level'],
        'pii_count': sum(data['count'] for data in results['regex'].values()) + len(results['llm'].get('entities', [])),
        'text_length': results['text_metrics']['char_count']
    }
    st.session_state.analysis_history.append(analysis_entry)