# -*- coding: utf-8 -*-
from fpdf import FPDF
import random

import nltk
from nltk.corpus import words

# Download the words corpus if not already downloaded
nltk.download("words")


def create_pdf(words):
    """
    This function creates a PDF named 'output.pdf' with a list of the alphabet
    at the top. Below the alphabet, the words in the argument are printed in a
    paragraph format. It also adds בס"ד in 8 point font in the top right of the first page.
    """

    # Creating instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font to Times New Roman
    pdf.set_font("Times", size=14)

    # Add a cell with the alphabet
    alphabet = " ".join([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    pdf.cell(200, 10, text=alphabet, ln=1, align="C")

    # Add בס"ד in 8 point font in the top right of the first page
    pdf.add_font("NotoSansHebrew", "", "NotoSansHebrew.ttf", uni=True)
    pdf.set_font("NotoSansHebrew", "", 8)
    pdf.set_xy(170, 10)
    pdf.cell(20, 0, text='ד"סב', align="R")

    # Set margins for the paragraph
    pdf.set_left_margin(30)
    pdf.set_right_margin(30)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_xy(30, 20)

    # Set font and add a cell for the paragraph of words
    pdf.set_font("Times", size=24)
    paragraph = " ".join(words)
    pdf.multi_cell(0, 10, text=paragraph)

    # Save the pdf with name .pdf
    pdf.output("output.pdf")


def intersperse_true_values(e, t):
    """
    This function creates a list of boolean values with a specified number of
    True values evenly interspersed among False values.
    """
    # Calculate the size of each mini list
    mini_list_size = e // t
    # Calculate the remainder
    remainder = e % t

    # Initialize the final list
    final_list = []

    # Create each mini list
    for _ in range(t):
        # Initialize the mini list with all False
        mini_list = [False] * mini_list_size
        # If there is a remainder, add an extra False to the mini list
        if remainder > 0:
            mini_list.append(False)
            remainder -= 1
        # Randomly choose an index to be True
        true_index = random.randint(0, len(mini_list) - 1)
        mini_list[true_index] = True
        # Append the mini list to the final list
        final_list.extend(mini_list)

    return final_list


def generate_word(length, current_letter, add_letter):
    """
    This function generates a single gibberish word of a given length.
    """
    vowels = "aeiou".replace(current_letter, "")
    consonants = "bcdfghjklmnpqrstvwxyz".replace(current_letter, "")
    word = ""
    forbidden_combinations = [
        "bx",
        "cj",
        "cv",
        "cx",
        "dx",
        "fq",
        "fx",
        "gq",
        "gx",
        "hx",
        "jc",
        "jf",
        "jg",
        "jq",
        "js",
        "jv",
        "jx",
        "jz",
        "kq",
        "kx",
        "mx",
        "px",
        "pz",
        "qb",
        "qc",
        "qd",
        "qf",
        "qg",
        "qh",
        "qj",
        "qk",
        "ql",
        "qm",
        "qn",
        "qp",
        "qs",
        "qt",
        "qv",
        "qx",
        "qz",
        "sx",
        "vb",
        "vf",
        "vh",
        "vj",
        "vm",
        "vp",
        "vq",
        "vt",
        "vx",
        "xj",
        "xx",
        "zj",
        "zq",
        "zx",
    ]

    # Start with a random choice between a vowel or a consonant

    if random.choice([True, False]):
        word += random.choice(consonants)
        # random chance to add a second consonant
        if random.random() < 0.3 and len(word) < length:
            second_consonant = random.choice(consonants)
            # Check if the combination is forbidden and try again if needed
            while word[-1] + second_consonant in forbidden_combinations:
                second_consonant = random.choice(consonants)
            word += second_consonant

    while len(word) <= length:
        word += random.choice(vowels)
        if random.random() < 0.2 and len(word) < length and len(word) > 2:
            word += random.choice(vowels)

        word += random.choice(consonants)
        # random chance to add a second consonant
        if random.random() < 0.3 and len(word) < length:
            second_consonant = random.choice(consonants)
            while word[-1] + second_consonant in forbidden_combinations:
                second_consonant = random.choice(consonants)
            word += second_consonant

    # Insert the required letter at a random position in the word
    if add_letter:
        position = random.randint(0, len(word) - 1)
        word = word[:position] + current_letter + word[position + 1 :]

    return word


def generate_puzzle(num_words, caps=False):
    """
    This function generates a list of gibberish words.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    if num_words < len(alphabet):
        raise Exception("num words must be at least 26")
    gibberish_words = []
    english_words = set(
        words.words()
    )  # Create a set of English words for faster lookup
    alphabet_index = 0
    if caps:
        alphabet = alphabet.upper()

    interspersal = intersperse_true_values(num_words, 26)

    for curr_word in range(num_words):
        word_length = random.randint(2, 4)
        word = "word"
        while word in english_words:
            word = generate_word(
                word_length, alphabet[alphabet_index], interspersal[curr_word]
            )
        gibberish_words.append(word)
        if alphabet_index < len(alphabet) - 1:
            alphabet_index += interspersal[curr_word]  # true == 1

    return gibberish_words


if __name__ == "__main__":
    create_pdf(generate_puzzle(60, True))
