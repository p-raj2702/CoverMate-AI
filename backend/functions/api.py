from mangum import Mangum
from backend.main import app

# Netlify function runs at /.netlify/functions/api
# Preserve your FastAPI paths (/api/v1/...)
handler = Mangum(app, api_gateway_base_path="/.netlify/functions/api")