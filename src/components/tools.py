from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from src.components.llm_instance import llm

def summarizer_fn(text: str) -> str:
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant that summarizes content."},
        {"role": "user", "content": f"Summarize this:\n{text}"}
    ])
    return response.content if hasattr(response, "content") else response


def legal_drafting_fn(instruction: str) -> str:
    """
    Drafts legal documents based on the given instruction and context.
    """
    response = llm.invoke([
        {
            "role": "system",
            "content": (
                "You are a senior legal draftsman with expertise in Indian legal formats. "
                "Your job is to prepare accurate, formal legal drafts that comply with Indian law. "
                "Always include:\n"
                "1. Proper headings (e.g., 'IN THE COURT OF...', 'LEGAL NOTICE')\n"
                "2. Parties involved (with placeholders like [Name], [Address])\n"
                "3. Facts of the case\n"
                "4. Legal grounds / references to statutes or case law if relevant\n"
                "5. Relief sought / demand\n"
                "6. Signature & date block\n"
                "Maintain professional tone and formatting."
            )
        },
        {
            "role": "user",
            "content": f"Draft the following legal document:\n\n{instruction}"
        }
    ])

    return response.content if hasattr(response, "content") else response


summarizer_tool = Tool.from_function(
    name="Summarizer",
    description="Use this tool to summarize any text input.",
    func=summarizer_fn
)


legal_drafting_tool = Tool.from_function(
    name="LegalDrafting",
    description="Drafts formal legal documents such as notices, petitions, agreements, and affidavits.",
    func=legal_drafting_fn
)