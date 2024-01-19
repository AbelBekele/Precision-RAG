from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import PineconeStore
from langchain.document_loaders.fs.pdf import PDFLoader
from langchain.document_loaders.fs.directory import DirectoryLoader
from langchain.utils.pinecone_client import pinecone

PINECONE_INDEX_NAME = "10-academy"
PINECONE_NAME_SPACE = "10-academy"
# Name of directory to retrieve your files from
# Make sure to add your PDF files inside the 'docs' folder
file_path = 'docs'

def run():
    try:
        # load raw docs from all files in the directory
        directory_loader = PDFLoader("./docs/10_Academy_challenge_doc.pdf")

        raw_docs = directory_loader.load()

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        docs = text_splitter.split_documents(raw_docs)
        print('split docs', docs)

        print('creating vector store...')
        # create and store the embeddings in the vector store
        embeddings = OpenAIEmbeddings()
        index = pinecone.Index(PINECONE_INDEX_NAME)  # change to your own index name

        # embed the PDF documents
        PineconeStore.from_documents(docs, embeddings, {
            'pineconeIndex': index,
            'namespace': PINECONE_NAME_SPACE,
            'textKey': 'text',
        })
    except Exception as error:
        print('error', error)
        raise Exception('Failed to ingest your data')

if __name__ == "__main__":
    run()
    print('ingestion complete')
