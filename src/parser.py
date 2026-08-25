"""Parser for JobsForHer job listings."""
import logging
import re
import json
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def _extract_next_data(html):
    """Try to extract __NEXT_DATA__ JSON from page."""
    try:
        match = re.search(r'<script[^>]*id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>', html, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            if data and isinstance(data, dict):
                return data
    except Exception as e:
        logger.debug(f"Could not extract __NEXT_DATA__: {e}")
    return None


def parse_jobs(html, url):
    """
    Parse job listings from JobsForHer HTML.
    
    Returns:
        list: List of job dictionaries
    """
    jobs = []
    
    # Try __NEXT_DATA__ first
    next_data = _extract_next_data(html)
    if next_data:
        logger.debug("Found __NEXT_DATA__ but it may be empty")
    
    # Fall back to HTML parsing (client-side rendered site)
    soup = BeautifulSoup(html, 'html.parser')
    
    # JobsForHer/HerKey uses MUI and dynamically loads jobs
    # Look for job card containers - they appear after JS renders
    job_cards = soup.find_all('div', attrs={'data-test-id': 'job-card'})
    
    if not job_cards:
        # Try alternative selectors - look for any elements with job-related test IDs
        job_cards = soup.find_all(attrs={'data-test-id': re.compile(r'job', re.I)})
    
    if not job_cards:
        # Try finding job links in the dynamically loaded section
        parent_section = soup.find('div', id='parentmore_jobs')
        if parent_section:
            job_cards = parent_section.find_all(['div', 'article'], recursive=True)
    
    if not job_cards:
        # Fallback: look for any link containing /job/ or /apply/
        job_cards = soup.find_all('a', href=re.compile(r'/(job|apply|career)'))
        
    for card in job_cards:
        try:
            job = {}
            
            # Extract job title
            title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'h5'], class_=re.compile(r'(title|name|heading)', re.I))
            if not title_elem:
                title_elem = card.find(['a'], href=re.compile(r'/job'))
            job['title'] = title_elem.get_text(strip=True) if title_elem else None
            
            # Extract company
            company_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'company', re.I))
            job['company'] = company_elem.get_text(strip=True) if company_elem else None
            
            # Extract location
            location_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'location', re.I))
            job['location'] = location_elem.get_text(strip=True) if location_elem else None
            
            # Extract job type/work mode
            type_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'(type|mode|remote|wfh)', re.I))
            job['jobType'] = type_elem.get_text(strip=True) if type_elem else None
            
            # Extract experience
            exp_elem = card.find(['span', 'div', 'p'], string=re.compile(r'(experience|years|yrs)', re.I))
            job['experience'] = exp_elem.get_text(strip=True) if exp_elem else None
            
            # Extract salary
            salary_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'(salary|ctc|compensation)', re.I))
            job['salary'] = salary_elem.get_text(strip=True) if salary_elem else None
            
            # Extract job URL
            link_elem = card.find('a', href=re.compile(r'/job'))
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                if href.startswith('/'):
                    href = f"https://www.jobsforher.com{href}"
                job['url'] = href
            else:
                job['url'] = None
            
            # Extract posted date
            date_elem = card.find(['span', 'div', 'p', 'time'], class_=re.compile(r'(date|posted|time)', re.I))
            job['postedDate'] = date_elem.get_text(strip=True) if date_elem else None
            
            # Extract description snippet
            desc_elem = card.find(['p', 'div'], class_=re.compile(r'(description|summary|snippet)', re.I))
            job['description'] = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Skip if no meaningful data
            if not job.get('title') and not job.get('url'):
                continue
            
            # Add metadata
            from datetime import datetime, timezone
            job['scrapedAt'] = datetime.now(timezone.utc).isoformat()
            job['sourceUrl'] = url
            
            jobs.append(job)
            
        except Exception as e:
            logger.warning(f"Error parsing job card: {e}")
            continue
    
    return jobs
