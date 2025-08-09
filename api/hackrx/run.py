from backend.main import app  # Import FastAPI app from backend
from mangum import Mangum

# Wrap FastAPI in Mangum for AWS Lambda/Vercel serverless
handler = Mangum(app)