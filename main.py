from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from PyPDF2 import PdfReader
import re

import os

# # Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "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"

model = ChatOpenAI(
model="openhermes",
base_url="http://127.0.0.1:11434/v1"
)

pdf_path="/content/BRD - HRMS.pdf"


@tool
def fetch_pdf_content(pdf_path: str):
  """
    Extracts and processes text content from a PDF file at the given path.

    Args:
        pdf_path (str): The file path of the PDF to be processed.

    Returns:
        str: The processed text content of the PDF with whitespace removed.
    """
  print(pdf_path)
  with open(pdf_path, "rb") as f:
    pdf = PdfReader(f)
    text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
    processed_text = re.sub(r'\s+', '', text).strip()
    return processed_text
  
pdf_reader = Agent(
role='PDF Content Extractor',
goal='Extract and preprocess text from a PDF located in current local directory',
backstory='Specializes in handling and interpreting PDF documents',
verbose=True,
tools=[fetch_pdf_content],
allow_delegation=False,
llm=model
)


pdf_local_relative_path = "/content/BRD - HRMS.pdf"

def pdf_reading_task(pdf):
  return Task(
  description=f"Read and preprocess the PDF at this local path: {pdf_local_relative_path}",
  agent=pdf_reader,
  expected_output="Extracted and preprocessed text from a PDF",
  )


task_highlights_drafting = Task(
description="Create a list of key features including all the important points based on the extracted PDF content.",
agent=feature_writer,
expected_output="List of key features describing the key points of the PDF",
)

task_reco_generation = Task(
description="Generate a final recommendation on assessment of the expected performance of the fund based on the features.",
agent=reco_creator,
expected_output="An overall recommendation with reasons"
)


crew = Crew(
agents=[pdf_reader, feature_writer, reco_creator],
tasks=[pdf_reading_task(pdf_local_relative_path),
task_highlights_drafting,
task_reco_generation],
verbose=2
)

# Let’s start!
result = crew.kickoff()
print("“ — — — — — — — — — — — — — “")
print(f"”Final result: \n{result}”")

