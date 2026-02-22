"""
Utilities for extracting specific data patterns from text
"""

import re
from typing import List, Set

class DataExtractor:
    """Extract emails, phone numbers, and other data from text"""
    
    # Regex patterns
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERN = r'(?:\+91|91)?[-.\s]?(?:\d{5}[-.\s]?\d{5}|\d{4}[-.\s]?\d{6}|\d{3}[-.\s]?\d{7}|\d{10})'
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract email addresses from text
        
        Args:
            text: Text to search
            
        Returns:
            List of unique email addresses
        """
        if not text:
            return []
        
        emails = re.findall(DataExtractor.EMAIL_PATTERN, text)
        # Filter out common non-contact emails
        filtered = [
            email for email in emails 
            if not any(x in email.lower() for x in ['example.com', 'test.com', 'domain.com'])
        ]
        return list(set(filtered))
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """
        Extract phone numbers from text
        
        Args:
            text: Text to search
            
        Returns:
            List of unique phone numbers
        """
        if not text:
            return []
        
        phones = re.findall(DataExtractor.PHONE_PATTERN, text)
        # Clean and format phone numbers
        cleaned = []
        for phone in phones:
            # Remove spaces, dots, hyphens
            clean = re.sub(r'[-.\s]', '', phone)
            # Remove +91 or 91 prefix if present
            clean = re.sub(r'^(\+91|91)', '', clean)
            # Only keep 10-digit numbers
            if len(clean) == 10 and clean.isdigit():
                cleaned.append(clean)
        
        return list(set(cleaned))
    
    @staticmethod
    def extract_branches(text: str) -> List[str]:
        """
        Extract engineering branch names from text
        
        Args:
            text: Text to search
            
        Returns:
            List of branch names found
        """
        if not text:
            return []
        
        text_lower = text.lower()
        branches = []
        
        # Common branch keywords
        branch_keywords = {
            'computer science': 'Computer Science Engineering',
            'cse': 'Computer Science Engineering',
            'information technology': 'Information Technology',
            'it': 'Information Technology',
            'electronics and communication': 'Electronics and Communication Engineering',
            'ece': 'Electronics and Communication Engineering',
            'electrical': 'Electrical Engineering',
            'eee': 'Electrical Engineering',
            'mechanical': 'Mechanical Engineering',
            'civil': 'Civil Engineering',
            'chemical': 'Chemical Engineering',
            'biotechnology': 'Biotechnology',
            'automobile': 'Automobile Engineering',
            'aerospace': 'Aerospace Engineering',
            'instrumentation': 'Instrumentation Engineering',
            'production': 'Production Engineering',
            'industrial': 'Industrial Engineering',
            'mining': 'Mining Engineering',
            'petroleum': 'Petroleum Engineering',
            'textile': 'Textile Engineering',
            'metallurgical': 'Metallurgical Engineering',
            'marine': 'Marine Engineering'
        }
        
        for keyword, branch_name in branch_keywords.items():
            if keyword in text_lower and branch_name not in branches:
                branches.append(branch_name)
        
        return branches
    
    @staticmethod
    def clean_college_name(name: str) -> str:
        """
        Clean and standardize college name
        
        Args:
            name: Raw college name
            
        Returns:
            Cleaned college name
        """
        if not name:
            return ""
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Remove common prefixes/suffixes that might be duplicated
        name = re.sub(r'\s*-\s*$', '', name)
        
        return name.strip()
    
    @staticmethod
    def extract_location(text: str, state: str) -> str:
        """
        Extract location/address information
        
        Args:
            text: Text to search
            state: State name to help identify location
            
        Returns:
            Location string
        """
        if not text:
            return ""
        
        # Look for common address patterns
        # This is a simplified version - could be enhanced
        location_patterns = [
            r'(?:located in|address:|location:)\s*([^.]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*' + re.escape(state) + r')',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
