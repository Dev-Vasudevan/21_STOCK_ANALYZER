import openai
import PyPDF2
import pdfplumber
from langchain.document_loaders import PyPDFLoader

openai.api_key = "API_KEY"

def extract_text_from_pdf(pdf_path):

    pdf_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text()
    return pdf_text

def ask_question(question, context):

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Read the following text and answer the question:\n{context}\n\nQuestion: {question}\nAnswer:",
        max_tokens=100,
        temperature=1,
        stop=None
    )
    answer = response.choices[0].text.strip()
    return answer

def save_qa_history(question, answer):


    with open("qa_history.txt", "a") as f:
        f.write(f"{question}\n{answer}\n")

def load_qa_history():


    qa_history = []
    with open("qa_history.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            qa_history.append((line.split("\n")[0], line.split("\n")[1]))
    return qa_history

def main():

    loader = PyPDFLoader("Meta-12.31.2022-Exhibit-99.1-FINAL.pdf")
    pdf_text = loader.load_and_split()[0:5]

    qa_history = load_qa_history()

    while True:
        question = input("Enter a question or type \"quit\": ")
        if question == "quit":
            break

        answer = None
        for q, a in qa_history:
            if q == question:
                answer = a
                break

        if answer is None:
            answer = ask_question(question, pdf_text)

        save_qa_history(question, answer)

        print("Answer:", answer)

if __name__ == "__main__":
    main()
