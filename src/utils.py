"""Utility functions for fetching pages with Camoufox."""
import logging
from urllib.parse import urlparse
from camoufox.async_api import AsyncCamoufox

logger = logging.getLogger(__name__)


def _parse_proxy(proxy_url):
    """Parse proxy URL into components for Camoufox."""
    if not proxy_url:
        return None
    
    parsed = urlparse(proxy_url)
    return {
        'server': f'{parsed.scheme}://{parsed.hostname}:{parsed.port}',
        'username': parsed.username,
        'password': parsed.password,
    }


async def _fetch(url, proxy_url=None):
    """
    Fetch a page using Camoufox with residential proxy.
    
    Returns:
        str: HTML content if successful and > 500 bytes, None otherwise
    """
    proxy_config = _parse_proxy(proxy_url) if proxy_url else None
    
    try:
        async with AsyncCamoufox(
            headless=True,
            geoip=True,
            proxy=proxy_config
        ) as browser:
            page = await browser.new_page()
            
            # Navigate and wait for network idle
            response = await page.goto(url, wait_until='networkidle', timeout=90000)
            
            if not response or response.status >= 400:
                logger.warning(f"Bad response status: {response.status if response else 'None'}")
                return None
            
            # Wait for dynamic content to render (JobsForHer/HerKey is heavily React-based)
            await page.wait_for_timeout(8000)
            
            # Try to wait for job content container
            try:
                await page.wait_for_selector('#parentmore_jobs, [data-test-id*="job"]', timeout=10000)
            except Exception as e:
                logger.warning(f"Timeout waiting for job containers: {e}")
            
            # Get HTML content
            html = await page.content()
            
            # Reject suspiciously small responses
            if len(html) < 500:
                logger.warning(f"Response too small: {len(html)} bytes")
                return None
            
            return html
            
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None
