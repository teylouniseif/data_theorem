import falcon
import json
from urllib.parse import urlparse
from functools import wraps
from typing import Callable, Dict, Any

# Validation decorator
def validate_url(f: Callable[[Any, falcon.Request, falcon.Response, Any], None]) -> Callable[[Any, falcon.Request, falcon.Response, Any], None]:
    @wraps(f)
    def wrapper(self: Any, req: falcon.Request, resp: falcon.Response, *args: Any, **kwargs: Any) -> None:
        url: str = ''

        if req.content_type == 'application/x-www-form-urlencoded':
            form_data: Dict[str, str] = req.get_media()  # Parses form-encoded body
            url = form_data.get('url', '')
        
        if not url:
            raise falcon.HTTPBadRequest('Missing URL', 'The "url" field is required.')

        if not is_valid_url(url):
            raise falcon.HTTPBadRequest('Invalid URL', 'The "url" field must contain a valid URL.')

        # Pass validated URL via req.context for the route to access
        req.context['data'] = {'url': url}

        return f(self, req, resp, *args, **kwargs)
    
    return wrapper

# Basic URL validation function
def is_valid_url(url: str) -> bool:
    """Basic URL validation using urllib."""
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])
