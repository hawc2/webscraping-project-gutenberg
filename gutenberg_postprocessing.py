"""
Post-processing pipeline for Project Gutenberg text files.
Strips Gutenberg headers/footers, then cleans text via tokenization,
stopword removal, and lemmatization.
"""

import io
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Patterns matching Gutenberg header lines
BEGIN_TEXT = {
    "*END*THE SMALL PRINT",
    "*** START OF THE PROJECT GUTENBERG",
    "*** START OF THIS PROJECT GUTENBERG",
    " *** START OF THIS PROJECT GUTENBERG",
    "***START OF THE PROJECT GUTENBERG",
    "*** START OF THE COPYRIGHTED",
    "**The Project Gutenberg",
    "*SMALL PRINT!",
    "****     SMALL PRINT!",
    '["Small Print" V.',
    "This etext was prepared by",
    "This etext was produced by",
    "This Etext was prepared by",
    "This eBook was prepared by",
    "This Project Gutenberg Etext was prepared by",
    "E-text prepared by",
    "Produced by",
    "Distributed Proofreading Team",
    "Proofreading Team at http://www.pgdp.net",
    "http://gallica.bnf.fr)",
    "      http://archive.org/details/",
    '      (http://www.ibiblio.org/gutenberg/',
    "http://www.pgdp.net",
    "by The Internet Archive)",
    "by The Internet Archive/Canadian Libraries",
    "by The Internet Archive/American Libraries",
    "public domain material from the Internet Archive",
    "Internet Archive)",
    "Internet Archive/Canadian Libraries",
    "Internet Archive/American Libraries",
    "material from the Google Print project",
    "*END THE SMALL PRINT",
    "The Project Gutenberg",
    "http://gutenberg.spiegel.de/ erreichbar.",
    "http://gutenberg2000.de erreichbar.",
    "Project Runeberg publishes",
    "Beginning of this Project Gutenberg",
    "Project Gutenberg Online Distributed",
    "Gutenberg Online Distributed",
    "the Project Gutenberg Online Distributed",
    "the Project Gutenberg Online Distributed Proofreading Team",
    "Project Gutenberg TEI",
    "Gutenberg Distributed Proofreaders",
    "Project Gutenberg Distributed Proofreaders",
    "and the Project Gutenberg Online Distributed Proofreading Team",
    "Mary Meehan, and the Project Gutenberg Online Distributed Proofreading",
    "                this Project Gutenberg edition.",
    "More information about this book is at the top of this file.",
    "tells you about restrictions in how the file may be used.",
    "l'authorization à les utilizer pour preparer ce texte.",
    "of the etext through OCR.",
    "*****These eBooks Were Prepared By Thousands of Volunteers!*****",
    "We need your donations more than ever!",
}

# Patterns matching Gutenberg footer lines
END_TEXT = {
    "*** END OF THE PROJECT GUTENBERG",
    "*** END OF THIS PROJECT GUTENBERG",
    " *** END OF THIS PROJECT GUTENBERG",
    "        ***END OF THE PROJECT GUTENBERG",
    "***END OF THE PROJECT GUTENBERG",
    "*** END OF THE COPYRIGHTED",
    "End of the Project Gutenberg",
    " End of the Project Gutenberg",
    "End of The Project Gutenberg",
    "End of Project Gutenberg",
    "End of this Project Gutenberg",
    "END OF PROJECT GUTENBERG",
    "End of this is COPYRIGHTED",
    "by Project Gutenberg",
    "The Project Gutenberg Etext of ",
    "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**",
    "Ende dieses Project Gutenberg",
    "Ende dieses Projekt Gutenberg",
    "Ende dieses Etextes ",
    "Ende diese Project Gutenberg",
    "Ende dieses Project Gutenber",
    "Fin de Project Gutenberg",
    "Ce document fut presente en lecture",
    "Ce document fut présenté en lecture",
    "More information about this book is at the top of this file.",
    "We need your donations more than ever!",
}


def remove_gutenberg(txt_in):
    """Read a Gutenberg text file and strip header/footer boilerplate."""
    with open(txt_in, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if any(line.startswith(marker) for marker in BEGIN_TEXT):
            lines = lines[lines.index(line) + 1 :]

        if any(line.startswith(marker) for marker in END_TEXT):
            lines = lines[: lines.index(line)]
            return "\n".join(lines)

    return "\n".join(lines)


def clean_text(text):
    """Tokenize, lowercase, remove punctuation/stopwords, and lemmatize."""
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans("", "", string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [w for w in tokens if w.isalpha()]
    stop_words = set(stopwords.words("english") + list(string.punctuation))
    tokens = [w for w in tokens if w not in stop_words]
    return [lemmatizer.lemmatize(w) for w in tokens]


def process(txt_in, outfile):
    """Full pipeline: strip Gutenberg boilerplate, clean, and write to file."""
    print("cleaning...")
    text = remove_gutenberg(txt_in)
    tokens = clean_text(text)

    print("writing to file...")
    with io.open(outfile, "w", encoding="utf8") as f:
        f.write(" ".join(tokens) + "\n")
    print("done")
