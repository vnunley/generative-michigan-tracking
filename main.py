# -*- coding: utf-8 -*-
from fpdf import FPDF
import random

import nltk
from nltk.corpus import words

# Download the words corpus if not already downloaded
nltk.download("words")


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


def generate_word(length, current_letter, next_letter, add_letter, language="en"):
    """
    This function generates a single gibberish word of a given length.
    """
    en_vowels = "aeiou".replace(current_letter, "").replace(next_letter, "")
    en_consonants = "bcdfghjklmnpqrstvwxyz".replace(current_letter, "").replace(
        next_letter, ""
    )
    en_forbidden_combinations = [
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

    he_letters = "אבגדהוזחטיכלמנסעפצקרשת".replace(current_letter, "").replace(
        next_letter, ""
    )
    he_forbidden_combinations = []
    he_sofit_letters = {"כ": "ך", "מ": "ם", "נ": "ן", "פ": "ף", "צ": "ץ"}
    # Forbidden Hebrew words
    he_forbidden_words = [["י", "ה", "ו", "ה"], ["א", "ל", "ה", "י", "נ", "ו"]]

    if language not in ["en", "he"]:
        raise ValueError("Unsupported language")

    word = ""

    # Start with a random choice between a vowel or a consonant if english
    if language == "en":
        if random.choice([True, False]):
            word += random.choice(en_consonants)
            # random chance to add a second consonant
            if random.random() < 0.3 and len(word) < length:
                second_consonant = random.choice(en_consonants)
                # Check if the combination is forbidden and try again if needed
                while word[-1] + second_consonant in en_forbidden_combinations:
                    second_consonant = random.choice(en_consonants)
                word += second_consonant
        while len(word) <= length:
            word += random.choice(en_vowels)
            if random.random() < 0.2 and len(word) < length and len(word) > 2:
                word += random.choice(en_vowels)
            word += random.choice(en_consonants)
            # random chance to add a second consonant
            if random.random() < 0.3 and len(word) < length:
                second_consonant = random.choice(en_consonants)
                while word[-1] + second_consonant in en_forbidden_combinations:
                    second_consonant = random.choice(en_consonants)
                word += second_consonant
    elif language == "he":
        word += random.choice(he_letters)
        while len(word) <= length:
            next_letter = random.choice(he_letters)
            while word[-1] + next_letter in he_forbidden_combinations:
                next_letter = random.choice(he_letters)
            word += next_letter

        # Check if the last letter of the word needs to be sofit
        if word[-1] in he_sofit_letters:
            word = word[:-1] + he_sofit_letters[word[-1]]

        # Check if the word is one of the forbidden words
        while list(word) in he_forbidden_words:
            word = generate_word(
                length, current_letter, next_letter, add_letter, language
            )

    # Insert the required letter at a random position in the word
    if add_letter:
        position = random.randint(0, len(word) - 1)
        word = word[:position] + current_letter + word[position + 1 :]

    return word


def generate_word_set(num_words, language="en", caps=False):
    """
    This function generates a list of gibberish words.
    """
    if language == "en":
        alphabet = "abcdefghijklmnopqrstuvwxyz"
    elif language == "he":
        alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
    else:
        raise ValueError("Unsupported language")

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
                word_length,
                alphabet[alphabet_index],
                alphabet[max(alphabet_index - 1, 0)],
                interspersal[curr_word],
                language,
            )
        gibberish_words.append(word)
        if alphabet_index < len(alphabet) - 1:
            alphabet_index += interspersal[curr_word]  # true == 1

    return gibberish_words


def create_puzzles(num_words, num_puzzles, lang="en", caps=False):
    """
    This function creates a number of puzzles, each containing a set of gibberish words.
    The number of puzzles and the number of words in each puzzle are specified by the parameters.
    The language parameter determines the language of the words, and the filename parameter
    specifies the name of the output file. If the caps parameter is set to True, the words
    will be in uppercase.

    Parameters:
    num_words (int): The number of words in each puzzle.
    num_puzzles (int): The number of puzzles to create.
    language (str, optional): The language of the words. Defaults to 'en'.
    filename (str, optional): The name of the output file. Defaults to 'output.pdf'.
    caps (bool, optional): If set to True, the words will be in uppercase. Defaults to False.

    Returns:
    None
    """
    word_sets = [
        generate_word_set(num_words, lang, caps=caps) for _ in range(num_puzzles)
    ]

    return word_sets


