from datetime import datetime

def convertDateToDatetime(date: str) -> datetime:
    """
    Given a timestamp string, convert to a datetime object.
    """
    milliseconds_length = len(date.split('.')[-1])

    # The string dates we get vary, so we have to sanitize to 3 places and 'Z'
    # Truncate if more than 3 places & 'Z', else pad zeroes
    if '.' in date:
        if milliseconds_length > 4:
            dotInd = date.find('.')
            date = date[:dotInd + 4] + date[-1]
        elif milliseconds_length < 4:
            date = date[:-1] + '0' * (4 - milliseconds_length) + date[-1]
    else:
        # There is no decimal portion, so we have to add it
        date = date[:-1] + ".000" + date[-1]

    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")