import pandas as pd
import re
import sys
import os

vocab = []
parameters_spam = {}
parameters_ham = {}
p_spam = 0
p_ham = 0
alpha = 1

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def train_model():
    global vocab, parameters_spam, parameters_ham, p_spam, p_ham

    sms = pd.read_csv(resource_path('dulieuhuanluyen'), sep='\t', header=None, names=['Label', 'SMS'])
    data_random = sms.sample(frac=1, random_state=1)
    index = round(len(data_random) * 0.8)
    huanluyen = data_random[:index].reset_index(drop=True)
    
    huanluyen['SMS'] = huanluyen['SMS'].str.replace(r'\W', ' ', regex=True).str.lower().str.split()

    vocab = list(set(word for sms in huanluyen['SMS'] for word in sms))
    
    number_appear = {word: [0] * len(huanluyen) for word in vocab}
    for idx, sms in enumerate(huanluyen['SMS']):
        for word in sms:
            number_appear[word][idx] += 1
    
    word_counts = pd.DataFrame(number_appear)
    train_extend = pd.concat([huanluyen, word_counts], axis=1)
    
    spam_messages = train_extend[train_extend['Label'] == 'spam']
    ham_messages = train_extend[train_extend['Label'] == 'ham']
    p_spam = len(spam_messages) / len(train_extend)
    p_ham = len(ham_messages) / len(train_extend)
    
    n_spam = spam_messages['SMS'].apply(len).sum()
    n_ham = ham_messages['SMS'].apply(len).sum()
    n_vocab = len(vocab)
    
    parameters_spam = {word: (spam_messages[word].sum() + alpha) / (n_spam + alpha * n_vocab) for word in vocab}
    parameters_ham = {word: (ham_messages[word].sum() + alpha) / (n_ham + alpha * n_vocab) for word in vocab}

def classify_test(message):
    message = re.sub(r'\W', ' ', message)
    message = message.lower().split()
    p_spam_given = p_spam
    p_ham_given = p_ham
    for word in message:
        if word in parameters_spam:
            p_spam_given *= parameters_spam[word]
        if word in parameters_ham:
            p_ham_given *= parameters_ham[word]
    if p_ham_given > p_spam_given:
        return 'ham'
    elif p_spam_given > p_ham_given:
        return 'spam'
    else:
        return 'needs human classification'

train_model()


