"""
Data models for college information
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CollegeInfo:
    """Data class to store college information"""
    name: str = ""
    university: str = ""
    email: str = ""
    location: str = ""
    branches: List[str] = field(default_factory=list)
    hod_contact: str = ""
    admin_contact: str = ""
    other_contacts: List[str] = field(default_factory=list)
    website: str = ""
    college_type: str = ""  # Government/Private/Autonomous
    
    def to_dict(self):
        """Convert to dictionary for Excel export"""
        return {
            'College Name': self.name,
            'University': self.university,
            'Email': self.email,
            'Location': self.location,
            'Branches': ', '.join(self.branches) if self.branches else '',
            'HOD Contact': self.hod_contact,
            'Admin Contact': self.admin_contact,
            'Other Contacts': ', '.join(self.other_contacts) if self.other_contacts else '',
            'Website': self.website,
            'Type': self.college_type
        }
    
    def is_valid(self):
        """Check if college has minimum required information"""
        return bool(self.name and (self.email or self.website or self.admin_contact))
    
    def __hash__(self):
        """Make hashable for duplicate detection"""
        return hash((self.name.lower(), self.location.lower()))
    
    def __eq__(self, other):
        """Check equality based on name and location"""
        if not isinstance(other, CollegeInfo):
            return False
        return (self.name.lower() == other.name.lower() and 
                self.location.lower() == other.location.lower())


class CollegeDataManager:
    """Manage collection of college data"""
    
    def __init__(self):
        self.colleges: List[CollegeInfo] = []
    
    def add_college(self, college: CollegeInfo):
        """Add college if valid and not duplicate"""
        if college.is_valid() and college not in self.colleges:
            self.colleges.append(college)
            return True
        return False
    
    def get_all(self) -> List[CollegeInfo]:
        """Get all colleges"""
        return self.colleges
    
    def clear(self):
        """Clear all data"""
        self.colleges.clear()
    
    def count(self) -> int:
        """Get count of colleges"""
        return len(self.colleges)
    
    def to_list_of_dicts(self) -> List[dict]:
        """Convert all colleges to list of dictionaries"""
        return [college.to_dict() for college in self.colleges]
