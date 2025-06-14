from pydantic import BaseModel, Field, confloat
from typing import List, Literal

class Suggestion(BaseModel):
    
    text: str = Field(description="The suggested text for the operator.")

    type: Literal["answer", "clarifying_question"] = Field(description="The type of suggestion.")
    
    source: str = Field(description="The source filename")

    confidence: float = Field(
        description="The confidence that the suggestion is truthful and relevant, on a scale of 0.0 to 1.0. This is based on the retriever's relevance score and the model's own semantic assessment."
    )

class SuggestionList(BaseModel):
    suggestions: List[Suggestion] = Field(description="A list of 2-3 helpful suggestions.")