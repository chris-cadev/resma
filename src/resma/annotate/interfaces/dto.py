from dataclasses import dataclass


@dataclass
class TemplateDTO:
    filepath: str
    content: str
