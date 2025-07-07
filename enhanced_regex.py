# import re
# from typing import List, Dict, Tuple
# # ====================
# # ADVANCED REGEX PATTERNS
# # ====================

# class EnhancedRegexDetector:
#     """Enhanced regex patterns with international support"""
    
#     @staticmethod
#     def get_patterns() -> Dict[str, Dict]:
#         return {
#             # Indian Patterns
#             'aadhaar': {
#     'pattern': r'\b(?!0000(?:\s|-)?0000(?:\s|-)?0000)(\d{4}(?:\s|-)?\d{4}(?:\s|-)?\d{4})\b',
#     'weight': 5.0,
#     'category': 'critical_pii',
#     'description': 'Indian Aadhaar Number (validated format)'
#     },

#             'pan': {
#                 'pattern': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
#                 'weight': 4.0,
#                 'category': 'critical_pii',
#                 'description': 'Indian PAN Card'
#             },
#             'indian_phone': {
#                 'pattern': r'\b(?:\+91[\s-]?)?[6-9]\d{9}\b',
#                 'weight': 5.0,
#                 'category': 'moderate_pii',
#                 'description': 'Indian Phone Number'
#             },
            
#             # International Patterns
#             'us_ssn': {
#                 'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
#                 'weight': 5.0,
#                 'category': 'critical_pii',
#                 'description': 'US Social Security Number'
#             },
#             'uk_ni': {
#                 'pattern': r'\b[A-Z]{2}\s?\d{6}\s?[A-Z]\b',
#                 'weight': 4.0,
#                 'category': 'critical_pii',
#                 'description': 'UK National Insurance Number'
#             },
#             'international_phone': {
#                 'pattern': r'\b\+\d{1,4}[\s-]?\d{6,14}\b',
#                 'weight': 2.5,
#                 'category': 'moderate_pii',
#                 'description': 'International Phone Number'
#             },
            
#             # Financial
#             'credit_card': {
#                 'pattern': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
#                 'weight': 5.0,
#                 'category': 'critical_pii',
#                 'description': 'Credit/Debit Card Number'
#             },
#             'iban': {
#                 'pattern': r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}[A-Z0-9]{0,16}\b',
#                 'weight': 4.0,
#                 'category': 'critical_pii',
#                 'description': 'IBAN Account Number'
#             },
#             'swift_bic': {
#                 'pattern': r'\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?\b',
#                 'weight': 3.0,
#                 'category': 'moderate_pii',
#                 'description': 'SWIFT/BIC Code'
#             },
            
#             # Common Patterns
#             'email': {
#                 'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
#                 'weight': 2.5,
#                 'category': 'moderate_pii',
#                 'description': 'Email Address'
#             },
#             'ip_address': {
#                 'pattern': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
#                 'weight': 2.0,
#                 'category': 'moderate_pii',
#                 'description': 'IP Address'
#             },
#             'mac_address': {
#                 'pattern': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
#                 'weight': 2.0,
#                 'category': 'moderate_pii',
#                 'description': 'MAC Address'
#             },
#             'passport': {
#                 'pattern': r'\b[A-Z][0-9]{7,8}\b',
#                 'weight': 4.0,
#                 'category': 'critical_pii',
#                 'description': 'Passport Number'
#             },
#             'license_plate': {
#                 'pattern': r'\b[A-Z]{1,3}[\s-]?\d{1,4}[\s-]?[A-Z]{1,3}\b',
#                 'weight': 2.0,
#                 'category': 'moderate_pii',
#                 'description': 'License Plate'
#             },
#             'date_of_birth': {
#                 'pattern': r'\b(?:0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.](?:19|20)\d{2}\b',
#                 'weight': 3.0,
#                 'category': 'moderate_pii',
#                 'description': 'Date of Birth'
#             },
#             'coordinate': {
#                 'pattern': r'\b-?\d{1,3}\.\d{4,},?\s*-?\d{1,3}\.\d{4,}\b',
#                 'weight': 2.5,
#                 'category': 'moderate_pii',
#                 'description': 'GPS Coordinates'
#             }
#         }



import re
from typing import List, Dict, Tuple

# ====================
# ADVANCED REGEX PATTERNS
# ====================

