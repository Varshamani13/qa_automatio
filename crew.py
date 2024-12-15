from fastapi import FastAPI, File, UploadFile, HTTPException
from crewai import Crew, Process
from agents import qa_planner, qa_coder, qa_executor, qa_analyzer, feature_analyzer
from tasks import planning_task, coding_task, execution_task, analysis_task, feature_task
import os
import shutil
import uvicorn

app = FastAPI()

# Initialize the QA Crew
qa_crew = Crew(
    agents=[feature_analyzer, qa_planner, qa_coder, qa_executor, qa_analyzer],
    tasks=[feature_task, planning_task, coding_task, execution_task, analysis_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-and-test")
async def upload_and_test(file: UploadFile = File(...)):
    """
    Upload a document, extract features, and run tests on it.
    """
    try:
        # Save uploaded file to the server
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print(f"Uploaded file saved to: {file_path}")

        # Step 1: Extract features from the document
        print("\n=== Extracting Features from Document ===")
        feature_result = qa_crew.kickoff(inputs={"document_path": file_path})

        if not feature_result:
            raise HTTPException(status_code=500, detail="Feature extraction failed.")

        print("Features extracted successfully.")

        # Step 2: Execute tests for all extracted features
        print("\n=== Starting Automated Testing ===")
        test_results = qa_crew.kickoff(inputs={"document_path": file_path})

        # Save test results to a report file
        report_path = os.path.join(UPLOAD_DIR, "test_report.txt")
        with open(report_path, "w") as report:
            report.write(f"Test Results:\n{test_results}\n")

        print(f"Test report generated at: {report_path}")

        return {
            "message": "Testing completed successfully.",
            "test_report_path": report_path,
        }

    except Exception as e:
        print(f"Error during processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during processing.")


if __name__ == "__main__":
    uvicorn.run("crew:app", host="0.0.0.0", port=8000)
