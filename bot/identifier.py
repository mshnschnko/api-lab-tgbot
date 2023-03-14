from typing import Optional, Tuple, Union


def reminder_recognize_from_id(data: Optional[str]) -> Tuple[str, int]:
    text = str(data)
    try:
        row_id = int(text.split('id:')[1])
        return text, row_id
    except:
        return "Unspecified identificator", 0
