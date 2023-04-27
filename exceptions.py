"""Custom apps exceptions"""


class NotCorrectMessage(Exception):
    """Incorrect message from user, which cannot be parsed"""
    pass


class NotConsistInDB(Exception):
    """incorrect message to bot when remind doesn't find in db"""
    pass
