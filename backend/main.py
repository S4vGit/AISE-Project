from fastapi import FastAPI
from backend.routes import users, fake_news, detection, admin
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create the FastAPI app
app = FastAPI(
    title="Fake News Generator API",
    description="API per generare e analizzare fake news da immagini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allowing all HTTP methods
    allow_headers=["*"],  # Allowing all HTTP headers
)

# Route inclusions
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(fake_news.router, prefix="/fake-news", tags=["Fake News"])
app.include_router(detection.router, prefix="/detection", tags=["Detection"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

# Home route
@app.get("/")
def home():
    return {"message": "Fake News Generator API is running!"}

# Start the API server
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
