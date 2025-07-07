# import streamlit as st
# import urllib.parse
# from enhanced_regex import EnhancedRegexDetector
# from advanced_ner import AdvancedNERDetector
# from advanced_llm import AdvancedLLMDetector
# from scoring_engine import AdvancedScoringEngine
# from visualizer import PrivacyVisualizer
# # Import all necessary functions and the TextProcessor class from sidebar.py
# from sidebar import _render_sidebar, _render_analysis_tab, _render_dashboard_tab, _render_trends_tab, _render_settings_tab, _perform_analysis, _display_analysis_results, _add_to_history, TextProcessor
# from typing import List, Dict

# # Core ML/NLP imports - keep these as they are, assuming they are handled by the environment
# try:
#     from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
#     import spacy
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn.metrics.pairwise import cosine_similarity
#     import torch
# except ImportError as e:
#     st.error(f"Required packages not installed: {e}")

# # ====================
# # MAIN APPLICATION
# # ====================
# class AdvancedPrivacyDetector:
#     """Main application class for the Privacy Guardian."""

#     def __init__(self):
#         # Initialize core detection and scoring components
#         self.regex_detector = EnhancedRegexDetector()
#         self.ner_detector = AdvancedNERDetector()
#         self.llm_detector = AdvancedLLMDetector()
#         self.scoring_engine = AdvancedScoringEngine()
#         self.visualizer = PrivacyVisualizer()

#         # Initialize Streamlit session state variables if they don't exist
#         if 'analysis_history' not in st.session_state:
#             st.session_state.analysis_history = []
#         if 'current_results' not in st.session_state:
#             st.session_state.current_results = None
#         if 'analysis_ran' not in st.session_state:
#             st.session_state.analysis_ran = False # To track if auto-analysis has run
#         if 'uploaded_file_content' not in st.session_state:
#             st.session_state.uploaded_file_content = ""
#         if 'last_uploaded_file_id' not in st.session_state:
#             st.session_state.last_uploaded_file_id = None
#         if 'active_tab' not in st.session_state:
#             st.session_state.active_tab = "Analysis" # Default active tab


#     # These methods are wrappers to call functions defined in sidebar.py
#     # This structure keeps the main app logic cleaner and delegates UI rendering
#     # and analysis execution to the appropriate modules.
#     def _render_sidebar(self):
#         """Renders the application sidebar and returns user input choices."""
#         return _render_sidebar()

#     def _render_analysis_tab(self):
#         """Renders the Analysis tab content."""
#         return _render_analysis_tab(self)

#     def _render_dashboard_tab(self):
#         """Renders the Dashboard tab content."""
#         return _render_dashboard_tab(self)

#     def _render_trends_tab(self):
#         """Renders the Trends tab content."""
#         return _render_trends_tab(self)

#     def _render_settings_tab(self):
#         """Renders the Settings tab content."""
#         return _render_settings_tab(self)

#     def _perform_analysis(self, text: str) -> Dict:
#         """Performs the comprehensive privacy analysis on the given text."""
#         return _perform_analysis(self, text)

#     def _display_analysis_results(self, results: Dict):
#         """Displays the detailed analysis results."""
#         return _display_analysis_results(self, results)

#     def _add_to_history(self, text: str, results: Dict):
#         """Adds the current analysis results to the history."""
#         return _add_to_history(self, text, results)

#     def run(self):
#         """Main method to run the Streamlit application."""
#         st.set_page_config(
#             page_title="Advanced Privacy Guardian",
#             page_icon="🛡️",
#             layout="wide",
#             initial_sidebar_state="expanded"
#         )
        
#         # Custom CSS for enhanced visual aesthetics (Green and Black theme)
#         st.markdown("""
#         <style>
#             /* General styling for the main application background */
#             .stApp {
#                 background-color: #1a1a1a; /* Dark background */
#                 color: #e0e0e0; /* Light text for contrast */
#                 font-family: 'Inter', sans-serif;
#                 padding-top: 20px;
#             }
#             /* Styling for the main header */
#             .main-header {
#                 font-size: 2.5em;
#                 font-weight: bold;
#                 color: #4CAF50; /* Green for branding */
#                 text-align: center;
#                 padding: 20px;
#                 background-color: #2c2c2c; /* Slightly lighter dark background for header */
#                 border-radius: 10px;
#                 margin-bottom: 30px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* More prominent shadow */
#             }
#             /* Styling for subheaders */
#             h1, h2, h3, h4, h5, h6 {
#                 color: #4CAF50; /* Green for section titles */
#             }
#             /* Styling for primary buttons */
#             .stButton>button {
#                 background-color: #4CAF50; /* Green button */
#                 color: white;
#                 border-radius: 8px;
#                 padding: 10px 20px;
#                 font-size: 1em;
#                 transition: all 0.3s ease; /* Smooth transition for hover effects */
#                 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); /* Darker shadow for buttons */
#                 border: none; /* No border for a cleaner look */
#             }
#             .stButton>button:hover {
#                 background-color: #45a049; /* Darker green on hover */
#                 transform: translateY(-2px); /* Slight lift effect */
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); /* Enhanced shadow on hover */
#             }
#             /* Styling for metric cards (e.g., Overall Risk Score) */
#             .metric-card {
#                 background-color: #2c2c2c; /* Dark background for cards */
#                 border-radius: 10px;
#                 padding: 20px;
#                 margin-bottom: 20px;
#                 box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
#                 border-left: 5px solid; /* Colored border for risk level indication */
#             }
#             /* Specific border colors for different risk levels */
#             .risk-low { border-left-color: #4CAF50; } /* Green */
#             .risk-medium { border-left-color: #FFC107; } /* Amber */
#             .risk-high { border-left-color: #FF5722; } /* Deep Orange */
#             .risk-critical { border-left-color: #D32F2F; } /* Red */
#             /* Styling for tab headers */
#             .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
#                 font-size: 1.1em;
#                 font-weight: bold;
#                 color: #e0e0e0; /* Light text for tabs */
#             }
#             .stTabs [data-baseweb="tab-list"] button {
#                 background-color: #2c2c2c; /* Darker tab background */
#                 border-radius: 8px 8px 0 0; /* Rounded top corners */
#                 margin-right: 5px;
#             }
#             .stTabs [data-baseweb="tab-list"] button:hover {
#                 background-color: #3a3a3a; /* Lighter on hover */
#             }
#             .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
#                 background-color: #4CAF50; /* Green for selected tab */
#                 color: white;
#             }
#             /* Adjust sidebar width */
#             section[data-testid="stSidebar"] {
#                 width: 350px !important;
#                 background-color: #0d0d0d; /* Even darker sidebar */
#                 color: #e0e0e0;
#             }
#             /* Styling for text areas and file uploaders */
#             .stTextArea textarea, .stFileUploader label {
#                 background-color: #2c2c2c; /* Dark input fields */
#                 color: #e0e0e0;
#                 border-radius: 8px;
#                 border: 1px solid #4CAF50; /* Green border */
#             }
#             .stTextArea label, .stFileUploader label {
#                 color: #e0e0e0; /* Label color */
#             }
#             /* Info/Warning messages */
#             .stAlert {
#                 border-radius: 8px;
#             }
#             .stAlert.info {
#                 background-color: #2c2c2c;
#                 color: #81D4FA; /* Light blue for info */
#                 border-left: 5px solid #81D4FA;
#             }
#             .stAlert.warning {
#                 background-color: #2c2c2c;
#                 color: #FFD54F; /* Amber for warning */
#                 border-left: 5px solid #FFD54F;
#             }
#             .stAlert.success {
#                 background-color: #2c2c2c;
#                 color: #A5D6A7; /* Light green for success */
#                 border-left: 5px solid #A5D6A7;
#             }
#             /* Custom styling for the main header with icon and AI-Powered text */
#             .custom-header {
#                 display: flex;
#                 align-items: center;
#                 justify-content: center;
#                 gap: 15px;
#                 font-size: 2.5em;
#                 font-weight: bold;
#                 color: #e0e0e0; /* White text */
#                 background: linear-gradient(45deg, #1a1a1a, #4CAF50); /* Gradient background */
#                 padding: 25px 0;
#                 border-radius: 15px;
#                 margin-bottom: 30px;
#                 box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
#                 position: relative;
#                 overflow: hidden;
#             }
#             .custom-header::before {
#                 content: '';
#                 position: absolute;
#                 top: -50%;
#                 left: -50%;
#                 width: 200%;
#                 height: 200%;
#                 background: radial-gradient(circle, rgba(76,175,80,0.2) 0%, rgba(26,26,26,0) 70%);
#                 transform: rotate(45deg);
#                 opacity: 0.7;
#             }
#             .custom-header .icon {
#                 font-size: 1.2em;
#                 color: white; /* White icon */
#                 text-shadow: 0 0 10px #4CAF50; /* Green glow */
#             }
#             .custom-header .subtitle {
#                 font-size: 0.4em;
#                 font-weight: normal;
#                 color: #c0c0c0; /* Lighter grey for subtitle */
#                 margin-top: -10px; /* Pull subtitle closer to main title */
#                 display: block; /* Ensure subtitle is on a new line */
#             }
#         </style>
#         """, unsafe_allow_html=True)
        
