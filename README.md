## Task Outline

The objective is implementing and testing linear error-correcting codes, specifically the error correction codes developed by Richard W. Hamming in 1950. This coding scheme is designed to address issues in data transmission and storage systems by either detecting up to two-bit errors or correcting single-bit errors. This Python project implements the hamming code functionalities in a generalized manner.

## Project Structure

The package consists of four main components:

1. `hamming.py`: Implements the core functionality of Hamming code.
2. `models.py`: Defines the `BinaryMessage` class for handling binary data.
3. `transmission.py`: Provides functions for simulating the transmission of messages over a noisy channel.
4. `main.ipynb`: A Jupyter notebook for demonstration and testing.

## Hamming Code Implementation

The `hamming.py` module is the core of the project, offering functionalities for encoding and decoding messages as well as detecting and correcting errors using the Hamming code. It uses the custom data model `BinaryMessage` for all operations on binary data.

### Key Components

- **HammingCode Class**: Encapsulates the encoding and decoding logic. It has methods for encoding messages, decoding codewords, and handling errors.
- **BinaryMessage Object**: This object extends NumPy’s `ndarray` and is used for all binary operations within the HammingCode class and ensures that the data is indeed binary.

The Implementation allows to choose between two modes: `detect` and `correct` mode. In  the `detect` mode, the Hamming code is used to detect the presence of errors in the codeword. It can identify single-bit and two-bit errors but does not correct them. This mode is useful for systems where error detection is sufficient or where an external error handling mechanism is employed. The `detect` mode enables the Hamming code to also correct any single-bit error in the codeword. In this mode, two-bit errors can not be sufficiently detected. This mode is useful when 2 bit errors are very unlikely and the transmitted codeword should be corrected.

Our implementation of the HammingCode class lets the user dynamically configure the length of the message (in bits). The system then computes the minimum number of parity bits (`p`) required for the given message length. The code rate, a measure of the efficiency of the code, is calculated as the ratio of message bits to the total bits in the codeword (message bits + parity bits). A higher code rate indicates a more efficient encoding but may reduce the error-correcting capability. This is an important trade off: we can increase the code efficiency, meaning we need less parity check bits for each message, but this increases the likelihood of a two bit error (which we can not correct any more) in the codeword.

The following matrices are calculated for a given HammingCode instance:

- **Parity Matrix (P)**: A matrix that helps in constructing the Generator Matrix and is key to determining the positions of parity bits in the codeword.
- **Generator Matrix (G)**: Vital for encoding messages. It transforms the message into a codeword by adding parity bits.
- **Parity-Check Matrix (H)**: Used for error detection and correction. It is instrumental in identifying the syndrome or pattern of errors in a codeword.

## Transmission Simulation

This module simulates the practical application of the Hamming code in a noisy channel transmission scenario. The process of transmitting over a noisy channel is simulated in several steps, from encoding to decoding of the message. Messages are converted to binary using the Hamming code and then transmitted. This step simulates the addition of parity bits and preparation of the codeword. During transmission, the codeword may be subjected to errors, simulating real-world interferences. Upon receiving the codeword, the system decodes it back to the original message. It also checks and corrects any errors if in "Correct" mode or detects errors in "Detect" mode. This end-to-end simulation demonstrates the robustness of the Hamming code in maintaining data integrity in noisy transmission environments.

## How to use

The notebook `main.ipynb` guides you through this entire end-to-end process. You can try out different configurations there.
