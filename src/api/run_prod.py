import uvicorn
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False,
        workers=4,
        log_level="warning"
    )