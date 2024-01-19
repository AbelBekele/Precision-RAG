import PyPDF2
from langchain_community.document_loaders import TextLoader

def convert_pdf_to_txt(pdf_path, txt_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF file reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages) ):
            # Extract the text from the page
            text += pdf_reader.pages[page_num].extract_text()


    # Write the text to a text file
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
convert_pdf_to_txt('10_Academy_challenge_doc.pdf', '10_Academy_challenge_doc.txt')


loader = TextLoader("10_Academy_challenge_doc.txt", encoding = 'UTF-8')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")