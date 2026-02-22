"""
Google search functionality for finding college websites
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
import time
from utils.logger import setup_logger

logger = setup_logger('google_search')

class GoogleSearcher:
    """Search Google for college websites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
    
    def search_colleges(self, state: str, branch: str, college_type: str = "All Types", max_results: int = 20) -> List[Tuple[str, str]]:
        """
        Search for engineering colleges
        
        Args:
            state: State name
            branch: Engineering branch
            college_type: Type of college (Government/Private/All)
            max_results: Maximum number of results to return
            
        Returns:
            List of tuples (college_name, url)
        """
        results = []
        
        try:
            # Construct search query
            query = self._build_query(state, branch, college_type)
            logger.info(f"Searching for: {query}")
            
            # Perform search
            search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num={max_results}"
            
            response = self.session.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find search result links
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:max_results]:
                try:
                    # Extract title and URL
                    link_tag = result.find('a')
                    if link_tag and link_tag.get('href'):
                        url = link_tag['href']
                        
                        # Get title
                        title_tag = result.find('h3')
                        title = title_tag.get_text() if title_tag else "Unknown"
                        
                        # Filter out non-college URLs
                        if self._is_valid_college_url(url, title):
                            results.append((title, url))
                            logger.debug(f"Found: {title} - {url}")
                
                except Exception as e:
                    logger.debug(f"Error parsing result: {e}")
                    continue
            
            logger.info(f"Found {len(results)} potential college websites")
            
        except requests.RequestException as e:
            logger.error(f"Search request failed: {e}")
        except Exception as e:
            logger.error(f"Search error: {e}")
        
        return results
    
    def _build_query(self, state: str, branch: str, college_type: str) -> str:
        """Build Google search query"""
        query_parts = []
        
        # Add college type if specified
        if college_type and college_type != "All Types":
            query_parts.append(college_type.lower())
        
        query_parts.append("engineering college")
        
        # Add branch if not "All Branches"
        if branch and branch != "All Branches":
            query_parts.append(branch)
        
        query_parts.append(state)
        query_parts.append("contact")
        
        return " ".join(query_parts)
    
    def _is_valid_college_url(self, url: str, title: str) -> bool:
        """Check if URL is likely a college website"""
        if not url or url.startswith('#'):
            return False
        
        # Exclude common non-college domains
        exclude_domains = [
            'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'instagram.com', 'wikipedia.org', 'shiksha.com',
            'careers360.com', 'collegedunia.com'
        ]
        
        url_lower = url.lower()
        for domain in exclude_domains:
            if domain in url_lower:
                return False
        
        # Look for college-related keywords
        college_keywords = ['college', 'university', 'institute', 'education', '.edu', '.ac.in']
        
        combined = (url_lower + " " + title.lower())
        return any(keyword in combined for keyword in college_keywords)
    
    def search_with_duckduckgo(self, state: str, branch: str, college_type: str = "All Types", max_results: int = 20) -> List[Tuple[str, str]]:
        """
        Alternative search using DuckDuckGo (more scraping-friendly)
        
        Args:
            state: State name
            branch: Engineering branch
            college_type: Type of college
            max_results: Maximum results
            
        Returns:
            List of tuples (college_name, url)
        """
        results = []
        
        try:
            query = self._build_query(state, branch, college_type)
            logger.info(f"Searching DuckDuckGo for: {query}")
            
            # DuckDuckGo HTML search
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            
            response = self.session.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find result links
            result_links = soup.find_all('a', class_='result__a')
            
            for link in result_links[:max_results]:
                try:
                    url = link.get('href')
                    title = link.get_text(strip=True)
                    
                    if url and self._is_valid_college_url(url, title):
                        results.append((title, url))
                        logger.debug(f"Found: {title} - {url}")
                
                except Exception as e:
                    logger.debug(f"Error parsing result: {e}")
                    continue
            
            logger.info(f"Found {len(results)} potential college websites")
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
        
        return results
