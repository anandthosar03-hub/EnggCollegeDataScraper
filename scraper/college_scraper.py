"""
College website scraper to extract information
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import time
from data.college_data import CollegeInfo
from scraper.data_extractor import DataExtractor
from utils.logger import setup_logger

logger = setup_logger('college_scraper')

class CollegeScraper:
    """Scrape college websites for information"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.extractor = DataExtractor()
    
    def scrape_college(self, url: str, college_name: str = "", state: str = "") -> Optional[CollegeInfo]:
        """
        Scrape a college website for information
        
        Args:
            url: College website URL
            college_name: College name from search (optional)
            state: State name for location context
            
        Returns:
            CollegeInfo object or None if scraping fails
        """
        try:
            logger.info(f"Scraping: {url}")
            
            # Fetch webpage
            response = self.session.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text(separator=' ', strip=True)
            
            # Create college info object
            college = CollegeInfo()
            college.website = url
            
            # Extract college name
            college.name = self._extract_college_name(soup, college_name)
            
            # Extract emails
            emails = self.extractor.extract_emails(text_content)
            if emails:
                college.email = emails[0]  # Primary email
            
            # Extract phone numbers
            phones = self.extractor.extract_phone_numbers(text_content)
            if phones:
                college.admin_contact = phones[0]  # Primary contact
                if len(phones) > 1:
                    college.other_contacts = phones[1:5]  # Additional contacts
            
            # Extract branches
            college.branches = self.extractor.extract_branches(text_content)
            
            # Extract location
            college.location = self._extract_location(soup, text_content, state)
            
            # Try to determine college type
            college.college_type = self._determine_college_type(text_content)
            
            # Try to find university affiliation
            college.university = self._extract_university(text_content)
            
            # Look for specific contact pages
            self._scrape_contact_page(soup, url, college)
            
            logger.info(f"Successfully scraped: {college.name}")
            return college
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def _extract_college_name(self, soup: BeautifulSoup, fallback_name: str) -> str:
        """Extract college name from webpage"""
        # Try title tag
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            # Clean up title
            title_text = title_text.split('|')[0].split('-')[0].strip()
            if len(title_text) > 5:
                return self.extractor.clean_college_name(title_text)
        
        # Try h1 tag
        h1 = soup.find('h1')
        if h1:
            h1_text = h1.get_text().strip()
            if len(h1_text) > 5:
                return self.extractor.clean_college_name(h1_text)
        
        # Fallback to search result name
        return self.extractor.clean_college_name(fallback_name) if fallback_name else "Unknown College"
    
    def _extract_location(self, soup: BeautifulSoup, text: str, state: str) -> str:
        """Extract location information"""
        # Look for address tags
        address = soup.find('address')
        if address:
            return address.get_text(strip=True)
        
        # Look for common location patterns
        location = self.extractor.extract_location(text, state)
        if location:
            return location
        
        return state  # Fallback to state name
    
    def _determine_college_type(self, text: str) -> str:
        """Determine if college is Government or Private"""
        text_lower = text.lower()
        
        gov_keywords = ['government', 'govt', 'state government', 'central government', 'public college']
        private_keywords = ['private', 'autonomous', 'self-financed']
        
        # Check for government keywords
        if any(keyword in text_lower for keyword in gov_keywords):
            return "Government"
        
        # Check for private keywords
        if any(keyword in text_lower for keyword in private_keywords):
            return "Private"
        
        return "Unknown"
    
    def _extract_university(self, text: str) -> str:
        """Extract university affiliation"""
        # Look for university mentions
        import re
        university_pattern = r'affiliated (?:to|with) ([^.,]+university[^.,]*)'
        match = re.search(university_pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # Look for autonomous university
        if 'autonomous' in text.lower():
            return "Autonomous"
        
        return ""
    
    def _scrape_contact_page(self, soup: BeautifulSoup, base_url: str, college: CollegeInfo):
        """Try to find and scrape contact page for more details"""
        try:
            # Look for contact page link
            contact_links = soup.find_all('a', href=True)
            
            for link in contact_links:
                link_text = link.get_text().lower()
                href = link['href']
                
                if 'contact' in link_text or 'contact-us' in href.lower():
                    # Build full URL
                    if href.startswith('http'):
                        contact_url = href
                    elif href.startswith('/'):
                        from urllib.parse import urljoin
                        contact_url = urljoin(base_url, href)
                    else:
                        continue
                    
                    # Scrape contact page
                    logger.debug(f"Found contact page: {contact_url}")
                    response = self.session.get(contact_url, headers=self.headers, timeout=10)
                    contact_soup = BeautifulSoup(response.text, 'html.parser')
                    contact_text = contact_soup.get_text(separator=' ', strip=True)
                    
                    # Extract additional emails and phones
                    additional_emails = self.extractor.extract_emails(contact_text)
                    additional_phones = self.extractor.extract_phone_numbers(contact_text)
                    
                    # Update college info if we found more data
                    if not college.email and additional_emails:
                        college.email = additional_emails[0]
                    
                    if not college.admin_contact and additional_phones:
                        college.admin_contact = additional_phones[0]
                    
                    break  # Only scrape first contact page found
                    
        except Exception as e:
            logger.debug(f"Could not scrape contact page: {e}")
