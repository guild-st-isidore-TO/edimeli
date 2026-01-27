"""
GABC Score Web Scraper
Fetches GABC scores directly from online sources
"""

from bs4 import BeautifulSoup
import requests
import warnings

# Suppress SSL warnings
warnings.filterwarnings('ignore')
requests.packages.urllib3.disable_warnings()


def get_gabc_score(chant_id):
    """
    Scrape GABC score from Cantus Index or GregoBase.
    
    This function attempts to retrieve GABC notation (Gregorian musical notation)
    for a given chant ID by querying multiple online databases.
    
    Args:
        chant_id (str): The ID of the chant to query (required)
    
    Returns:
        str: The GABC score, or None if not found
    """
    
    # Try Cantus Index first - primary source for GABC scores
    print(f"Scraping GABC score for chant {chant_id}...")
    
    gabc_score = try_cantus_index(chant_id)
    if gabc_score:
        print(f"✓ Found on Cantus Index")
        return gabc_score
    
    # Try GregoBase as fallback if Cantus Index doesn't have the score
    gabc_score = try_gregobase(chant_id)
    if gabc_score:
        print(f"✓ Found on GregoBase")
        return gabc_score
    
    # Return None if score not found in either database
    print(f"✗ Could not find GABC score for chant {chant_id}")
    return None


def try_cantus_index(chant_id):
    """
    Try to scrape GABC score from Cantus Index database.
    
    Attempts three strategies:
    1. Extract GABC from HTML content of the chant page
    2. Find and download GABC file links
    3. Query the Cantus Index API endpoint
    """
    try:
        # Try direct chant page using the chant ID
        url = f'https://cantusindex.org/id/{chant_id}'
        print(f"  Visiting: {url}")
        response = requests.get(url, timeout=10, verify=False, allow_redirects=True)
        
        # Process only successful responses
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Strategy 1: Look for GABC content directly embedded in HTML
            gabc_score = extract_gabc_from_html(soup)
            if gabc_score:
                return gabc_score
            
            # Strategy 2: Look for download link to .gabc file in page links
            for link in soup.find_all('a'):
                href = link.get('href', '')
                text = link.get_text()
                # Check if link points to GABC file or is labeled as download
                if '.gabc' in href.lower() or 'download' in text.lower():
                    gabc_url = href
                    # Convert relative URLs to absolute
                    if gabc_url.startswith('/'):
                        gabc_url = f'https://cantusindex.org{gabc_url}'
                    print(f"    → Trying link: {gabc_url}")
                    try:
                        gabc_response = requests.get(gabc_url, timeout=10, verify=False)
                        # GABC files start with '(' character
                        if gabc_response.status_code == 200 and gabc_response.text.strip().startswith('('):
                            return gabc_response.text.strip()
                    except:
                        pass
            
            # Strategy 3: Try the Cantus Index API endpoint for JSON data
            api_url = f'https://cantusindex.org/api/v1/chant/{chant_id}'
            print(f"  Trying API: {api_url}")
            try:
                api_response = requests.get(api_url, timeout=10, verify=False)
                if api_response.status_code == 200:
                    data = api_response.json()
                    # Try to extract GABC or incipit from API response
                    if isinstance(data, dict) and 'gabc' in data:
                        return data['gabc']
                    if 'incipit' in data:
                        return data['incipit']
            except:
                pass
            
    except Exception as e:
        print(f"  Error: {e}")
    
    return None