#         # Main Header with icon and subtitle
#         st.markdown("""
#         <div class="custom-header">
#             <span class="icon">🛡️</span>
#             <div>
#                 Advanced Privacy Text Detector
#                 <span class="subtitle">AI-Powered Privacy Risk Detection & Analysis System</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Handle preloaded text from browser extension (via ?q=...)
#         query_params = st.query_params
#         if "q" in query_params:
#             preloaded_text = urllib.parse.unquote(query_params["q"])
#             st.session_state["preloaded_text"] = preloaded_text

#         # Render the sidebar and get the selected input type
#         sidebar_input_type, _ = self._render_sidebar()

#         # Tabs are always rendered at the top of the main content area
#         # We use a callback to update session_state.active_tab when a tab is clicked
#         # Note: st.tabs itself manages the active tab visually.
#         # We ensure 'Analysis' tab is selected when analysis runs.
#         tab_titles = ["🔍 Analysis", "📊 Dashboard", "📈 Trends", "⚙️ Settings"]
#         tab_objects = st.tabs(tab_titles)

#         # Divide the main content area into two columns: one for input/analysis, one for quick info
#         main_input_col, quick_info_col = st.columns([3, 1])

#         with main_input_col:
#             st.subheader("📝 Input Data") # Changed from "Text Analysis" to "Input Data"

#             user_text = "" # Initialize user_text
#             uploaded_file_main = None # Initialize uploaded_file_main

#             if sidebar_input_type == "text":
#                 # Always display the text area for manual input when 'Text Input' is selected
#                 preloaded = st.session_state.get("preloaded_text", "")
#                 user_text = st.text_area(
#                     "🔐 Enter Text to Analyze:",
#                     value=preloaded,
#                     height=300,
#                     key="main_text_input", # Unique key for stability
#                     placeholder="Paste your text here for privacy risk analysis...",
#                     help="Enter any text content you want to analyze for privacy risks"
#                 )
#                 if st.button("🔍 Analyze Text", type="primary", use_container_width=True, key="analyze_text_button"):
#                     if user_text.strip():
#                         with st.spinner("Analyzing text for privacy risks..."):
#                             results = self._perform_analysis(user_text)
#                             st.session_state.current_results = results
#                             self._add_to_history(user_text, results)
#                             st.success("✅ Analysis complete!")
#                         st.session_state.active_tab = "Analysis" # Switch to Analysis tab after analysis
#                         st.rerun() # Rerun to display results in tabs immediately
#                     else:
#                         st.warning("⚠️ Please enter some text to analyze.")

#             elif sidebar_input_type == "file":
#                 # Only display the file uploader when 'File Upload' is selected
#                 uploaded_file_main = st.file_uploader(
#                     "📄 Upload PDF/Text File",
#                     type=['txt', 'csv', 'json', 'pdf', 'docx'],
#                     help="Drag and drop file here or click to browse. Supported formats: TXT, CSV, JSON, PDF, DOCX. Limit 200MB per file.",
#                     key="main_file_uploader" # Unique key for stability
#                 )

#                 # Process uploaded file immediately if it changes
#                 if uploaded_file_main is not None:
#                     # Check if the uploaded file is new or different from the one currently in session_state
#                     if 'last_uploaded_file_id' not in st.session_state or st.session_state.last_uploaded_file_id != uploaded_file_main.file_id:
#                         try:
#                             file_content = TextProcessor.extract_text_from_file(uploaded_file_main)
#                             st.session_state.uploaded_file_content = file_content
#                             st.session_state.last_uploaded_file_id = uploaded_file_main.file_id
#                             st.success(f"File '{uploaded_file_main.name}' loaded successfully!")
#                         except Exception as e:
#                             st.error(f"Error reading uploaded file: {e}")
#                             st.session_state.uploaded_file_content = ""
#                             st.session_state.last_uploaded_file_id = None # Reset ID on error
#                 elif uploaded_file_main is None and 'last_uploaded_file_id' in st.session_state and st.session_state.last_uploaded_file_id is not None:
#                     # If uploader is cleared, clear session state content
#                     st.session_state.uploaded_file_content = ""
#                     st.session_state.last_uploaded_file_id = None
#                     st.info("File upload cleared.")

#                 # Display extracted text if available (from a file upload)
#                 if st.session_state.uploaded_file_content:
#                     st.text_area("📖 Extracted Text Preview:", value=st.session_state.uploaded_file_content, height=200, disabled=True, key="extracted_file_preview")
                
