import re
import os
import PreprocessModule.Dictionary.NegationWord as negation
import PreprocessModule.Dictionary.Acronym as acronym
import PreprocessModule.Dictionary.ShortWord as shortword
import PreprocessModule.Dictionary.Emoji as emoji
import PreprocessModule.Dictionary.Emoticon as emoticon
from nltk.tokenize import word_tokenize

class PreprocessOperation:

    def remove_white_space(text):
        whitespace_removed_tweet = re.sub('[\s]+', ' ', text)
        return whitespace_removed_tweet

    def remove_hash_tag(text):
        hash_removed_tweet = re.sub(r'#([^\s]+)', r' \1', text)
        return hash_removed_tweet

    def remove_username(text):
        username_removed_tweet = re.sub(r'\S*@(?:\[[^\]]+\]|\S+)', '', text)
        return username_removed_tweet

    def remove_url_email(text):
        url_removed_tweet = re.sub(
            r'(https?:\/\/|www\.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)
        url_removed_tweet_plus = re.sub(
            r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.(com|lk|edu|co|in|cn|net|uk|org|info|eu|ru|biz|tk|ads)\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',
            '', url_removed_tweet)
        return url_removed_tweet_plus

    def remove_repeat_char(text):
        repeated_char_removed_tweet = re.sub(r'(.)\1{3,}', r'\1\1', text, flags=re.DOTALL)
        return repeated_char_removed_tweet

    def replace_negation_words(word_list):
        replaced_negation = []
        for w in word_list:
            try:
                replaced_negation.append(negation.select_negation(w))
            except:
                replaced_negation.append(w)
        return replaced_negation

    def replace_acronym_words(word_list):
        replaced_acronym = []
        for w in word_list:
            try:
                replaced_acronym.append(acronym.select_acronym(w.lower()))
            except:
                replaced_acronym.append(w)
        return replaced_acronym

    def replace_short_words(word_list):
        replaced_short = []
        for w in word_list:
            try:
                replaced_short.append(shortword.select_shortwords(w.lower()))
            except:
                replaced_short.append(w)
        return replaced_short

    def replace_emoticons(word_list):
        replaced_emoticons = []
        for w in word_list:
            try:
                replaced_emoticons.append(emoticon.select_emoticon(w))
            except:
                replaced_emoticons.append(w)
        return replaced_emoticons

    def replace_emoji(wold_list):
        replaced_emoji = []
        for w in wold_list:
            try:
                replaced_emoji.append(emoji.select_emoji(w))
            except:
                replaced_emoji.append(w)
        return replaced_emoji

    def replace_mixed_words(text):
        r0 = re.sub("can’t|isn’t|aren’t|wasn’t|weren’t|hasn’t|haven’t|hadn’t|didn’t|doesn’t|don’t|couldn’t|wouldn’t|shouldn’t|mustn’t|needn’t|mightn’t|daren’t", 'not', text)
        r1 = re.sub("who’s", 'who is', r0)
        r2 = re.sub("who’d", 'who would', r1)
        r3 = re.sub("who’ll", 'who will', r2)
        r4 = re.sub("what’s", 'what is', r3)
        r5 = re.sub("how’s", 'how is', r4)
        r6 = re.sub("where’s", 'where is', r5)
        r7 = re.sub("when’s", 'when is', r6)
        r8 = re.sub("here’s", 'here is', r7)
        r9 = re.sub("there’s", 'there is', r8)
        r10 = re.sub("there’d", 'there would', r9)
        r11 = re.sub("there’ll", 'there will', r10)
        r12 = re.sub("I’m", 'i am', r11)
        r13 = re.sub("he’s", 'he is', r12)
        r14 = re.sub("she’s", 'she is', r13)
        r15 = re.sub("it’s", 'it is', r14)
        r16 = re.sub("what’ll", 'what will', r15)

        r17 = re.sub("ude00", 'grin', r16)
        r18 = re.sub("ude01", 'big grin', r17)
        r19 = re.sub("ude02", 'laugh', r18)
        r20 = re.sub("ude05", 'laugh', r19)
        r21 = re.sub("ude09", 'wink', r20)
        r22 = re.sub("ude0e", 'cool', r21)
        r23 = re.sub("ude0d", 'love', r22)
        r24 = re.sub("ude18", 'romantic kiss', r23)
        r25 = re.sub("ude17", 'kiss', r24)
        r26 = re.sub("ude42", 'smile', r25)
        r27 = re.sub("ude11", 'disgusted', r26)
        r28 = re.sub("ude13", 'sad', r27)
        r29 = re.sub("ude15", 'confused', r28)
        r30 = re.sub("ude12", 'sad', r29)
        r31 = re.sub("ude41", 'sad', r30)
        r32 = re.sub("ude2d", 'crying', r31)
        r33 = re.sub("ude22", 'sad', r32)
        r34 = re.sub("ude28", 'scared', r33)
        r35 = re.sub("ude31", 'scared', r34)
        r36 = re.sub("ude21", 'angry', r35)
        r37 = re.sub("ude20", 'angry', r36)
        r38 = re.sub("ude08", 'fantacy', r37)
        r39 = re.sub("ude1c", 'funny', r38)
        r40 = re.sub("ude1d", 'funny', r39)
        r41 = re.sub("ude0a", 'happy', r40)
        r42 = re.sub("ude35", 'crazy', r41)
        r43 = re.sub("ude2a", 'sleepy', r42)
        r44 = re.sub("ude07", 'angel', r43)
        r45 = re.sub("udc4d", 'like', r44)
        r46 = re.sub("udc4e", 'dislike', r45)
        r47 = re.sub("udc4c", 'love', r46)
        r48 = re.sub("u2764", 'joy', r47)
        r49 = re.sub("u2026t", "'", r48)

        r50 = re.sub("doesn’t", "not", r49)
        r51 = re.sub("haven’t", "not", r50)
        r52 = re.sub("can’t", "not", r51)
        r53 = re.sub("isn’t", "not", r52)
        r54 = re.sub("aren’t", "not", r53)
        r55 = re.sub("shouldn’t", "not", r54)
        r56 = re.sub("weren’t", "not", r55)
        r57 = re.sub("hasn’t", "not", r56)
        r58 = re.sub("wasn’t", "not", r57)
        r59 = re.sub("doesn’t", "not", r58)
        r60 = re.sub("don’t", "not", r59)
        r61 = re.sub("didn’t", "not", r60)
        r62 = re.sub("couldn’t", "not", r61)
        r63 = re.sub("wouldn’t", "not", r62)
        r64 = re.sub("won’t", "not", r63)
        r65 = re.sub("mightn’t", "not", r64)
        r66 = re.sub("daren’t", "not", r65)
        r67 = re.sub("that’s", "that is", r66)
        return r67

    def remove_single_char(text):
        nonalphanumeric_less = re.sub(r'[^A-Za-z\s]+', '', text)
        single_character_less = re.sub(r'\b[B-Zb-z]\b', '', nonalphanumeric_less)
        return single_character_less

    def remove_stop_words(text):
        stop_words = []
        word_tokens = (word_tokenize(text))
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'Dictionary\stopwords.txt')
        with open(filename, encoding='utf-8', errors='ignore')as f:
            lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())
        f.close()
        filtered_sentence_stopword = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence_stopword.append(w)
        sentence = ""
        for a in filtered_sentence_stopword:
            sentence = sentence + a + " "
        return sentence