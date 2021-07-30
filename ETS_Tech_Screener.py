import os
import sys
import json
import nltk
import pandas as pd

from nltk.tokenize import word_tokenize

# Function to read input file
def readfile(filename):
    # Reading csv file with pandas
    try:
        fl = pd.read_csv(filename)
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e

    if "Id" not in fl.columns:
        raise Exception("Invalid columns - need Id Column in file")

    if "Sentence" not in fl.columns:
        raise Exception("Invalid columns - need Sentence column in file")

    return fl


def get_tags(sentence):
    # Word tokenization
    words = word_tokenize(sentence)

    # Tagging
    pos_with_words = nltk.pos_tag(words)

    # Separating tags & words and saving tags separately
    tags = [tag for _, tag in pos_with_words]

    return words, tags


def get_preps_idx(words, tags):
    preposition = ["on", "for", "of", "to", "at", "in", "with", "by"]

    length = len(words)

    preposition_index = []
    for ind, word in enumerate(words):
        # Checking specifically for 'to'
        if word.lower() == "to" and ind + 1 < length and tags[ind + 1] == "VB":
            continue
        if word.lower() in preposition:
            preposition_index.append(ind)

    return preposition_index


# Function to create json
def get_features(sentence):
    words, tags = get_tags(sentence)

    preposition_index = get_preps_idx(words, tags)

    length = len(words)

    for i in preposition_index:
        w, t = words[i], tags[i]

        features_words = []
        features_tags = []
        for j in range(1, 3):
            features_words.append(" ".join(words[max(0, i - j) : i + 1]))
            features_words.append(" ".join(words[i : min(i + j + 1, length)]))
            features_words.append(
                " ".join(words[max(0, i - j) : min(i + j + 1, length)])
            )

            features_tags.append(" ".join(tags[max(0, i - j) : i + 1]))
            features_tags.append(" ".join(tags[i : min(i + j + 1, length)]))
            features_tags.append(" ".join(tags[max(0, i - j) : min(i + j + 1, length)]))

        yield words[i], features_words + features_tags


def extract_features(df, outfile):
    df = df[["Id", "Sentence"]]

    with open(outfile, "w") as f:
        for sentence_id, sentence in df.itertuples(index=False):
            for prep_id, (prep, features) in enumerate(get_features(sentence)):
                out = json.dumps(
                    {
                        "id": f"{sentence_id}_{prep_id}",
                        "prep": prep,
                        "features": features,
                    },
                    indent=None,
                )

                f.write(out + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("required inputfile and outputfile as arguments")

    infile, outfile = sys.argv[1:3]

    df = readfile(infile)
    extract_features(df, outfile)

    # Calling function over csv file
