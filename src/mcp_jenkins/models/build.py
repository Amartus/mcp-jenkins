from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Artifact(BaseModel):
    """Represents a build artifact in Jenkins"""
    # In some Jenkins versions / configurations `displayPath` may be null.
    # Accept None here to avoid Pydantic validation errors when the field is missing.
    displayPath: Optional[str] = None
    fileName: str
    relativePath: str


class Build(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    number: int
    url: str

    # The following fields are determined by the depth when get info
    name: Optional[str] = None
    node: Optional[str] = None

    class_: Optional[str] = Field(None, alias='_class')
    building: Optional[bool] = None
    duration: Optional[int] = None
    estimatedDuration: Optional[int] = None
    result: Optional[str] = None
    timestamp: Optional[int] = None
    inProgress: Optional[bool] = None
    artifacts: list[Artifact] = Field(default_factory=list)
    nextBuild: Optional['Build'] = None
    previousBuild: Optional['Build'] = None
