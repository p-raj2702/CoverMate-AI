import os
import faiss
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from utils import extract_text_from_pdf
from sklearn.metrics.pairwise import cosine_similarity

# 🔐 Set your Gemini API Key
genai.configure(api_key="AIzaSyCnwh66Ba-kHUm2ySC3L_ui10sIczmzHug")

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Gemini model
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")


# Constants
TOP_K = 5

def embed_clauses(clauses):
    embeddings = model.encode(clauses)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings

def chunk_text(text, max_len=500):
    import re
    clauses = re.split(r'\n{2,}|\.\s', text)
    return [clause.strip() for clause in clauses if len(clause.strip()) > 20]

def query_chunks(question, clauses, embeddings):
    question_embedding = model.encode([question])
    similarities = cosine_similarity([question_embedding[0]], embeddings)[0]
    top_k_idx = similarities.argsort()[::-1][:TOP_K]
    top_k_clauses = [clauses[i] for i in top_k_idx]
    return "\n".join(top_k_clauses)

def answer_with_gemini(question, context):
    prompt = f"""You are an insurance assistant AI. Based on the policy clauses provided, answer the question factually and clearly.

Policy Clauses:
{context}

Question: {question}
Answer:"""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def process_document_and_questions(pdf_url, questions):
    # Step 1: Extract and chunk
    text = extract_text_from_pdf(pdf_url)
    clauses = chunk_text(text)

    # Step 2: Embed
    index, embeddings = embed_clauses(clauses)

    # Step 3: Answer questions
    final_answers = []
    for q in questions:
        context = query_chunks(q, clauses, embeddings)
        answer = answer_with_gemini(q, context)
        final_answers.append(answer)

    return final_answers

# 🔁 Final public method used in FastAPI
def process_query(pdf_url, questions):
    try:
        return process_document_and_questions(pdf_url, questions)
    except Exception as e:
        return [f"Processing failed: {str(e)}"] * len(questions)