#                 if st.session_state.uploaded_file_content: # Check if content was extracted from a file
#                     if st.button("🔍 Analyze Uploaded File", type="primary", use_container_width=True, key="analyze_file_button"):
#                         with st.spinner("Analyzing file for privacy risks..."):
#                             results = self._perform_analysis(st.session_state.uploaded_file_content)
#                             st.session_state.current_results = results
#                             self._add_to_history(st.session_state.uploaded_file_content, results)
#                             st.success("✅ File analysis complete!")
#                         st.session_state.active_tab = "Analysis" # Switch to Analysis tab after analysis
#                         st.rerun() # Rerun to display results in tabs immediately
#                 else:
#                     st.info("⬆️ Please upload a file to enable analysis.")

#             elif sidebar_input_type == "url":
#                 st.warning("🌐 URL analysis feature coming soon! Please use Text Input or File Upload for now.")
#                 url_input_main = st.text_input("Enter URL to analyze:", key="main_url_input")
#                 if st.button("Fetch & Analyze URL (Main)", type="secondary", use_container_width=True, key="analyze_url_button_main"):
#                     st.info("URL analysis is not yet implemented.")


#             # Auto-analyze if extension text was passed and analysis hasn't run yet
#             if st.session_state.get("preloaded_text") and st.session_state.get("analysis_ran") is not True:
#                 # Ensure the input method is set to "Text Input" for preloaded text
#                 # to make the "Analyze Text" button active implicitly.
#                 st.session_state["input_method_radio"] = "Text Input"
#                 with st.spinner("Analyzing preloaded text..."):
#                     results = self._perform_analysis(st.session_state["preloaded_text"])
#                     st.session_state.current_results = results
#                     st.session_state.analysis_ran = True # Mark analysis as run
#                     self._add_to_history(st.session_state["preloaded_text"], results)
#                     st.success("✅ Auto-analysis complete!")
#                 st.session_state.active_tab = "Analysis" # Switch to Analysis tab after auto-analysis
#                 st.rerun() # Rerun to display results in tabs immediately


#         with quick_info_col:
#             st.subheader("📋 Quick Info")
#             with st.expander("📖 Analysis Guide", expanded=True):
#                 st.markdown("""
#                 This tool helps detect sensitive information.
#                 **What we detect:**
#                 - 🆔 **Government IDs:** Social Security Numbers (SSN, Aadhaar, PAN)
#                 - 💳 **Financial Data:** Credit Card Numbers, Bank Account Numbers (IBAN)
#                 - 📞 **Contact Info:** Email Addresses, Phone Numbers, IP Addresses
#                 - 👤 **Personal Identifiers:** Names, Dates of Birth, Gender
#                 - 🏠 **Addresses & Locations:** Street Addresses, Cities, Countries
#                 - 🌐 **Technical Identifiers:** MAC Addresses, API Keys (if configured)

#                 **Risk Levels:**
#                 - 🟢 **Low (0-3)**: Minimal privacy risk, generally safe to share.
#                 - 🟡 **Medium (3-6)**: Moderate attention needed, review before sharing.  
#                 - 🟠 **High (6-8)**: Significant risk present, strong caution advised.
#                 - 🔴 **Critical (8-10)**: Immediate action required, highly sensitive data.
#                 """)
#             with st.expander("🧪 Sample Texts"):
#                 st.markdown("Click a button to load a sample text into the main input area.")
#                 # Use st.session_state to pass sample text to the main input area
#                 if st.button("📞 Contact Info Sample", key="sample_contact_main"):
#                     st.session_state["preloaded_text"] = """
#                     Contact Information:
#                     Email: john.doe@company.com
#                     Phone: +1-555-123-4567
#                     Address: 123 Main St, Anytown, ST 12345
#                     Date of Birth: 1985-03-15
#                     """
#                     st.session_state["input_method_radio"] = "Text Input" # Set input method for sample
#                     st.rerun() # Rerun to update the main text area
#                 if st.button("🆔 ID Numbers Sample", key="sample_id_main"):
#                     st.session_state["preloaded_text"] = """
#                     Personal Details:
#                     SSN: 123-45-6789
#                     Credit Card: 4532 1234 5678 9012
#                     Phone: 9876543210
#                     Aadhaar: 1234 5678 9012
#                     """
#                     st.session_state["input_method_radio"] = "Text Input" # Set input method for sample
#                     st.rerun() # Rerun to update the main text area
#                 if st.button("🌐 Mixed Data Sample", key="sample_mixed_main"):
#                     st.session_state["preloaded_text"] = """
#                     Meeting notes for Project X. Attendees: Jane Doe (jane.doe@example.com), John Smith (phone: 555-987-6543). 
#                     Discussion about financial report from Q3 2024. Account number: GB33BUKB20201555555555. 
#                     The server IP address is 192.168.1.100.
#                     """
#                     st.session_state["input_method_radio"] = "Text Input" # Set input method for sample
#                     st.rerun() # Rerun to update the main text area

#         # IMPORTANT: Analysis Results section at the very bottom
#         # This section will only display if there are current results.
#         # The content will be drawn from the selected tab.
#         if st.session_state.current_results:
#             st.markdown("---") # Separator before results
#             st.subheader("Results") # Header for the results section
            
#             # This is where the content of the selected tab will be displayed
#             # We use a placeholder for the content to be displayed below the input section
#             # The actual content rendering is handled by the _render_*_tab functions
#             # based on the active tab in session state.
            
#             # We need to determine which tab object corresponds to the active tab in session state
#             # and then use a 'with' block for that tab.
#             # However, st.tabs() itself returns the *currently selected* tab object.
#             # To avoid re-rendering all tabs, and just render the content of the active tab at the bottom,
#             # we simply check st.session_state.active_tab and call the corresponding function.
            
#             if st.session_state.active_tab == "🔍 Analysis":
#                 self._render_analysis_tab()
#             elif st.session_state.active_tab == "📊 Dashboard":
#                 self._render_dashboard_tab()
#             elif st.session_state.active_tab == "📈 Trends":
#                 self._render_trends_tab()
#             elif st.session_state.active_tab == "⚙️ Settings":
#                 self._render_settings_tab()
#             else:
#                 # This case should ideally not be hit if active_tab is always one of the above.
#                 # It's a fallback.
#                 st.info("Select a tab above to view the analysis details.")

# # ====================
# # APPLICATION ENTRY POINT
# # ====================

# def main():
#     """Main application entry point."""
#     try:
#         app = AdvancedPrivacyDetector()
#         app.run()
#     except Exception as e:
#         st.error(f"Application error: {e}")
#         st.write("Please refresh the page or contact support.")

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import urllib.parse
# from enhanced_regex import EnhancedRegexDetector
# from advanced_ner import AdvancedNERDetector
# from advanced_llm import AdvancedLLMDetector
# from scoring_engine import AdvancedScoringEngine
# from visualizer import PrivacyVisualizer
# # Import all necessary functions and the TextProcessor class from sidebar.py
# from sidebar import _render_sidebar, _render_analysis_tab, _render_dashboard_tab, _render_trends_tab, _render_settings_tab, _perform_analysis, _display_analysis_results, _add_to_history, TextProcessor
# from typing import List, Dict

