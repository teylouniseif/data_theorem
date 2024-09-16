from wsgiref.simple_server import make_server
import falcon
import os
import json
from typing import Dict, Any
from validation import validate_url
from scraping import find_script

class HomePage:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Serve the HTML page from the templates folder."""
        file_path = os.path.join(os.path.dirname(__file__), 'templates', 'url.html')
        resp.content_type = 'text/html'
        with open(file_path, 'r') as f:
            resp.body = f.read()

class SubmitUrl:
    @validate_url  # Apply the validation decorator to this method
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Handles POST requests."""
        data: Dict[str, str] = req.context['data']
        url: str = data.get('url', '')
        
        # Handle the valid URL
        script_info: Optional[Dict[str, Any]] = find_script(url, '__NEXT_DATA__')

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(script_info)

app = falcon.App()

form_page = HomePage()
app_info = SubmitUrl()

app.add_route('/', form_page)
app.add_route('/info', app_info)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
