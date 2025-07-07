class PrivacyConfig:
    
    # 🎯 Risk scoring weights per specific PII type
    RISK_WEIGHTS = {
        'aadhaar': 5.0,
        'pan': 4.5,
        'credit_card': 5.0,
        'passport': 4.5,
        'ssn': 5.0,

        'email': 3.0,
        'phone': 3.0,
        'address': 2.5,
        'ip': 2.0,
        'mac': 2.0,

        'dob': 2.0,
        'name': 1.5,
        'username': 1.5,

        'contextual': 2.0,   # Context-dependent risks
        'similarity': 1.5,   # Text similarity risks
        'frequency': 1.0     # Frequency-based risks
    }

    # 🔐 Sensitivity thresholds for risk classification
    SENSITIVITY_LEVELS = {
        'low': (0, 3),
        'medium': (3, 6),
        'high': (6, 8),
        'critical': (8, 10)
    }

    # 📁 File size limit in MB
    MAX_FILE_SIZE = 10

    # 📄 Supported file extensions for upload
    SUPPORTED_TYPES = ['.txt', '.csv', '.json', '.pdf', '.docx']

