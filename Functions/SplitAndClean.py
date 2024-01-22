import re

def split_and_clean(input_string: str):
    # Split the input string using both commas and spaces as separators
    words = re.split(r',|\s', input_string)

    # Remove leading and trailing whitespaces from each word
    word_list = [word.strip() for word in words]

    # Filter out empty strings
    word_list = list(filter(None, word_list))

    return word_list