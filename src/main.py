"""JobsForHer Scraper - Main entry point."""
import asyncio
import logging
import os
from apify import Actor
from .utils import _fetch
from .parser import parse_jobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main scraper logic."""
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        max_results = actor_input.get('maxResults', 50)
        start_url = actor_input.get('startUrl', 'https://www.jobsforher.com/jobs')
        
        logger.info(f"Starting JobsForHer scraper - maxResults: {max_results}")
        
        # Get proxy configuration
        proxy_config = actor_input.get('proxyConfiguration')
        proxy_url = None
        
        if proxy_config and proxy_config.get('useApifyProxy'):
            # Build Apify proxy URL
            password = os.getenv('APIFY_PROXY_PASSWORD')
            groups = proxy_config.get('apifyProxyGroups', ['RESIDENTIAL'])
            group = groups[0] if groups else 'RESIDENTIAL'
            
            if password:
                proxy_url = f"http://groups-{group}:{password}@proxy.apify.com:8000"
                logger.info(f"Using Apify proxy with group: {group}")
            else:
                logger.warning("APIFY_PROXY_PASSWORD not found in environment")
        
        # Track progress
        results_count = 0
        page = 1
        
        # Main scraping loop
        while results_count < max_results:
            # Construct paginated URL
            if page == 1:
                url = start_url
            else:
                # JobsForHer pagination (common patterns - may need adjustment)
                separator = '&' if '?' in start_url else '?'
                url = f"{start_url}{separator}page={page}"
            
            logger.info(f"Fetching page {page}: {url}")
            
            # Retry logic
            html = None
            for attempt in range(3):
                try:
                    html = await _fetch(url, proxy_url)
                    if html:
                        break
                    logger.warning(f"Attempt {attempt + 1}/3 failed for {url}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1}/3 error: {e}")
                    if attempt < 2:
                        await asyncio.sleep(2 ** attempt)
            
            if not html:
                logger.error(f"Failed to fetch page {page} after 3 attempts")
                break
            
            # Parse jobs from HTML
            jobs = parse_jobs(html, url)
            
            if not jobs:
                logger.warning(f"No jobs found on page {page}, stopping pagination")
                break
            
            logger.info(f"Found {len(jobs)} jobs on page {page}")
            
            # Push results to dataset immediately
            for job in jobs:
                if results_count >= max_results:
                    break
                
                await Actor.push_data(job)
                results_count += 1
                
                # Log progress every 10 results
                if results_count % 10 == 0:
                    logger.info(f"Progress: {results_count}/{max_results} jobs scraped")
            
            # Stop if we've reached max results
            if results_count >= max_results:
                logger.info(f"Reached maxResults limit: {max_results}")
                break
            
            # Move to next page
            page += 1
            
            # Prevent infinite loops
            if page > 100:
                logger.warning("Reached max page limit (100)")
                break
            
            # Polite delay between pages
            await asyncio.sleep(2)
        
        logger.info(f"Scraping complete. Total results: {results_count}")


if __name__ == '__main__':
    asyncio.run(main())
