import requests
import json
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

def find_script(url: str, script_id: str) -> Optional[Dict[str, Any]]:
    try:
        # Fetch the HTML content from the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        script_tag = soup.find('script', id=script_id)

        if script_tag is None:
            return None

        props = json.loads(script_tag.get_text())['props']

        latest_version = props['versions'][0]

        description = props['app']['media']['description']

        total_downloads = props['app']['stats']['pdownloads']

        info = {
            'name': latest_version['name'],
            'version': latest_version['vername'],
            'date': latest_version['date'],
            'downloads': total_downloads,
            'description': description,
        }

        return info
    except Exception:
        return None
