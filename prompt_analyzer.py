# -*- coding: utf-8 -*-
"""Prompt-Analyzer

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11HtllrZoyThsWZipDeJ9qN6Hu5Oztntu
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv
import json


os.environ['OPENAI_API_KEY'] = ""

# Initialize OpenAI client
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# output schemas
response_schemas = [
    ResponseSchema(
        name="output_type",
        description="The type of output required: 'string' for single record, 'dataframe' for multiple records, or 'plot' for visualizations"
    ),
    ResponseSchema(
        name="explanation",
        description="Brief explanation of why this output type was chosen"
    )
]

# output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are a data analysis expert. Analyze the following user query and determine what type of output would be most appropriate.

User Query: {query}

Guidelines:
- If the user is asking about a single record or piece of information, respond with 'string'
- If the user is asking about multiple records or needs tabular data, respond with 'dataframe'
- If the user is requesting any kind of visualization or comparison, respond with 'plot'

{format_instructions}
""")

def analyze_prompt(user_query):
    """
    Analyzes a user query and determines the appropriate output type.

    Args:
        user_query (str): The user's data query

    Returns:
        dict: A dictionary containing output_type and explanation
    """
    format_instructions = output_parser.get_format_instructions()
    prompt = prompt_template.format(
        query=user_query,
        format_instructions=format_instructions
    )

    response = llm.invoke(prompt)
    parsed_response = output_parser.parse(response.content)

    return parsed_response

def test_analyzer():
    """
    Test function to demonstrate the prompt analyzer with sample queries.
    """
    test_queries = [
        "What is the average age of employees?",
        "Show me all sales records from last month",
        "Can you create a bar chart of product sales by category?"
    ]

    for query in test_queries:
        result = analyze_prompt(query)
        print(f"Query: {query}")
        print(f"Analysis: {json.dumps(result, indent=2)}")
        print()

# Example of how the analyzer could be integrated into a pipeline
def process_query(query):
    """
    Process a query through the appropriate pipeline based on the analysis.

    Args:
        query (str): The user's data query

    Returns:
        str: Description of which pipeline would be executed
    """
    analysis = analyze_prompt(query)
    output_type = analysis['output_type']

    if output_type == 'string':
        return f"Executing string pipeline for query: {query}"
    elif output_type == 'dataframe':
        return f"Executing dataframe pipeline for query: {query}"
    elif output_type == 'plot':
        return f"Executing plot pipeline for query: {query}"
    else:
        return f"Unknown output type: {output_type}"

# Main execution
if __name__ == "__main__":
    print("Testing prompt analyzer:")
    test_analyzer()

    print("\nTesting pipeline processing:")
    test_pipeline_queries = [
        "What is the highest sales value?",
        "List all employees in the marketing department",
        "Show a pie chart of revenue by region"
    ]

    for query in test_pipeline_queries:
        result = process_query(query)
        print(result)

!pip install langchain-openai langchain pandas  openai langchain-community