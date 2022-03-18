import re
import nltk
STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
def tokenize_and_clean(doc):
 matches = re.finditer(r'\w+|[^\w\s]+', doc)
 for match in matches:
   word = match.group()
   if len(word) > 2 and word.isalpha():
       word = word.lower()
    if word not in STOP_WORDS:
     yield word
def extract_verbs(doc):
 words = tuple(tokenize_and_clean(doc))
 tags = nltk.pos_tag(words)
 lemmatizer = nltk.stem.WordNetLemmatizer()
 VERBS = ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD')
 verb_counts = {}
 for word, pos in tags:
   if pos in VERBS:
     word = lemmatizer.lemmatize(word, 'v')
     verb_counts[word] = verb_counts.get(word, 0) + 1
 verb_counts = sorted(verb_counts.items(), key=lambda t: t[1], reverse=True)
 return verb_counts
if __name__ == '__main__':
 with open('1_doc.txt', 'r', encoding='utf-8') as f:
 doc = f.read()
 verb_counts = extract_verbs(doc)
 for verb, count in verb_counts[:20]:
    print(f'{verb:10} {count}')