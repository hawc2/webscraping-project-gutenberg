from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import WordNetLemmatizer
import io
from HeaderRemove import remove_gutenberg


# pre-stop word processes
def process_workflow(txt_in, outfile):
    print('cleaning...')
    # strip gutenberg headers
    text_in = remove_gutenberg(txt_in)

    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text_in)

    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # remove remaining non-alphabetic words
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english')+list(punctuation))
    cleaned = [w for w in words if w not in stop_words]
    super_clean = [lemmatizer.lemmatize(word) for word in cleaned]

    print('writing to file...')
    with io.open(outfile, 'w', encoding = 'utf8') as f:
        for sub in super_clean:
            try:
                f.write(sub + ' ')
            except Exception as e:
                print('Something Broke: ', e)
                continue
        f.write('\n')
        f.close()
    print('Done')