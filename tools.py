from crewai_tools import DirectoryReadTool, CodeInterpreterTool, CSVSearchTool, CodeDocsSearchTool

# Add document ingestion tool for parsing BRD documents
document_ingestor_tool = CodeDocsSearchTool()

# Initialize QA-specific tools
directory_tool = DirectoryReadTool()

analysis_tool = CSVSearchTool()
execution_tool = CodeInterpreterTool()

