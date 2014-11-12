class BoardError(Exception):
    """
    Parent of all board exceptions
    """
    pass

class OutsideError(BoardError):
    """
    Word is going outside the board
    """
    pass

class TooManyBlanksError(BoardError):
    pass

class InvalidPremiumError(BoardError):
    pass

class MismatchLetterError(BoardError):
    pass
