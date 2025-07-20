from enum import StrEnum

class Answer(StrEnum):
    """
    Enum representing the possible answers to a question.
    """
    YES = "yes"
    NO = "no"
    NO_ANSWER = "no answer"

    def __str__(self) -> str:
        return self.value
    
    def get_values(self) -> list[str]:
        """
        Get the values of the enum as a list.
        
        Returns:
            list[str]: List of enum values.
        """
        return [self.YES, self.NO, self.MAYBE]