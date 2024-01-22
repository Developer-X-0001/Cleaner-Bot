def format_large_number(number: int):
    # Define the suffixes and their corresponding divisors
    suffixes = ['', 'K', 'M', 'B', 'T']
    divisor = 1000.0

    # Initialize the index and suffix
    index = 0
    while number >= divisor and index < len(suffixes) - 1:
        number /= divisor
        index += 1

    # Format the number with the appropriate suffix
    formatted_number = "{:.1f}{}".format(number, suffixes[index])

    return formatted_number
