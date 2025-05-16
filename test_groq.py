import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env file
load_dotenv()

# Get the Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")
print(f"Using API key (first 10 chars): {groq_api_key[:10]}...")

try:
    # Initialize the LLM
    print("Initializing Groq LLM...")
    llm = ChatGroq(
        api_key=groq_api_key,
        model_name="llama3-70b-8192"  # Using llama3-70b model
    )
    
    # Create a simple prompt template
    prompt = PromptTemplate(
        input_variables=["movie"],
        template="Write a one-sentence summary for the movie {movie}."
    )
    
    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Test with a simple request
    print("Testing LLM with a simple request...")
    result = chain.invoke({"movie": "The Matrix"})
    
    # Print the result
    print("\nResponse from Groq API:")
    print(result["text"])
    print("\nAPI test successful!")

except Exception as e:
    print(f"\nError communicating with Groq API: {str(e)}")
    import traceback
    print(traceback.format_exc())
