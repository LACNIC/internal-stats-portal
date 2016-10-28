from django.template.defaultfilters import truncatechars


def truncate_text(text, length):
    if text:
        if len(text) > length:
            return truncatechars(text, length)
        else:
            return text
    return ""