class EnhancedRegexDetector:
    """Enhanced regex patterns with international support"""

    def __init__(self):
        self.patterns = self.get_patterns()

    @staticmethod
    def get_patterns() -> Dict[str, Dict]:
        return {
            # Indian Patterns
            'aadhaar': {
                'pattern': r'\b(?!0000(?:\s|-)?0000(?:\s|-)?0000)(\d{4}(?:\s|-)?\d{4}(?:\s|-)?\d{4})\b',
                'weight': 5.0,
                'category': 'critical_pii',
                'description': 'Indian Aadhaar Number (validated format)'
            },
            'pan': {
                'pattern': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
                'weight': 4.0,
                'category': 'critical_pii',
                'description': 'Indian PAN Card'
            },
            'indian_phone': {
                'pattern': r'\b(?:\+91[\s-]?)?[6-9]\d{9}\b',
                'weight': 5.0,
                'category': 'moderate_pii',
                'description': 'Indian Phone Number'
            },
            # International Patterns
            'us_ssn': {
                'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
                'weight': 5.0,
                'category': 'critical_pii',
                'description': 'US Social Security Number'
            },
            'uk_ni': {
                'pattern': r'\b[A-Z]{2}\s?\d{6}\s?[A-Z]\b',
                'weight': 4.0,
                'category': 'critical_pii',
                'description': 'UK National Insurance Number'
            },
            'international_phone': {
                'pattern': r'\b\+\d{1,4}[\s-]?\d{6,14}\b',
                'weight': 2.5,
                'category': 'moderate_pii',
                'description': 'International Phone Number'
            },
            # Financial
            'credit_card': {
                'pattern': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                'weight': 5.0,
                'category': 'critical_pii',
                'description': 'Credit/Debit Card Number'
            },
            'iban': {
                'pattern': r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}[A-Z0-9]{0,16}\b',
                'weight': 4.0,
                'category': 'critical_pii',
                'description': 'IBAN Account Number'
            },
            'swift_bic': {
                'pattern': r'\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?\b',
                'weight': 3.0,
                'category': 'moderate_pii',
                'description': 'SWIFT/BIC Code'
            },
            # Common Patterns
            'email': {
                'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'weight': 2.5,
                'category': 'moderate_pii',
                'description': 'Email Address'
            },
            'ip_address': {
                'pattern': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                'weight': 2.0,
                'category': 'moderate_pii',
                'description': 'IP Address'
            },
            'mac_address': {
                'pattern': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
                'weight': 2.0,
                'category': 'moderate_pii',
                'description': 'MAC Address'
            },
            'passport': {
                'pattern': r'\b[A-Z][0-9]{7,8}\b',
                'weight': 4.0,
                'category': 'critical_pii',
                'description': 'Passport Number'
            },
            'license_plate': {
                'pattern': r'\b[A-Z]{1,3}[\s-]?\d{1,4}[\s-]?[A-Z]{1,3}\b',
                'weight': 2.0,
                'category': 'moderate_pii',
                'description': 'License Plate'
            },
            'date_of_birth': {
                'pattern': r'\b(?:0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.](?:19|20)\d{2}\b',
                'weight': 3.0,
                'category': 'moderate_pii',
                'description': 'Date of Birth'
            },
            'coordinate': {
                'pattern': r'\b-?\d{1,3}\.\d{4,},?\s*-?\d{1,3}\.\d{4,}\b',
                'weight': 2.5,
                'category': 'moderate_pii',
                'description': 'GPS Coordinates'
            }
        }

    def detect(self, text: str) -> Dict[str, Dict]:
        """
        Detect PII patterns in the provided text.
        Returns a dictionary with pattern names and their match details.
        """
        results = {}
        for pattern_name, pattern_info in self.patterns.items():
            pattern = pattern_info['pattern']
            matches = list(re.finditer(pattern, text))
            if matches:
                results[pattern_name] = {
                    'description': pattern_info['description'],
                    'count': len(matches),
                    'weight': pattern_info['weight'],
                    'category': pattern_info['category'],
                    'matches': [
                        {
                            'value': match.group(0),
                            'confidence': 0.95,  # Static confidence for regex matches
                            'context': text[max(0, match.start() - 20):match.end() + 20]
                        } for match in matches
                    ]
                }
        return results