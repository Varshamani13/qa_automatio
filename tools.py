from crewai_tools import DirectoryReadTool, CodeInterpreterTool, CSVSearchTool, CodeDocsSearchTool,PDFSearchTool

document_ingestor_tool = CodeDocsSearchTool()
pdf_search_tool = PDFSearchTool(pdf='BRD - HRMS.pdf')

directory_tool = DirectoryReadTool()

analysis_tool = CSVSearchTool()
execution_tool = CodeInterpreterTool()

