def word_count(text):
    wordcount = {}
    for word in text.split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    return wordcount