# # Core ML/NLP imports - keep these as they are, assuming they are handled by the environment
# try:
#     from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
#     import spacy
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn.metrics.pairwise import cosine_similarity
#     import torch
# except ImportError as e:
#     st.error(f"Required packages not installed: {e}")

# # ====================
# # MAIN APPLICATION
# # ====================
# class AdvancedPrivacyDetector:
#     """Main application class for the Privacy Guardian."""

#     def __init__(self):
#         # Initialize core detection and scoring components
#         self.regex_detector = EnhancedRegexDetector()
#         self.ner_detector = AdvancedNERDetector()
#         self.llm_detector = AdvancedLLMDetector()
#         self.scoring_engine = AdvancedScoringEngine()
#         self.visualizer = PrivacyVisualizer()

#         # Initialize Streamlit session state variables if they don't exist
#         if 'analysis_history' not in st.session_state:
#             st.session_state.analysis_history = []
#         if 'current_results' not in st.session_state:
#             st.session_state.current_results = None
#         if 'analysis_ran' not in st.session_state:
#             st.session_state.analysis_ran = False # To track if auto-analysis has run
#         if 'uploaded_file_content' not in st.session_state:
#             st.session_state.uploaded_file_content = ""
#         if 'last_uploaded_file_id' not in st.session_state:
#             st.session_state.last_uploaded_file_id = None
#         # Use active_tab_name to store the name of the currently selected tab
#         if 'active_tab_name' not in st.session_state:
#             st.session_state.active_tab_name = "🔍 Analysis" # Default active tab name


#     # These methods are wrappers to call functions defined in sidebar.py
#     # This structure keeps the main app logic cleaner and delegates UI rendering
#     # and analysis execution to the appropriate modules.
#     def _render_sidebar(self):
#         """Renders the application sidebar and returns user input choices."""
#         return _render_sidebar()

#     def _render_analysis_tab(self):
#         """Renders the Analysis tab content."""
#         return _render_analysis_tab(self)

#     def _render_dashboard_tab(self):
#         """Renders the Dashboard tab content."""
#         return _render_dashboard_tab(self)

#     def _render_trends_tab(self):
#         """Renders the Trends tab content."""
#         return _render_trends_tab(self)

#     def _render_settings_tab(self):
#         """Renders the Settings tab content."""
#         return _render_settings_tab(self)

#     def _perform_analysis(self, text: str) -> Dict:
#         """Performs the comprehensive privacy analysis on the given text."""
#         return _perform_analysis(self, text)

#     def _display_analysis_results(self, results: Dict):
#         """Displays the detailed analysis results."""
#         return _display_analysis_results(self, results)

#     def _add_to_history(self, text: str, results: Dict):
#         """Adds the current analysis results to the history."""
#         return _add_to_history(self, text, results)

#     def run(self):
#         """Main method to run the Streamlit application."""
#         st.set_page_config(
#             page_title="Advanced Privacy Guardian",
#             page_icon="🛡️",
#             layout="wide",
#             initial_sidebar_state="expanded"
#         )
        
#         # Custom CSS for enhanced visual aesthetics (Green and Black theme)
#         st.markdown("""
#         <style>
#             /* General styling for the main application background */
#             .stApp {
#                 background-color: #1a1a1a; /* Dark background */
#                 color: #e0e0e0; /* Light text for contrast */
#                 font-family: 'Inter', sans-serif;
#                 padding-top: 20px;
#             }
#             /* Styling for the main header */
#             .main-header {
#                 font-size: 2.5em;
#                 font-weight: bold;
#                 color: #4CAF50; /* Green for branding */
#                 text-align: center;
#                 padding: 20px;
#                 background-color: #2c2c2c; /* Slightly lighter dark background for header */
#                 border-radius: 10px;
#                 margin-bottom: 30px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* More prominent shadow */
#             }
#             /* Styling for subheaders */
#             h1, h2, h3, h4, h5, h6 {
#                 color: #4CAF50; /* Green for section titles */
#             }
#             /* Styling for primary buttons */
#             .stButton>button {
#                 background-color: #4CAF50; /* Green button */
#                 color: white;
#                 border-radius: 8px;
#                 padding: 10px 20px;
#                 font-size: 1em;
#                 transition: all 0.3s ease; /* Smooth transition for hover effects */
#                 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); /* Darker shadow for buttons */
#                 border: none; /* No border for a cleaner look */
#             }
#             .stButton>button:hover {
#                 background-color: #45a049; /* Darker green on hover */
#                 transform: translateY(-2px); /* Slight lift effect */
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); /* Enhanced shadow on hover */
#             }
#             /* Styling for metric cards (e.g., Overall Risk Score) */
#             .metric-card {
#                 background-color: #2c2c2c; /* Dark background for cards */
#                 border-radius: 10px;
#                 padding: 20px;
#                 margin-bottom: 20px;
#                 box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
#                 border-left: 5px solid; /* Colored border for risk level indication */
#             }
#             /* Specific border colors for different risk levels */
#             .risk-low { border-left-color: #4CAF50; } /* Green */
#             .risk-medium { border-left-color: #FFC107; } /* Amber */
#             .risk-high { border-left-color: #FF5722; } /* Deep Orange */
#             .risk-critical { border-left-color: #D32F2F; } /* Red */
#             /* Styling for tab headers */
#             .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
#                 font-size: 1.1em;
#                 font-weight: bold;
#                 color: #e0e0e0; /* Light text for tabs */
#             }
#             .stTabs [data-baseweb="tab-list"] button {
#                 background-color: #2c2c2c; /* Darker tab background */
#                 border-radius: 8px 8px 0 0; /* Rounded top corners */
#                 margin-right: 5px;
#             }
#             .stTabs [data-baseweb="tab-list"] button:hover {
#                 background-color: #3a3a3a; /* Lighter on hover */
#             }
#             .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
#                 background-color: #4CAF50; /* Green for selected tab */
#                 color: white;
#             }
#             /* Adjust sidebar width */
#             section[data-testid="stSidebar"] {
#                 width: 350px !important;
#                 background-color: #0d0d0d; /* Even darker sidebar */
#                 color: #e0e0e0;
#             }
#             /* Styling for text areas and file uploaders */
#             .stTextArea textarea, .stFileUploader label {
#                 background-color: #2c2c2c; /* Dark input fields */
#                 color: #e0e0e0;
#                 border-radius: 8px;
#                 border: 1px solid #4CAF50; /* Green border */
#             }
#             .stTextArea label, .stFileUploader label {
#                 color: #e0e0e0; /* Label color */
#             }
#             /* Info/Warning messages */
#             .stAlert {
#                 border-radius: 8px;
#             }
#             .stAlert.info {
#                 background-color: #2c2c2c;
#                 color: #81D4FA; /* Light blue for info */
#                 border-left: 5px solid #81D4FA;
#             }
#             .stAlert.warning {
#                 background-color: #2c2c2c;
#                 color: #FFD54F; /* Amber for warning */
#                 border-left: 5px solid #FFD54F;
#             }
#             .stAlert.success {
#                 background-color: #2c2c2c;
#                 color: #A5D6A7; /* Light green for success */
#                 border-left: 5px solid #A5D6A7;
#             }
#             /* Custom styling for the main header with icon and AI-Powered text */
#             .custom-header {
#                 display: flex;
#                 align-items: center;
#                 justify-content: center;
#                 gap: 15px;
#                 font-size: 2.5em;
#                 font-weight: bold;
#                 color: #e0e0e0; /* White text */
#                 background: linear-gradient(45deg, #1a1a1a, #4CAF50); /* Gradient background */
#                 padding: 25px 0;
#                 border-radius: 15px;
#                 margin-bottom: 30px;
#                 box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
#                 position: relative;
#                 overflow: hidden;
#             }
#             .custom-header::before {
#                 content: '';
#                 position: absolute;
#                 top: -50%;
#                 left: -50%;
#                 width: 200%;
#                 height: 200%;
#                 background: radial-gradient(circle, rgba(76,175,80,0.2) 0%, rgba(26,26,26,0) 70%);
#                 transform: rotate(45deg);
#                 opacity: 0.7;
#             }
#             .custom-header .icon {
#                 font-size: 1.2em;
#                 color: white; /* White icon */
#                 text-shadow: 0 0 10px #4CAF50; /* Green glow */
#             }
#             .custom-header .subtitle {
#                 font-size: 0.4em;
#                 font-weight: normal;
#                 color: #c0c0c0; /* Lighter grey for subtitle */
#                 margin-top: -10px; /* Pull subtitle closer to main title */
#                 display: block; /* Ensure subtitle is on a new line */
#             }
#         </style>
#         """, unsafe_allow_html=True)
        
