from dotenv import load_dotenv
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from pinecone import PodSpec
from pinecone import Pinecone as ppincone
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.vectorstores import Pinecone

class KnowledgeAssistant:

    def __init__(self):
        load_dotenv()
        os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
        os.environ["PINECONE_ENV"] = os.getenv("PINECONE_ENV")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

        self.pc = ppincone(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV")
        )
        self.embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.index = self.pc.Index('canopy--document-uploader')

        self.text_field = "text"
        self.vectorstore = Pinecone(self.index, self.embed_model, self.text_field)
        self.chat = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model='gpt-3.5-turbo')

    def augment_prompt(self, query):
        results = self.vectorstore.similarity_search(query, k=3)
        source_knowledge = "\n".join([x.page_content for x in results])
        augmented_prompt = f"""Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {query}"""
        return augmented_prompt

    def run_chat(self, query):
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=f"Hi AI, {query}"),
            AIMessage(content="I'm great thank you. How can I help you?"),
        ]

        augmented_prompt = self.augment_prompt(query)

        prompt = HumanMessage(content=augmented_prompt)
        messages.append(prompt)

        res = self.chat(messages)
        return res.content

# if __name__ == "__main__":
#     assistant = KnowledgeAssistant()
#     query = "Who are the tutors in this week's challenge?"
#     response = assistant.run_chat(query)
#     print(response)

if __name__ == "__main__":
    assistant = KnowledgeAssistant()
    query = "Who are the tutors in this week's challenge?"

    # Get the augmented prompt and source_knowledge
    augmented_prompt, source_knowledge = assistant.augment_prompt(query)

    # Print or use source_knowledge as needed
    print(source_knowledge)