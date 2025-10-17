import requests
import json
import os 
from requests.exceptions import RequestException

from utils.config import USAJOBS_API_KEY


def fetch_usajobs(keyword, location="remote", results_per_page=5):
    """
    Fetches job listings from the USAJOBS API based on keyword and location,
    and extracts key details.
    
    Args:
        keyword (str): The primary search term (e.g., "software engineer").
        location (str): The desired location (e.g., "remote", "Washington, DC").
        results_per_page (int): The maximum number of results to return.
        
    Returns:
        list: A list of dictionaries, where each dictionary contains 
              detailed information about a job posting. Returns an empty 
              list on failure.
    """
    
    headers = {
        'Authorization-Key': USAJOBS_API_KEY, 
        'User-Agent': 'sneha391998@gmail.com',
        'Host': 'data.usajobs.gov'
    }

    params = {
        'Keyword': keyword,
        'LocationName': location,
        'ResultsPerPage': results_per_page,
    }
    
    try:
        response = requests.get('https://data.usajobs.gov/api/search', headers=headers, params=params)
        response.raise_for_status() 
        
        data = response.json()
        result = []
        
        if 'SearchResult' in data and 'SearchResultItems' in data['SearchResult']:
            job_items = data['SearchResult']['SearchResultItems']
            
            for item in job_items:
                descriptor = item.get('MatchedObjectDescriptor', {})
                user_area = descriptor.get('UserArea', {}).get('Details', {})
                
                job_title = descriptor.get('PositionTitle', 'N/A')
                job_url = descriptor.get('PositionURI', 'N/A')
                job_apply_url = descriptor.get('ApplyURI', ['N/A'])[0] 
                job_qualifications = descriptor.get('QualificationSummary', 'N/A')
                

                job_summary = user_area.get('JobSummary', 'N/A') 
                job_duties = user_area.get('MajorDuties', 'N/A') 
                
                result.append({
                    'Job Title': job_title,
                    'Job URL': job_url,
                    'Job Apply URL': job_apply_url,
                    'Job Qualifications': job_qualifications,
                    'Job Summary': job_summary,
                    'Job Duties': job_duties
                })
        
        return result 
    
    except RequestException as e:
        # Catch network or HTTP errors from requests library
        print(f"An error occurred during the request: {e}")
        return []
    except KeyError as e:
        # Catch errors if the JSON structure changes unexpectedly
        print(f"Error parsing response: Missing expected key {e}. Response structure may have changed.")
        return []

# Execute the search
if __name__ == "__main__":
    print(f"\n--- CareerCritter Job Search: Testing 'IT' Query ---")
    titles = fetch_usajobs("it")
    if titles:
        print(f"\nFound {len(titles)} Job Listings:")
        for job in titles:
            print("-" * 30)
            print(f"Title: {job['Job Title']}")
            print(f"URL: {job['Job URL']}")
    else:
        print("\nNo job listings found or an error occurred. Check your API key and network connection.")