def try_gregobase(chant_id):
    """
    Try to scrape GABC score from GregoBase (alternative Gregorian music database).
    
    Uses two strategies:
    1. Extract GABC from HTML content
    2. Find and download GABC file links
    """
    try:
        # Build URL for the chant page
        url = f'https://gregobase.selapa.net/chant.php?id={chant_id}'
        print(f"  Visiting: {url}")
        
        response = requests.get(url, timeout=10, verify=False, allow_redirects=True)
        
        # Process only successful responses
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Strategy 1: Look for GABC content embedded in page HTML
            gabc_score = extract_gabc_from_html(soup)
            if gabc_score:
                return gabc_score
            
            # Strategy 2: Look for GABC download links on the page
            for link in soup.find_all('a'):
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # Check if link is labeled as "GABC" or points to a .gabc file
                if 'GABC' in text or '.gabc' in href.lower():
                    gabc_url = href
                    # Convert relative URLs to absolute URLs
                    if gabc_url.startswith('/'):
                        gabc_url = f'https://gregobase.selapa.net{gabc_url}'
                    elif not gabc_url.startswith('http'):
                        gabc_url = f'https://gregobase.selapa.net/{gabc_url}'
                    
                    print(f"    → Found GABC link: {gabc_url}")
                    try:
                        gabc_response = requests.get(gabc_url, timeout=10, verify=False)
                        if gabc_response.status_code == 200:
                            gabc_text = gabc_response.text.strip()
                            # GABC files start with either 'name:' (metadata) or '(' (notation)
                            if gabc_text and (gabc_text.startswith('(') or gabc_text.startswith('name:')):
                                return gabc_text
                    except:
                        pass
            
    except Exception as e:
        print(f"  Error: {e}")
    
    return None


def extract_gabc_from_html(soup):
    """
    Extract GABC notation from various HTML elements.
    
    Tries multiple locations where GABC content might be embedded:
    - textarea elements (common for forms)
    - pre elements (preformatted text)
    - code elements (code blocks)
    - div/span/p elements with GABC content
    """
    # Strategy 1: Look in textarea - often used for displayable text content
    textarea = soup.find('textarea')
    if textarea:
        text = textarea.get_text().strip()
        # GABC notation starts with '(' character
        if text and text.startswith('('):
            return text
    
    # Strategy 2: Look in pre tag - preformatted text preserves whitespace
    pre = soup.find('pre')
    if pre:
        text = pre.get_text().strip()
        if text and text.startswith('('):
            return text
    
    # Strategy 3: Look in code tag - for code blocks
    code = soup.find('code')
    if code:
        text = code.get_text().strip()
        if text and text.startswith('('):
            return text
    
    # Strategy 4: Search for text starting with GABC notation patterns
    # GABC uses patterns like (c4 (d (f (g (h) (a (b
    for elem in soup.find_all(['div', 'span', 'p']):
        text = elem.get_text().strip()
        # Check if text starts with '(' and has reasonable length
        if text.startswith('(') and len(text) > 10:
            # Verify it contains GABC note names (c3, c4, d, f, g, h, etc.)
            if any(c in text for c in ['c4', 'c3', 'd', 'f', 'g', 'h']):
                return text
    
    # Return None if GABC content not found anywhere
    return None


# Main program - interactive GABC score fetcher
if __name__ == '__main__':
    # Display banner
    print("="*60)
    print("GABC Score Web Scraper")
    print("="*60)
    
    # Main loop - continues until user chooses to quit
    while True:
        print("\n")
        # Get chant ID from user
        chant_id = input("Enter chant ID (or 'quit' to exit): ").strip()
        
        # Check if user wants to exit
        if chant_id.lower() == 'quit':
            break
        
        # Validate that chant ID is not empty
        if not chant_id:
            print("Please enter a valid chant ID")
            continue
        
        # Get optional chant type (not required for search)
        chant_type = input("Enter chant type (optional, press Enter to skip): ").strip()
        if not chant_type:
            chant_type = None
        
        # Fetch GABC score using the chant ID
        print(f"\nFetching GABC score for chant {chant_id}" + (f" ({chant_type})" if chant_type else "") + "...")
        gabc = get_gabc_score(chant_id)
        
        # Display results
        if gabc:
            # GABC found - display the score
            print("\n✓ SUCCESS! GABC Score:")
            print("-" * 60)
            # Show first 15 lines of GABC (prevents overwhelming output for large scores)
            lines = gabc.split('\n')
            for line in lines[:15]:
                print(line)
            # Indicate if there are more lines
            if len(lines) > 15:
                print(f"... ({len(lines)} total lines)")
            print("-" * 60)
        else:
            # GABC not found
            print("✗ No GABC score found for this chant ID")