#         # Main Header with icon and subtitle
#         st.markdown("""
#         <div class="custom-header">
#             <span class="icon">🛡️</span>
#             <div>
#                 Advanced Privacy Text Detector
#                 <span class="subtitle">AI-Powered Privacy Risk Detection & Analysis System</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Handle preloaded text from browser extension (via ?q=...)
#         query_params = st.query_params
#         if "q" in query_params:
#             preloaded_text = urllib.parse.unquote(query_params["q"])
#             st.session_state["preloaded_text"] = preloaded_text

#         # Render the sidebar and get the selected input type
#         sidebar_input_type, _ = self._render_sidebar()

#         # Navigation Tabs - these are now the main navigation and are always visible
#         tab_titles = ["🔍 Analysis", "📊 Dashboard", "📈 Trends", "⚙️ Settings"]
        
#         # This will create the tabs. When a user clicks a tab, Streamlit reruns.
#         # In older Streamlit, the `st.tabs` function does not return the selected tab
#         # or have a `key` to link to session state for direct state management based on user clicks.
#         # Therefore, clicking these tabs WILL NOT automatically change the content displayed below
#         # (which relies on st.session_state.active_tab_name).
#         # The st.session_state.active_tab_name will only be updated programmatically
#         # after an analysis is performed.
#         st.tabs(tab_titles) # Removed 'key' as it's not supported in older versions

#         # Divide the main content area into two columns: one for input/analysis, one for quick info
#         main_input_col, quick_info_col = st.columns([3, 1])

#         with main_input_col:
#             st.subheader("📝 Input Data")

#             user_text = ""
#             uploaded_file_main = None

#             if sidebar_input_type == "text":
#                 preloaded = st.session_state.get("preloaded_text", "")
#                 user_text = st.text_area(
#                     "🔐 Enter Text to Analyze:",
#                     value=preloaded,
#                     height=300,
#                     key="main_text_input",
#                     placeholder="Paste your text here for privacy risk analysis...",
#                     help="Enter any text content you want to analyze for privacy risks"
#                 )
#                 if st.button("🔍 Analyze Text", type="primary", use_container_width=True, key="analyze_text_button"):
#                     if user_text.strip():
#                         with st.spinner("Analyzing text for privacy risks..."):
#                             results = self._perform_analysis(user_text)
#                             st.session_state.current_results = results
#                             self._add_to_history(user_text, results)
#                             st.success("✅ Analysis complete!")
#                         st.session_state.active_tab_name = "🔍 Analysis" # Programmatically switch to Analysis tab
#                         st.rerun() # Rerun to display results
#                     else:
#                         st.warning("⚠️ Please enter some text to analyze.")

#             elif sidebar_input_type == "file":
#                 uploaded_file_main = st.file_uploader(
#                     "📄 Upload PDF/Text File",
#                     type=['txt', 'csv', 'json', 'pdf', 'docx'],
#                     help="Drag and drop file here or click to browse. Supported formats: TXT, CSV, JSON, PDF, DOCX. Limit 200MB per file.",
#                     key="main_file_uploader"
#                 )

#                 if uploaded_file_main is not None:
#                     if 'last_uploaded_file_id' not in st.session_state or st.session_state.last_uploaded_file_id != uploaded_file_main.file_id:
#                         try:
#                             file_content = TextProcessor.extract_text_from_file(uploaded_file_main)
#                             st.session_state.uploaded_file_content = file_content
#                             st.session_state.last_uploaded_file_id = uploaded_file_main.file_id
#                             st.success(f"File '{uploaded_file_main.name}' loaded successfully!")
#                         except Exception as e:
#                             st.error(f"Error reading uploaded file: {e}")
#                             st.session_state.uploaded_file_content = ""
#                             st.session_state.last_uploaded_file_id = None
#                 elif uploaded_file_main is None and 'last_uploaded_file_id' in st.session_state and st.session_state.last_uploaded_file_id is not None:
#                     st.session_state.uploaded_file_content = ""
#                     st.session_state.last_uploaded_file_id = None
#                     st.info("File upload cleared.")

#                 if st.session_state.uploaded_file_content:
#                     st.text_area("📖 Extracted Text Preview:", value=st.session_state.uploaded_file_content, height=200, disabled=True, key="extracted_file_preview")
                
#                 if st.session_state.uploaded_file_content:
#                     if st.button("🔍 Analyze Uploaded File", type="primary", use_container_width=True, key="analyze_file_button"):
#                         with st.spinner("Analyzing file for privacy risks..."):
#                             results = self._perform_analysis(st.session_state.uploaded_file_content)
#                             st.session_state.current_results = results
#                             self._add_to_history(st.session_state.uploaded_file_content, results)
#                             st.success("✅ File analysis complete!")
#                         st.session_state.active_tab_name = "🔍 Analysis" # Programmatically switch to Analysis tab
#                         st.rerun() # Rerun to display results
#                 else:
#                     st.info("⬆️ Please upload a file to enable analysis.")

