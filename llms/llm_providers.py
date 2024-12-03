from gradio_client import Client, file
from llms.prompts.system import VISION_PREFIX, PDF_PREFIX
import json
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms.llamacpp import LlamaCpp
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.llm import LLMChain
from pprint import pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.prompts import PromptTemplate




FILE_PATH = "./uploads/"


# class SentenceTransformerEmbeddings(Embeddings):
#     def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)

#     def embed_documents(self, texts):
#         return self.model.encode(texts, convert_to_tensor=True)

#     def embed_query(self, text):
#         return self.model.encode(text, convert_to_tensor=True)



def get_vision_inference(filename):
    FILENAME = filename

    print(FILE_PATH+FILENAME)
    client = Client("HuggingFaceTB/SmolVLM")
    result = client.predict(
            input_dict={"text":VISION_PREFIX,"files":[file(FILE_PATH+FILENAME)]},
            decoding_strategy="Greedy",
            temperature=0.4,
            max_new_tokens=512,
            repetition_penalty=1.2,
            top_p=0.8,
            api_name="/chat",

    )

    result = json.loads(result)


    return result


def get_rag_inference(filename):
    FILENAME = filename
    #getting file texts

    texts = PyPDFLoader(file_path=FILE_PATH+FILENAME,).load()

    pages = []

    for page in texts:
        pages.append(page)


    embeddings = SentenceTransformerEmbeddings()

    print(embeddings.model_name)


    vector_store = InMemoryVectorStore.from_documents(pages, embeddings)

    docs = vector_store.similarity_search(query=PDF_PREFIX, k=5)
    # for doc in docs:
    #     print(f'Page {doc.metadata["page"]}: {doc.page_content[:300]}\n')    

    llm = LlamaCpp(
        model_path = "llms/models/llama-3.2-1b-instruct-q8_0.gguf",
        temperature=0.3,
        max_tokens=2000        
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="Contexto: {context}\n\nPregunta: {question}"
    )       

    chain = LLMChain(llm=llm, prompt=prompt ,verbose=True,)

    inputs = [{"context": doc.page_content, "question": PDF_PREFIX} for doc in docs]


    result = chain.apply(inputs)
    

    print(result)

    return result[0]





