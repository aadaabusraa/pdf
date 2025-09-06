from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from scrape import get_pdf_chunks 

template = (
    "Answer only in Turkish language. "
    "If your answer is in English, translate it to Turkish first before answering."
    "You are tasked with extracting specific information from the following text content: {content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3")

def parse_with_ollama(pdf_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(pdf_chunks, start=1):
        response = chain.invoke(
            {"content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(pdf_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
