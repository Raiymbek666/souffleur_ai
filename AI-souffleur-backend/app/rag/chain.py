from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import Runnable

from app.rag.prompts import QUERY_GENERATION_PROMPT, RESPONSE_GENERATION_PROMPT
from app.rag.schema import SuggestionList
from app.rag.user_context import get_formatted_user_context

def _format_chat_history(messages):
    # the recieved messages format to plain text

    role_map = {
        "client": "Пользователь",
        "operator": "Оператор"
    }

    return "\n".join(
        [f"{role_map.get(msg['from'], msg['from'])}: {msg['text']}" for msg in messages]
    )

def _format_chunks_for_prompt(chunks):
    # receives docs from vector store, formats to plain text
    if not chunks:
        return "No relevant documents found"

    return "\n\n---\n\n".join(
        [f"Filename: {chunk['filename']}\nContent: {chunk['text']}\nRelevance Score: {chunk['relevance_score']}" for chunk in chunks]
    )


class RAGChain:
    def __init__(self, llm_client, krb_retriever, mmb_retriever):
        self.llm = llm_client
        self.krb_retriever = krb_retriever
        self.mmb_retriever = mmb_retriever


        llm_structured_output = self.llm.with_structured_output(SuggestionList)

        self.query_generation_chain: Runnable = (
            ChatPromptTemplate.from_template(QUERY_GENERATION_PROMPT)
            | self.llm
            | StrOutputParser()
        )

        self.response_generation_chain: Runnable = (
            ChatPromptTemplate.from_template(RESPONSE_GENERATION_PROMPT)
            | llm_structured_output
        )

    def run_request(self, messages, db, k=3):
        if not messages:
            return []
        
        user_type = messages[0].get("type", "KRB") 
        user_id = messages[0].get("call_id")
        user_context = get_formatted_user_context(db=db, user_type=user_type, user_id=user_id)

        retriever_to_use = None

        if (user_type=="KRB"):
            retriever_to_use = self.krb_retriever
        elif (user_type=="MMB"):
            retriever_to_use = self.mmb_retriever
        else:
            raise Exception("Invalid type in messages")

        formatted_history = _format_chat_history(messages)

        rag_search_query = self.query_generation_chain.invoke(
            {
                "chat_history": formatted_history, 
                "user_context": user_context
            }
        )

        print(f"Generated RAG search query: {rag_search_query}")

        retrieved_chunks = retriever_to_use.retrieve(rag_search_query, k)

        kb_retrieved_information = _format_chunks_for_prompt(retrieved_chunks)

        pydantic_output = self.response_generation_chain.invoke(
            {
                "chat_history": formatted_history, 
                "kb_info": kb_retrieved_information, 
                "user_context": user_context
            }
        )

        suggestions_list = [s.dict() for s in pydantic_output.suggestions]

        return suggestions_list