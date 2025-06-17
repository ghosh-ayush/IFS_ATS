from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

PROMPT = PromptTemplate(
    input_variables=["job_desc", "context"],
    template=(
        "Using 80% of the provided resume content and allowing up to 20% "
        "reasonable additions, craft an ATS-friendly resume and cover letter.\n"
        "Job description: {job_desc}\n"
        "Relevant resume sections: {context}\n"
        "Return the resume first, then the cover letter."
    ),
)


def make_chain(store):
    """Build a RetrievalQA chain with the configured prompt."""
    llm = ChatOpenAI(model_name="gpt-4o-mini")
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=store.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
    )
