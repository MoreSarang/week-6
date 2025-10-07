from typing import Dict, List, Optional

import pandas as pd
import requests


    # Exercise - 1
class Genius:
    """A class to interact with the Genius API for artist and song information."""
    
    BASE_URL = "https://api.genius.com"
    
    def __init__(self, access_token: str):
        """
        Initialize the Genius API client.
        
        Args:
            access_token: Your Genius API access token
        """
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the Genius API."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    # Exercise - 2
    def get_artist(self, search_term: str) -> Dict:
        """Get artist information based on a search term."""
        search_endpoint = "/search"
        search_params = {'q': search_term}
        search_results = self._make_request(search_endpoint, search_params)
        
        if search_results['response']['hits']:
            first_hit = search_results['response']['hits'][0]
            artist_id = first_hit['result']['primary_artist']['id']
            
            artist_endpoint = f"/artists/{artist_id}"
            artist_data = self._make_request(artist_endpoint)
            
            return artist_data['response']['artist']
        else:
            return {}
        
    # Exercise - 3
    def get_artists(self, search_terms: List[str]) -> pd.DataFrame:
        """Get artist information for multiple search terms."""
        results = []
        
        for search_term in search_terms:
            try:
                artist_info = self.get_artist(search_term)
                
                if artist_info:
                    results.append({
                        'search_term': search_term,
                        'artist_name': artist_info.get('name', None),
                        'artist_id': artist_info.get('id', None),
                        'followers_count': artist_info.get('followers_count', None)
                    })
                else:
                    results.append({
                        'search_term': search_term,
                        'artist_name': None,
                        'artist_id': None,
                        'followers_count': None
                    })
            except Exception as e:
                print(f"Error processing '{search_term}': {e}")
                results.append({
                    'search_term': search_term,
                    'artist_name': None,
                    'artist_id': None,
                    'followers_count': None
                })
        
        return pd.DataFrame(results)# your code here ...