def create_pdf(word_sets, filename="output.pdf", language="en"):
    """
    This function creates a PDF named 'output.pdf' with a list of the alphabet
    at the top. Below the alphabet, the words in each set of the argument are printed in a
    paragraph format. It also adds בס"ד in 8 point font in the top right of the first page.
    It repeats the alphabet and words for each entry in `word_sets`, two per page max.
    """

    if word_sets is None:
        raise ValueError("word_sets cannot be None")

    # Creating instance of FPDF class
    pdf = FPDF()

    # Generate alphabet
    if language == "en":
        alphabet = " ".join([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    elif language == "he":
        # Generate Hebrew alphabet in reverse order
        alphabet = " ".join(
            [
                "ת",
                "ש",
                "ר",
                "ק",
                "צ",
                "פ",
                "ע",
                "ס",
                "נ",
                "מ",
                "ל",
                "כ",
                "י",
                "ט",
                "ח",
                "ז",
                "ו",
                "ה",
                "ד",
                "ג",
                "ב",
                "א",
            ]
        )
    else:
        raise ValueError("Unsupported language")

    pdf.add_page()
    # Add בס"ד in 8 point font in the top right of the first page
    pdf.add_font("NotoSansHebrew", "", "NotoSansHebrew.ttf", uni=True)
    pdf.set_font("NotoSansHebrew", "", 8)
    pdf.set_xy(170, 10)
    pdf.cell(20, 0, text='ד"סב', align="R")

    # Set margins for the paragraph
    pdf.set_left_margin(30)
    pdf.set_right_margin(30)
    pdf.set_auto_page_break(auto=True, margin=15)

    if language == "en":
        pdf.set_font("Times", "", size=14)
    elif language == "he":
        pdf.set_font("NotoSansHebrew", "", size=12)

    # Iterate over word_sets
    for i, word_set in enumerate(word_sets):
        # Add a page every two word sets
        if i % 2 == 0 and i > 0:
            pdf.add_page()

        # Set font to Times New Roman
        pdf.set_font(size=14)

        # Add the alphabet at the top center of each word_set
        # Adjust the y position for the alphabet to avoid overlap
        y_position_alphabet = 10 if i % 2 == 0 else 130
        pdf.set_xy(25, y_position_alphabet)
        pdf.cell(0, 10, text=alphabet, ln=1, align="C")

        # Adjust the y position for each word set to avoid overlap
        y_position = 20 if i % 2 == 0 else 140
        pdf.set_xy(30, y_position)

        # Set font and add a cell for the paragraph of words
        pdf.set_font(size=24)
        if language == "he":
            # Reverse the Hebrew words
            word_set = [word[::-1] for word in word_set]

            # Split the paragraph into lines based on characters in each word
            # No more than a maximum of 31 characters per line including spaces between words
            lines = []
            line = ""
            for word in word_set:
                if len(line) + len(word) + 1 > 37:  # +1 for the space
                    lines.append(line)
                    line = word
                else:
                    line = line + " " + word if line else word
            if line:
                lines.append(line)

            # Print each line in the pdf
            for line in lines:
                line = " ".join(
                    reversed(line.split())
                )  # Reverse the order of words in each line
                pdf.set_x(10)  # Adjust the x position before adding the cell
                pdf.multi_cell(0, 10, text=line, align="R")
        elif language == "en":
            paragraph = " ".join(word_set)
            pdf.set_x(10)  # Adjust the x position before adding the cell
            pdf.multi_cell(0, 10, text=paragraph, align="L")

    # Save the pdf with name .pdf
    pdf.output(filename)


if __name__ == "__main__":
    lang = "en"
    for i in range(38):
        create_pdf(
            create_puzzles(60, 10, lang),
            filename=f"generated-library/{lang}/exercise-{lang}-{i}.pdf",
            language=lang,
        )

    lang = "he"
    for i in range(38):
        create_pdf(
            create_puzzles(60, 10, lang),
            filename=f"generated-library/{lang}/exercise-{lang}-{i}.pdf",
            language=lang,
        )