#             elif sidebar_input_type == "url":
#                 st.warning("🌐 URL analysis feature coming soon! Please use Text Input or File Upload for now.")
#                 url_input_main = st.text_input("Enter URL to analyze:", key="main_url_input")
#                 if st.button("Fetch & Analyze URL (Main)", type="secondary", use_container_width=True, key="analyze_url_button_main"):
#                     st.info("URL analysis is not yet implemented.")

#             # Auto-analyze if extension text was passed and analysis hasn't run yet
#             if st.session_state.get("preloaded_text") and st.session_state.get("analysis_ran") is not True:
#                 st.session_state["input_method_radio"] = "Text Input"
#                 with st.spinner("Analyzing preloaded text..."):
#                     results = self._perform_analysis(st.session_state["preloaded_text"])
#                     st.session_state.current_results = results
#                     st.session_state.analysis_ran = True
#                     self._add_to_history(st.session_state["preloaded_text"], results)
#                     st.success("✅ Auto-analysis complete!")
#                 st.session_state.active_tab_name = "🔍 Analysis" # Programmatically switch to Analysis tab
#                 st.rerun() # Rerun to display results

#         with quick_info_col:
#             st.subheader("📋 Quick Info")
#             with st.expander("📖 Analysis Guide", expanded=True):
#                 st.markdown("""
#                 This tool helps detect sensitive information.
#                 **What we detect:**
#                 - 🆔 **Government IDs:** Social Security Numbers (SSN, Aadhaar, PAN)
#                 - 💳 **Financial Data:** Credit Card Numbers, Bank Account Numbers (IBAN)
#                 - 📞 **Contact Info:** Email Addresses, Phone Numbers, IP Addresses
#                 - 👤 **Personal Identifiers:** Names, Dates of Birth, Gender
#                 - 🏠 **Addresses & Locations:** Street Addresses, Cities, Countries
#                 - 🌐 **Technical Identifiers:** MAC Addresses, API Keys (if configured)

#                 **Risk Levels:**
#                 - 🟢 **Low (0-3)**: Minimal privacy risk, generally safe to share.
#                 - 🟡 **Medium (3-6)**: Moderate attention needed, review before sharing.  
#                 - 🟠 **High (6-8)**: Significant risk present, strong caution advised.
#                 - 🔴 **Critical (8-10)**: Immediate action required, highly sensitive data.
#                 """)
#             with st.expander("🧪 Sample Texts"):
#                 st.markdown("Click a button to load a sample text into the main input area.")
#                 if st.button("📞 Contact Info Sample", key="sample_contact_main"):
#                     st.session_state["preloaded_text"] = """
#                     Contact Information:
#                     Email: john.doe@company.com
#                     Phone: +1-555-123-4567
#                     Address: 123 Main St, Anytown, ST 12345
#                     Date of Birth: 1985-03-15
#                     """
#                     st.session_state["input_method_radio"] = "Text Input"
#                     st.rerun()
#                 if st.button("🆔 ID Numbers Sample", key="sample_id_main"):
#                     st.session_state["preloaded_text"] = """
#                     Personal Details:
#                     SSN: 123-45-6789
#                     Credit Card: 4532 1234 5678 9012
#                     Phone: 9876543210
#                     Aadhaar: 1234 5678 9012
#                     """
#                     st.session_state["input_method_radio"] = "Text Input"
#                     st.rerun()
#                 if st.button("🌐 Mixed Data Sample", key="sample_mixed_main"):
#                     st.session_state["preloaded_text"] = """
#                     Meeting notes for Project X. Attendees: Jane Doe (jane.doe@example.com), John Smith (phone: 555-987-6543). 
#                     Discussion about financial report from Q3 2024. Account number: GB33BUKB20201555555555. 
#                     The server IP address is 192.168.1.100.
#                     """
#                     st.session_state["input_method_radio"] = "Text Input"
#                     st.rerun()

#         # Results Section - displayed conditionally after input section
#         if st.session_state.current_results:
#             st.markdown("---") # Separator before results
#             st.subheader("Results") # Header for the results section
            
#             # Now, based on which tab is "active" in the top navigation,
#             # we render the corresponding content here.
#             if st.session_state.active_tab_name == "🔍 Analysis":
#                 self._render_analysis_tab()
#             elif st.session_state.active_tab_name == "📊 Dashboard":
#                 self._render_dashboard_tab()
#             elif st.session_state.active_tab_name == "📈 Trends":
#                 self._render_trends_tab()
#             elif st.session_state.active_tab_name == "⚙️ Settings":
#                 self._render_settings_tab()
#             # If for some reason active_tab_name is not set (shouldn't happen with default)
#             else:
#                 st.info("Please select a tab to view analysis details.")

# # ====================
# # APPLICATION ENTRY POINT
# # ====================

# def main():
#     """Main application entry point."""
#     try:
#         app = AdvancedPrivacyDetector()
#         app.run()
#     except Exception as e:
#         st.error(f"Application error: {e}")
#         st.write("Please refresh the page or contact support.")

# if __name__ == "__main__":
#     main()









import streamlit as st
import urllib.parse
from enhanced_regex import EnhancedRegexDetector
from advanced_ner import AdvancedNERDetector
from advanced_llm import AdvancedLLMDetector
from scoring_engine import AdvancedScoringEngine
from visualizer import PrivacyVisualizer
# Import all necessary functions and the TextProcessor class from sidebar.py
from sidebar import _render_sidebar, _render_analysis_tab, _render_dashboard_tab, _render_trends_tab, _render_settings_tab, _perform_analysis, _display_analysis_results, _add_to_history, TextProcessor
from typing import List, Dict

# Core ML/NLP imports - keep these as they are, assuming they are handled by the environment
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
    import spacy
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import torch
except ImportError as e:
    st.error(f"Required packages not installed: {e}")

