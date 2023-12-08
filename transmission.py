"""This module contains functions for a simple hamming code use-case of transmitting
messages over a noisy channel. The functions handle encoding and decoding of strings to
bits as well as simulating errors in the transmission."""

import random
import numpy as np
from models import BinaryMessage


def str2bit(message: str) -> list:
    """Convert a string message to a list of binary digits.

    Args:
        message (str): The input string message.

    Returns:
        list: A list of binary digits representing the input message.
    """
    binary_digits = []
    for char in message:
        # Convert each character to a binary string and then to individual digits
        binary_digits.extend([int(bit)
                              for bit in format(ord(char), '08b')])
    return BinaryMessage(binary_digits)


def bit2str(binary_digits: list) -> str:
    """Converts a list of binary digits to a string of ASCII characters.

    Args:
        binary_digits (list): A list of binary digits.

    Returns:
        str: The converted string of ASCII characters.
    """
    string = ''
    for i in range(0, len(binary_digits), 8):
        # Take 8 bits at a time and convert them to a string
        byte = binary_digits[i:i+8]
        ascii_char = chr(int(''.join(map(str, byte)), 2))
        string += ascii_char
    return string


def pad_last_chunk(binary_digits, chunk_size):
    """Pads the last chunk of binary digits with zeros if it is not the full size. This is
    used for transmitting messages that are not a multiple of the chunk size. The padding
    needs to be removed before decoding the message back to ASCII.

    Args:
        binary_digits (list): The list of binary digits.
        chunk_size (int): The size of each chunk.

    Returns:
        tuple: A tuple containing the padded binary digits and the number of zeros added.
    """
    last_chunk_length = len(binary_digits) % chunk_size
    # If the last chunk is not the full size, pad it
    if last_chunk_length > 0:
        padding_needed = chunk_size - last_chunk_length
        binary_digits.extend([0] * padding_needed)
    else:
        padding_needed = 0
    return binary_digits, padding_needed


def list_to_chunks(lst, n):
    """Splits a list of values into multiple lists of size n (chunks).

    Args:
        lst (list): The list to be split into chunks.
        n (int): The size of each chunk.

    Returns:
        list: A list of chunks, where each chunk has size n.
    """
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i+n])
    return result


def chunks_to_list(chunks):
    """Converts a list of chunks into a single list. In other words, flattens the list.

    Args:
        chunks (list): A list of chunks, where each chunk is a list.

    Returns:
        list: A single list containing all the elements from the input chunks.
    """
    result = []
    for chunk in chunks:
        result.extend(chunk)
    return result


def generate_single_bit_error(message: BinaryMessage, error_probability: float) -> BinaryMessage:
    """Generates a binary error matrix with 1-bit errors based on the given message and
    error probability.

    Args:
        message (BinaryMessage): The binary message to introduce errors into.
        error_probability (float): The probability of introducing a 1-bit error in each position.

    Returns:
        BinaryMessage: The binary error matrix with 1-bit errors.
    """
    if not 0 <= error_probability <= 1:
        raise ValueError("Error probability must be between 0 and 1")

    error_matrix = np.zeros_like(message)
    for row in range(message.shape[0]):
        # Decide whether to introduce an error in this row
        if random.random() < error_probability:
            # Select a random position in the row to indicate the error
            error_position = random.randint(0, message.shape[1] - 1)
            error_matrix[row, error_position] = 1  # Marking the error position
    return error_matrix


def generate_multi_bit_error(message: BinaryMessage, error_probability: float) -> BinaryMessage:
    """Generates a multi-bit error matrix based on the given message and error
    probability.

    Args:
        message (BinaryMessage): The original binary message.
        error_probability (float): The probability of a bit being flipped.

    Returns:
        BinaryMessage: The error matrix with flipped bits based on the error probability.
    """
    if not 0 <= error_probability <= 1:
        raise ValueError("Error probability must be between 0 and 1")

    error_matrix = np.zeros_like(message)
    # flip all bits in the error message with error_probability
    for row in range(message.shape[0]):
        for col in range(message.shape[1]):
            if random.random() < error_probability:
                error_matrix[row, col] = 1
    return error_matrix
