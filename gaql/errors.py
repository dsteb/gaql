"""
    Module with User-defined errors and exceptions
"""


class AttributeValueException(Exception):
    """
        Error occured on getting the value of the attribute
    """


class ParseSelectException(Exception):
    """
        Exception occured on parsing select attributes
    """