# ====================
# MAIN APPLICATION
# ====================
class AdvancedPrivacyDetector:
    """Main application class for the Privacy Guardian."""

    def __init__(self):
        # Initialize core detection and scoring components
        self.regex_detector = EnhancedRegexDetector()
        self.ner_detector = AdvancedNERDetector()
        self.llm_detector = AdvancedLLMDetector() # <-- Corrected this line
        self.scoring_engine = AdvancedScoringEngine()
        self.visualizer = PrivacyVisualizer()

        # Initialize Streamlit session state variables if they don't exist
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'current_results' not in st.session_state:
            st.session_state.current_results = None
        if 'analysis_ran' not in st.session_state:
            st.session_state.analysis_ran = False # To track if auto-analysis has run
        if 'uploaded_file_content' not in st.session_state:
            st.session_state.uploaded_file_content = ""
        if 'last_uploaded_file_id' not in st.session_state:
            st.session_state.last_uploaded_file_id = None


    # These methods are wrappers to call functions defined in sidebar.py
    # This structure keeps the main app logic cleaner and delegates UI rendering
    # and analysis execution to the appropriate modules.
    def _render_sidebar(self):
        """Renders the application sidebar and returns user input choices."""
        return _render_sidebar()

    def _render_analysis_tab(self):
        """Renders the Analysis tab content."""
        return _render_analysis_tab(self)

    def _render_dashboard_tab(self):
        """Renders the Dashboard tab content."""
        return _render_dashboard_tab(self)

    def _render_trends_tab(self):
        """Renders the Trends tab content."""
        return _render_trends_tab(self)

    def _render_settings_tab(self):
        """Renders the Settings tab content."""
        return _render_settings_tab(self)

    def _perform_analysis(self, text: str) -> Dict:
        """Performs the comprehensive privacy analysis on the given text."""
        return _perform_analysis(self, text)

    def _display_analysis_results(self, results: Dict):
        """Displays the detailed analysis results."""
        return _display_analysis_results(self, results)

    def _add_to_history(self, text: str, results: Dict):
        """Adds the current analysis results to the history."""
        return _add_to_history(self, text, results)

    def run(self):
        """Main method to run the Streamlit application."""
        st.set_page_config(
            page_title="Advanced Privacy Guardian",
            page_icon="🛡️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for enhanced visual aesthetics (Green and Black theme)
        st.markdown("""
        <style>
            /* General styling for the main application background */
            .stApp {
                background-color: #1a1a1a; /* Dark background */
                color: #e0e0e0; /* Light text for contrast */
                font-family: 'Inter', sans-serif;
                padding-top: 20px;
            }
            /* Styling for the main header */
            .main-header {
                font-size: 2.5em;
                font-weight: bold;
                color: #4CAF50; /* Green for branding */
                text-align: center;
                padding: 20px;
                background-color: #2c2c2c; /* Slightly lighter dark background for header */
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* More prominent shadow */
            }
            /* Styling for subheaders */
            h1, h2, h3, h4, h5, h6 {
                color: #4CAF50; /* Green for section titles */
            }
            /* Styling for primary buttons */
            .stButton>button {
                background-color: #4CAF50; /* Green button */
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 1em;
                transition: all 0.3s ease; /* Smooth transition for hover effects */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); /* Darker shadow for buttons */
                border: none; /* No border for a cleaner look */
            }
            .stButton>button:hover {
                background-color: #45a049; /* Darker green on hover */
                transform: translateY(-2px); /* Slight lift effect */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); /* Enhanced shadow on hover */
            }
            /* Styling for metric cards (e.g., Overall Risk Score) */
            .metric-card {
                background-color: #2c2c2c; /* Dark background for cards */
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                border-left: 5px solid; /* Colored border for risk level indication */
            }
            /* Specific border colors for different risk levels */
            .risk-low { border-left-color: #4CAF50; } /* Green */
            .risk-medium { border-left-color: #FFC107; } /* Amber */
            .risk-high { border-left-color: #FF5722; } /* Deep Orange */
            .risk-critical { border-left-color: #D32F2F; } /* Red */
            /* Styling for tab headers */
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                font-size: 1.1em;
                font-weight: bold;
                color: #e0e0e0; /* Light text for tabs */
            }
            .stTabs [data-baseweb="tab-list"] button {
                background-color: #2c2c2c; /* Darker tab background */
                border-radius: 8px 8px 0 0; /* Rounded top corners */
                margin-right: 5px;
            }
            .stTabs [data-baseweb="tab-list"] button:hover {
                background-color: #3a3a3a; /* Lighter on hover */
            }
            .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                background-color: #4CAF50; /* Green for selected tab */
                color: white;
            }
            /* Adjust sidebar width */
            section[data-testid="stSidebar"] {
                width: 350px !important;
                background-color: #0d0d0d; /* Even darker sidebar */
                color: #e0e0e0;
            }
            /* Styling for text areas and file uploaders */
            .stTextArea textarea, .stFileUploader label {
                background-color: #2c2c2c; /* Dark input fields */
                color: #e0e0e0;
                border-radius: 8px;
                border: 1px solid #4CAF50; /* Green border */
            }
            .stTextArea label, .stFileUploader label {
                color: #e0e0e0; /* Label color */
            }
            /* Info/Warning messages */
            .stAlert {
                border-radius: 8px;
            }
            .stAlert.info {
                background-color: #2c2c2c;
                color: #81D4FA; /* Light blue for info */
                border-left: 5px solid #81D4FA;
            }
            .stAlert.warning {
                background-color: #2c2c2c;
                color: #FFD54F; /* Amber for warning */
                border-left: 5px solid #FFD54F;
            }
            .stAlert.success {
                background-color: #2c2c2c;
                color: #A5D6A7; /* Light green for success */
                border-left: 5px solid #A5D6A7;
            }
            /* Custom styling for the main header with icon and AI-Powered text */
            .custom-header {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                font-size: 2.5em;
                font-weight: bold;
                color: #e0e0e0; /* White text */
                background: linear-gradient(45deg, #1a1a1a, #4CAF50); /* Gradient background */
                padding: 25px 0;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
            }
            .custom-header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(76,175,80,0.2) 0%, rgba(26,26,26,0) 70%);
                transform: rotate(45deg);
                opacity: 0.7;
            }
            .custom-header .icon {
                font-size: 1.2em;
                color: white; /* White icon */
                text-shadow: 0 0 10px #4CAF50; /* Green glow */
            }
            .custom-header .subtitle {
                font-size: 0.4em;
                font-weight: normal;
                color: #c0c0c0; /* Lighter grey for subtitle */
                margin-top: -10px; /* Pull subtitle closer to main title */
                display: block; /* Ensure subtitle is on a new line */
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Main Header with icon and subtitle
        st.markdown("""
        <div class="custom-header">
            <span class="icon">🛡️</span>
            <div>
                Advanced Privacy Text Detector
                <span class="subtitle">AI-Powered Privacy Risk Detection & Analysis System</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Handle preloaded text from browser extension (via ?q=...)
        query_params = st.query_params
        if "q" in query_params:
            preloaded_text = urllib.parse.unquote(query_params["q"])
            st.session_state["preloaded_text"] = preloaded_text

        # Render the sidebar and get the selected input type
        sidebar_input_type, _ = self._render_sidebar()

        # Divide the main content area into two columns: one for input/analysis, one for quick info
        main_input_col, quick_info_col = st.columns([3, 1])

        with main_input_col:
            st.subheader("📝 Input Data")

            user_text = ""
            uploaded_file_main = None

            if sidebar_input_type == "text":
                preloaded = st.session_state.get("preloaded_text", "")
                user_text = st.text_area(
                    "🔐 Enter Text to Analyze:",
                    value=preloaded,
                    height=300,
                    key="main_text_input",
                    placeholder="Paste your text here for privacy risk analysis...",
                    help="Enter any text content you want to analyze for privacy risks"
                )
                if st.button("🔍 Analyze Text", type="primary", use_container_width=True, key="analyze_text_button"):
                    if user_text.strip():
                        with st.spinner("Analyzing text for privacy risks..."):
                            results = self._perform_analysis(user_text)
                            st.session_state.current_results = results
                            self._add_to_history(user_text, results)
                            st.success("✅ Analysis complete!")
                        st.rerun() # Rerun to display results
                    else:
                        st.warning("⚠️ Please enter some text to analyze.")

            elif sidebar_input_type == "file":
                uploaded_file_main = st.file_uploader(
                    "📄 Upload PDF/Text File",
                    type=['txt', 'csv', 'json', 'pdf', 'docx'],
                    help="Drag and drop file here or click to browse. Supported formats: TXT, CSV, JSON, PDF, DOCX. Limit 200MB per file.",
                    key="main_file_uploader"
                )

                if uploaded_file_main is not None:
                    if 'last_uploaded_file_id' not in st.session_state or st.session_state.last_uploaded_file_id != uploaded_file_main.file_id:
                        try:
                            file_content = TextProcessor.extract_text_from_file(uploaded_file_main)
                            st.session_state.uploaded_file_content = file_content
                            st.session_state.last_uploaded_file_id = uploaded_file_main.file_id
                            st.success(f"File '{uploaded_file_main.name}' loaded successfully!")
                        except Exception as e:
                            st.error(f"Error reading uploaded file: {e}")
                            st.session_state.uploaded_file_content = ""
                            st.session_state.last_uploaded_file_id = None
                    # Only show preview if there is content AND the file hasn't been cleared
                    if st.session_state.uploaded_file_content and uploaded_file_main:
                        st.text_area("📖 Extracted Text Preview:", value=st.session_state.uploaded_file_content, height=200, disabled=True, key="extracted_file_preview")
                elif uploaded_file_main is None and 'last_uploaded_file_id' in st.session_state and st.session_state.last_uploaded_file_id is not None:
                    # If file was previously uploaded but now cleared, reset state
                    st.session_state.uploaded_file_content = ""
                    st.session_state.last_uploaded_file_id = None
                    st.info("File upload cleared.")


                if st.session_state.uploaded_file_content:
                    if st.button("🔍 Analyze Uploaded File", type="primary", use_container_width=True, key="analyze_file_button"):
                        with st.spinner("Analyzing file for privacy risks..."):
                            results = self._perform_analysis(st.session_state.uploaded_file_content)
                            st.session_state.current_results = results
                            self._add_to_history(st.session_state.uploaded_file_content, results)
                            st.success("✅ File analysis complete!")
                        st.rerun() # Rerun to display results
                else:
                    st.info("⬆️ Please upload a file to enable analysis.")

            elif sidebar_input_type == "url":
                st.warning("🌐 URL analysis feature coming soon! Please use Text Input or File Upload for now.")
                url_input_main = st.text_input("Enter URL to analyze:", key="main_url_input")
                if st.button("Fetch & Analyze URL (Main)", type="secondary", use_container_width=True, key="analyze_url_button_main"):
                    st.info("URL analysis is not yet implemented.")

            # Auto-analyze if extension text was passed and analysis hasn't run yet
            if st.session_state.get("preloaded_text") and st.session_state.get("analysis_ran") is not True:
                # Ensure the sidebar input type is set to text input for preloaded text
                st.session_state["input_method_radio"] = "Text Input" 
                with st.spinner("Analyzing preloaded text..."):
                    results = self._perform_analysis(st.session_state["preloaded_text"])
                    st.session_state.current_results = results
                    st.session_state.analysis_ran = True
                    self._add_to_history(st.session_state["preloaded_text"], results)
                    st.success("✅ Auto-analysis complete!")
                st.rerun() # Rerun to display results


        with quick_info_col:
            st.subheader("📋 Quick Info")
            with st.expander("📖 Analysis Guide", expanded=True):
                st.markdown("""
                This tool helps detect sensitive information.
                **What we detect:**
                - 🆔 **Government IDs:** Social Security Numbers (SSN, Aadhaar, PAN)
                - 💳 **Financial Data:** Credit Card Numbers, Bank Account Numbers (IBAN)
                - 📞 **Contact Info:** Email Addresses, Phone Numbers, IP Addresses
                - 👤 **Personal Identifiers:** Names, Dates of Birth, Gender
                - 🏠 **Addresses & Locations:** Street Addresses, Cities, Countries
                - 🌐 **Technical Identifiers:** MAC Addresses, API Keys (if configured)

                **Risk Levels:**
                - 🟢 **Low (0-3)**: Minimal privacy risk, generally safe to share.
                - 🟡 **Medium (3-6)**: Moderate attention needed, review before sharing.  
                - 🟠 **High (6-8)**: Significant risk present, strong caution advised.
                - 🔴 **Critical (8-10)**: Immediate action required, highly sensitive data.
                """)
            with st.expander("🧪 Sample Texts"):
                st.markdown("Click a button to load a sample text into the main input area.")
                if st.button("📞 Contact Info Sample", key="sample_contact_main"):
                    st.session_state["preloaded_text"] = """
                    Contact Information:
                    Email: john.doe@company.com
                    Phone: +1-555-123-4567
                    Address: 123 Main St, Anytown, ST 12345
                    Date of Birth: 1985-03-15
                    """
                    st.session_state["input_method_radio"] = "Text Input"
                    st.rerun()
                if st.button("🆔 ID Numbers Sample", key="sample_id_main"):
                    st.session_state["preloaded_text"] = """
                    Personal Details:
                    SSN: 123-45-6789
                    Credit Card: 4532 1234 5678 9012
                    Phone: 9876543210
                    Aadhaar: 1234 5678 9012
                    """
                    st.session_state["input_method_radio"] = "Text Input"
                    st.rerun()
                if st.button("🌐 Mixed Data Sample", key="sample_mixed_main"):
                    st.session_state["preloaded_text"] = """
                    Meeting notes for Project X. Attendees: Jane Doe (jane.doe@example.com), John Smith (phone: 555-987-6543). 
                    Discussion about financial report from Q3 2024. Account number: GB33BUKB20201555555555. 
                    The server IP address is 192.168.1.100.
                    """
                    st.session_state["input_method_radio"] = "Text Input"
                    st.rerun()

        # Results Section - displayed conditionally after input section
        if st.session_state.current_results:
            st.markdown("---") # Separator before results
            st.subheader("Results") # Header for the results section
            
            # Navigation Tabs - these are now the main navigation and are always visible
            tab1, tab2, tab3, tab4 = st.tabs(["🔍 Analysis", "📊 Dashboard", "📈 Trends", "⚙️ Settings"])
            
            with tab1:
                self._render_analysis_tab()
            
            with tab2:
                self._render_dashboard_tab()
            
            with tab3:
                self._render_trends_tab()
            
            with tab4:
                self._render_settings_tab()

# ====================
# APPLICATION ENTRY POINT
# ====================

def main():
    """Main application entry point."""
    try:
        app = AdvancedPrivacyDetector()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.write("Please refresh the page or contact support.")

if __name__ == "__main__":
    main()