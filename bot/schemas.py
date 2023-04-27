from typing import NamedTuple


class TemporaryReminder(NamedTuple):
    id: int
    title: str
    type: str
    is_done: bool
    date: str


class PermanentReminder(NamedTuple):
    id: int
    title: str
    type: str
    is_done: bool
    frequency: int
    date: str


class Bookmark(NamedTuple):
    id: int
    title: str
    type: str
    is_done: bool
