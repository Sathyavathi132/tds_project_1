from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tasks  # Import tasks.py

app = FastAPI()

# Enable CORS (optional, useful for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Map task names to corresponding functions in tasks.py
TASKS = {
    "a2": tasks.a2_format_markdown,
    "a3": tasks.a3_count_wednesdays,
    "a4": tasks.a4_sort_contacts,
    "a5": tasks.a5_recent_logs,
    "a6": tasks.a6_extract_headers,
    "a7": tasks.a7_extract_sender,
    "a8": tasks.a8_extract_credit_card,
    "a9": tasks.a9_find_similar_comments,
    "a10": tasks.a10_calculate_gold_sales,
}


@app.get("/")
def home():
    return {"Workings"}

@app.post("/run")
def run_task(task: str):
    if task not in TASKS:
        raise HTTPException(status_code=400, detail="Invalid task name")
    
    try:
        result = TASKS[task]()  # Call the corresponding function
        return {"status": "success", "output": result}
    except Exception as e:
        return {"status": "error", "output": str(e)}

@app.get("/read")
def read_file(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File {path} not found")
    try:
        with open(path, "r") as file:
            return {"content": file.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
