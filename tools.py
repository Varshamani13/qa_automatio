from crewai_tools import DirectoryReadTool, CodeInterpreterTool, CSVSearchTool, CodeDocsSearchTool,PDFSearchTool

# Add document ingestion tool for parsing BRD documents
document_ingestor_tool = CodeDocsSearchTool()
pdf_search_tool = PDFSearchTool(pdf='BRD - HRMS.pdf')
# Initialize QA-specific tools
directory_tool = DirectoryReadTool()

analysis_tool = CSVSearchTool()
execution_tool = CodeInterpreterTool()

