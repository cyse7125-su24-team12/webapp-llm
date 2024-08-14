# Import necessary libraries and load your model here


from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os

index_name = "csye7125-chunks-250"
namespace = "default"
print(os.getenv("GROQ_API_KEY"))
print(os.getenv("PINECONE_API_KEY"))
print(os.getenv("HFACE_API_TOKEN"))
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Set up the embedding model to use via Hugging Face Inference API
embeddings = HuggingFaceEndpointEmbeddings(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",  # Public model name on Hugging Face
    huggingfacehub_api_token=os.getenv("HFACE_API_TOKEN")  # Your Hugging Face API token
)


# Create an index if it does not exist
existing_indexes = [ index.name for index in pinecone.list_indexes() ]
index = pinecone.Index(index_name)

db = PineconeVectorStore(
    index=index,
    namespace=namespace,
    embedding=embeddings
)

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

retriever = db.as_retriever()
# retriever.search_kwargs = {"k": 15} 

# Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# result = qa_chain.run("what is the scope and attack vector of SINEC NMS vulnerability?")
# Query FAISS and retrieve documents

# print(result)

def generate_response(prompt):
    # Your model logic here
    try :
        response = qa_chain.invoke(prompt)  # Placeholder response
    except Exception as e:
        response = f"Error: {e}"
    return response
