from crewai import Crew, Process
from agents import qa_planner, qa_coder, qa_executor, qa_analyzer, feature_analyzer
from tasks import planning_task, coding_task, execution_task, analysis_task, feature_task

qa_crew = Crew(
    agents=[qa_planner, qa_coder, qa_executor, qa_analyzer],
    tasks=[planning_task, coding_task, execution_task, analysis_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

def extract_features_from_document(document_path):
    # Extract features using the feature_analyzer agent
    print("\n=== Extracting Features from Document ===")
    crew = Crew(
        agents=[feature_analyzer],
        tasks=[feature_task], 
        process=Process.sequential,  
        memory=False,
        cache=False,
        max_rpm=100,
        share_crew=True
    )
    
    # Execute the task with the document
    result = crew.kickoff(inputs={'document_path': document_path})
    
    print("Results from feature extraction:", result)
  
    return result

def execute_test_for_all_features(features, document_path):
   
    print("\n=== Starting Automated Testing for Extracted Features ===")
    
    results = []
    
    print(f"\n=== Starting Test for Feature: {features} ===")
    result = qa_crew.kickoff(inputs={'feature': features, 'document_path': document_path})
    results.append(result)
    
 
    with open("test_report.txt", "w") as report:
        for feature, result in zip([f"{cat} - {ft}" for cat in features for ft in features[cat].keys()], results):
            report.write(f"Feature: {feature}\nResult: {result}\n\n")
    print("\n=== Test Report Generated ===")


if __name__ == "__main__":
    document_path = "BRD - HRMS.pdf"
    
    # Step 1: Extract features from the document (JSON structure with nested categories)
    features = extract_features_from_document(document_path)
    print(type(features))
    
    # Step 2: Execute tests for each feature
    if features:
        execute_test_for_all_features(features, document_path)
    else:
        print("No features extracted from the document.")
