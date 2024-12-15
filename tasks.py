from crewai import Task
from tools import document_ingestor_tool, execution_tool, directory_tool, analysis_tool,pdf_search_tool
from agents import qa_analyzer, qa_coder, qa_executor, qa_planner,feature_analyzer
from fpdf import FPDF
import requests



# Task: Analysis
feature_task = Task(
    name='Analysis Task',
    description='Analyze the given document and extract the features to be tested.',
    tools=[pdf_search_tool],
    verbose=True,
    memory=True,
    backstory=(
        "An analytical thinker skilled in interpreting test results, identifying "
        "deficiencies, and recommending improvements for better software quality."
    ),
    expected_output="the extracted features from the document.the type of output should be in string",
   
    allow_delegation=True,
    agent=feature_analyzer,
)

# Task: Planning
planning_task = Task(
    name='Planning Task',
    description='Analyze BRD document and strategize testing approach.',
    tools=[pdf_search_tool],
 
    backstory=(
        "An experienced QA strategist skilled in creating comprehensive testing "
        "plans, ensuring coverage for functionality, performance, and edge cases."
    ),
    expected_output="A detailed test strategy with defined testing approach, scope, and coverage.",
    allow_delegation=True,
    agent=qa_planner,
)

# Task: Coding
# coding_task = Task(
#     name='Coding Task',
#     description='Generate automated test scripts based on user stories.',
#     tools=[execution_tool],
#     execution_function=lambda inputs: f"Generated test scripts for {inputs['features']}.",
#     verbose=True,
#     memory=True,
#     backstory=(
#         "An automation expert specializing in writing robust test scripts that "
#         "cover various scenarios, ensuring compatibility with modern frameworks."
#     ),
#     expected_output="Automated test scripts covering functional and edge case scenarios.",
#     allow_delegation=True,
#     agent=qa_coder,
# )
coding_task = Task(
    description="Generate automated test scripts based on features",
    agent=qa_coder,
    backstory=(
        "An automation expert specializing in writing robust test scripts that "
        "cover various scenarios, ensuring compatibility with modern frameworks."
    ),
    expected_output="Automated test scripts covering functional and edge case scenarios.",
)
# Task: Execution
execution_task = Task(
    name='Execution Task',
    description='Set up environment and execute test scripts.',
    tools=[execution_tool],
  
    verbose=True,
    memory=True,
    backstory=(
        "A meticulous execution specialist, adept at managing environments, "
        "running test scripts, and maintaining detailed logs of test runs."
    ),
    expected_output="Test execution results, including logs and passed/failed status.",
    allow_delegation=True,
    agent=qa_executor,
)

# Task: Analysis
analysis_task = Task(
    name='Analysis Task',
    description='Analyze test results and provide insights.',
    tools=[analysis_tool],
    execution_function=lambda inputs: generate_pdf_report(inputs['features']),
    verbose=True,
    memory=True,
    backstory=(
        "An analytical thinker skilled in interpreting test results, identifying "
        "deficiencies, and recommending improvements for better software quality."
    ),
    expected_output="Test analysis report in PDF format with insights on test coverage, issues, and recommendations.",
    async_execution=False, 
    output_file='analysis_report.pdf',  
    allow_delegation=True,
    agent=qa_analyzer,
)

def generate_pdf_report(feature):
   
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

 
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Test Analysis Report for {feature}", ln=True, align="C")

    pdf.ln(10)  
    pdf.multi_cell(0, 10, txt=f"Insights and analysis for {feature}: This is where the detailed analysis would go.")

  
    pdf.output("analysis_report.pdf")

    return "PDF report generated successfully."


def execute_test_script_on_server(feature, url="http://3.83.24.72:8000/"):
    credentials = {'user': 'user', 'password': 'letuserpass'}
    headers = {'Content-Type': 'application/json'}
    
    try:
       
        response = requests.post(
            f"{url}/execute-test",  
            json={'feature': feature},
            auth=(credentials['user'], credentials['password']),
            headers=headers
        )
        
        if response.status_code == 200:
            return f"Test execution triggered successfully for {feature}."
        else:
            return f"Failed to trigger test execution for {feature}. Response: {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

