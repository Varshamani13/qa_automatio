from crewai import Crew, Process
from agents import qa_planner, qa_coder, qa_executor, qa_analyzer
from tasks import planning_task, coding_task, execution_task, analysis_task

qa_crew = Crew(
    agents=[qa_planner, qa_coder, qa_executor, qa_analyzer],
    tasks=[planning_task, coding_task, execution_task, analysis_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

def qa_automation_pipeline_with_crew(feature, document_path):
    print(f"\n=== Starting QA Automation for Feature: {feature} ===")
    result = qa_crew.kickoff(inputs={'feature': feature, 'document_path': document_path})
    with open("test_report.txt", "w") as report:
        report.write(result)
    print("\n=== Test Report Generated ===")

# Example Run
if __name__ == "__main__":
    qa_automation_pipeline_with_crew(feature="Login Functionality", document_path="BRD - HRMS.pdf")
