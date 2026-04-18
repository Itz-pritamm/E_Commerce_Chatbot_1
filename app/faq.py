import pandas as pd
from pathlib import Path
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


faqs_path=Path(__file__).parent / "resources" / "faq_data.csv"
chroma_client=chromadb.Client()
collection_name="faqs"



def ingest_faq_data(path):
    if collection_name not in [c.name for c in chroma_client.list_collections()]:
        print(" you are ingesting the data")
        collection=chroma_client.get_or_create_collection(
            name=collection_name
        )
        df=pd.read_csv(path)
        docs=df["question"].to_list()
        metadata=[{"answer":ans} for ans in df["answer"].to_list()]
        ids=[f"id_{i}" for i in range(len(docs))]


        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
    else:
        print(f"collection already exist{collection_name}")


def get_relevant_qa(query):
    collection=chroma_client.get_collection(name=collection_name)
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result



def  faq_chain(query):
    result=get_relevant_qa(query)
    context=''.join([r.get("answer") for r in result["metadatas"][0]])
    answer=generate_answer(query,context)
    return answer

def generate_answer(query,context):
    prompt=f"""given the question below,generate the answer based on the context only.
    if you don't find the answer inside the context then say "i don't know"  .
    don not make things up.
    
    questions:{query}

    context:{context}

    
    
    """
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": prompt,
            }
        ],
        model=os.environ ['GROQ_MODEL'],
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    ingest_faq_data(faqs_path)

    query = "what returning steps"
    #result = get_relevant_qa(query)
    answer=faq_chain(query)

    print(answer)