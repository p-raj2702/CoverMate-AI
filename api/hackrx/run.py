from backend.main import app  # Import your FastAPI app
from mangum import Mangum

# Wrap FastAPI in Mangum for serverless
handler = Mangum(app)