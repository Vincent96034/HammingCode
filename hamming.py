"""This module contains the HammingCode class for encoding and decoding messages using
Hamming code."""

from typing import List
import numpy as np
from models import BinaryMessage


class BitError(Exception):
    """Exception raised when a bit error is detected."""
    pass


class HammingCode:
    """Class for encoding and decoding messages using Hamming code.

    Methods:
        encode(message): Encodes the given message using Hamming code.
        decode(codeword): Decodes the given codeword using Hamming code.
        check_correct(codeword): Checks if the given codeword has any errors and
            corrects them if necessary.
        simulate_1bit_flip(codeword): Simulates a 1-bit flip error in the given codeword.
        simulate_2bit_flip(codeword): Simulates a 2-bit flip error in the given codeword.

    Arguments:
        message_bits (int): The number of message bits.
        mode (str, optional): The mode to run the Hamming code in. Can be either
            `correct` or `detect`. Defaults to `correct`.
            - `correct`: In this mode, the Hamming code will correct any 1-bit errors
                in the code. If there are more than 1-bit errors, the code will not
                be able to correct them and output a wrong message.
            - `detect`: In this mode, the Hamming code will detect any 1-bit or 2-bit
                errors in the code, but it will not correct them.
    """

    def __init__(self, message_bits: int, mode: str = "correct"):
        if mode not in ["correct", "detect"]:
            raise ValueError("Mode must be either `correct` or `detect`")
        self._k = message_bits
        self._p = self._get_min_p_bits(message_bits)
        self._P = self._generate_P()
        self._G = self._generate_G()
        self._H = self._generate_H()
        self.code_rate = message_bits / (message_bits + self._p)
        self.mode = mode

    def encode(self, message: BinaryMessage) -> BinaryMessage:
        """Encodes the given message using Hamming code.

        Args:
            message (ndarray): The message to encode.

        Returns:
            ndarray: The encoded codeword.
        """
        message = self._validate_binary(message)
        codeword = np.dot(self._G, message) % 2
        return BinaryMessage(codeword)

    def decode(self, codeword: BinaryMessage) -> BinaryMessage:
        """Decodes the given codeword using Hamming code.

        Args:
            codeword (ndarray): The codeword to decode.

        Returns:
            ndarray: The decoded message.
        """
        codeword = self._validate_binary(codeword)
        return BinaryMessage(codeword[:self._k])

    def check_correct(self, codeword: BinaryMessage) -> BinaryMessage:
        """Checks if the given codeword has any errors and corrects them if necessary.

        Args:
            codeword (ndarray): The codeword to check.

        Returns:
            ndarray: The corrected codeword.
        """
        codeword = self._validate_binary(codeword)
        error_syndrome = self._get_error_syndrome(codeword)
        error_exists = np.any(error_syndrome)
        if error_exists:
            if self.mode == "detect":
                raise BitError(
                    "1- or 2-bit errors detected! Cannot correct in mode `detect`.")
            error_position = self._get_error_position(error_syndrome)
            codeword = self._correct_error(codeword, error_position)
        return BinaryMessage(codeword)

    def simulate_1bit_flip(self, codeword: BinaryMessage) -> BinaryMessage:
        """Simulates a 1-bit flip error in the given codeword.

        Args:
            codeword (ndarray): The codeword to simulate the error on.

        Returns:
            ndarray: The codeword with the simulated error.
        """
        codeword = self._validate_binary(codeword)
        n = len(codeword)
        e = np.zeros(n)
        e[np.random.randint(n)] = 1
        codeword = (codeword + e) % 2
        return BinaryMessage(codeword)

    def simulate_2bit_flip(self, codeword: BinaryMessage) -> BinaryMessage:
        """Simulates a 2-bit flip error in the given codeword.

        Args:
            codeword (ndarray): The codeword to simulate the error on.

        Returns:
            ndarray: The codeword with the simulated error.
        """
        codeword = self._validate_binary(codeword)
        n = len(codeword)
        e = np.zeros(n)
        e[np.random.randint(n)] = 1
        e[np.random.randint(n)] = 1
        codeword = (codeword + e) % 2
        return BinaryMessage(codeword)

    def _get_min_p_bits(self, nbit: int) -> int:
        """Calculates the minimum number of parity bits required for the given number of
        message bits.

        Args:
            nbit (int): The number of message bits.

        Returns:
            int: The minimum number of parity bits.
        """
        p = 0
        while 2**p - p - 1 < nbit:
            p += 1
        return p

    def _generate_P(self) -> np.ndarray:
        """Generates the P matrix used for encoding.

        Returns:
            ndarray: The P matrix.
        """
        P = np.array([list(map(int, list(bin(i)[2:].zfill(self._p))))
                     for i in range(1, 2**self._p)])
        # remove vectors with only one 1 since they already exist in I_q
        # -> minimum hamming weight of 2 is needed
        P = P[np.sum(P, axis=1) > 1]
        self._P = P[:self._k]
        return self._P

    def _generate_G(self) -> np.ndarray:
        """Generates the G matrix used for encoding.

        Returns:
            ndarray: The G matrix.
        """
        I_k = np.eye(self._k)
        G = np.concatenate((I_k, self._P), axis=1).T
        self._G = G
        return self._G

    def _generate_H(self) -> np.ndarray:
        """Generates the H matrix used for error detection and correction.

        Returns:
            ndarray: The H matrix.
        """
        I_q = np.eye(self._p)
        H = np.concatenate((self._P.T, I_q), axis=1)
        self._H = H
        return self._H

    def _get_error_syndrome(self, codeword: BinaryMessage) -> BinaryMessage:
        """Calculates the error syndrome for the given codeword.

        Args:
            codeword (ndarray): The codeword to calculate the error syndrome for.

        Returns:
            ndarray: The error syndrome.
        """
        return np.dot(self._H, codeword) % 2

    def _get_error_position(self, error_syndrome: BinaryMessage) -> List[int]:
        """Calculates the error position based on the error syndrome.

        Args:
            error_syndrome (ndarray): The error syndrome.

        Returns:
            ndarray: The error position.
        """
        return np.where(np.all(self._H == error_syndrome[:, None], axis=0))[0]

    def _correct_error(self, codeword: BinaryMessage, error_position: int) -> BinaryMessage:
        """Corrects the error in the given codeword at the specified error position.

        Args:
            codeword (ndarray): The codeword to correct.
            error_position (ndarray): The error position.

        Returns:
            ndarray: The corrected codeword.
        """
        codeword[error_position] = int(codeword[error_position]) ^ 1
        return codeword

    def _validate_binary(self, arg):
        """Validates that the given argument is a BinaryMessage.

        Args:
            arg (ndarray): The argument to validate.

        Returns:
            ndarray: The argument as a BinaryMessage.
        """
        if not isinstance(arg, BinaryMessage):
            arg = BinaryMessage(arg)
        return arg
