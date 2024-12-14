from crewai import Agent
from tools import directory_tool, document_ingestor_tool, execution_tool, analysis_tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4-0125-preview"

# QA Planner Agent
qa_planner = Agent(
    role='QA Planner',
    goal='Analyze requirements and strategize the testing approach for {feature}.',
    verbose=True,
    memory=True,
    backstory=(
        "An experienced QA strategist skilled in creating comprehensive testing "
        "plans, ensuring coverage for functionality, performance, and edge cases."
    ),
    tools=[directory_tool],
    allow_delegation=True,
)

# QA Coder Agent
qa_coder = Agent(
    role='QA Coder',
    goal='Generate automated test scripts for {feature} based on the planned strategy.',
    verbose=True,
    memory=True,
    backstory=(
        "An automation expert specializing in writing robust test scripts that "
        "cover various scenarios, ensuring compatibility with modern frameworks."
    ),
    tools=[execution_tool],
    allow_delegation=False,
)

# QA Executor Agent
qa_executor = Agent(
    role='QA Executor',
    goal='Set up the testing environment and execute test scripts for {feature}.',
    verbose=True,
    memory=True,
    backstory=(
        "A meticulous execution specialist, adept at managing environments, "
        "running test scripts, and maintaining detailed logs of test runs."
    ),
    tools=[execution_tool],
    allow_delegation=False,
)

# QA Analyzer Agent
qa_analyzer = Agent(
    role='QA Analyzer',
    goal='Evaluate test execution logs and provide insights for {feature}.',
    verbose=True,
    memory=True,
    backstory=(
        "An analytical thinker skilled in interpreting test results, identifying "
        "deficiencies, and recommending improvements for better software quality."
    ),
    tools=[analysis_tool],
    allow_delegation=True,
)