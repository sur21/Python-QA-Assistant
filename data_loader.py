import os
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from tqdm import tqdm

load_dotenv()

def clean_html(text):
    if not isinstance(text, str):
        return ""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def prepare_documents(sample_size=8000):
    print("Loading Questions.csv...")
    questions = pd.read_csv('data/Questions.csv', encoding='ISO-8859-1')
    
    print("Loading Answers.csv...")
    answers = pd.read_csv('data/Answers.csv', encoding='ISO-8859-1')
    
    qa_pairs = answers.merge(questions, left_on='ParentId', right_on='Id', suffixes=('_ans', '_q'))
    qa_pairs = qa_pairs[qa_pairs['Score_q'] > 1].sort_values('Score_q', ascending=False)
    
    documents = []
    print("Creating documents...")
    for _, row in tqdm(qa_pairs.iterrows(), total=min(len(qa_pairs), sample_size)):
        if len(documents) >= sample_size:
            break
        q_body = clean_html(row['Body_q'])
        a_body = clean_html(row['Body_ans'])
        
        content = f"""Title: {row['Title']}
Question: {q_body}
Top Answer: {a_body}"""
        
        metadata = {"question_id": int(row['Id_q']), "score": int(row['Score_q'])}
        documents.append({"page_content": content, "metadata": metadata})
    
    print(f"Prepared {len(documents)} documents")
    return documents
