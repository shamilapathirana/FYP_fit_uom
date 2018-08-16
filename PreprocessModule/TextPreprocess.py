from PreprocessModule.PreprocessOps import PreprocessOperation
from nltk.tokenize import TweetTokenizer

class DataPreprocess:

    def text_preprocess(tweet):

        # Remove unnecessary white space
        white_removed_text = PreprocessOperation.remove_white_space(text= tweet)

        # Remove hash tag
        hash_removed_text = PreprocessOperation.remove_hash_tag(text=white_removed_text)

        # Remove At sign
        remove_username = PreprocessOperation.remove_username(text=hash_removed_text)

        # Remove additional white spaces
        white_removed_text_2 = PreprocessOperation.remove_white_space(text=remove_username)

        # Remove URLS and Emails
        remove_url_email = PreprocessOperation.remove_url_email(text=white_removed_text_2)

        # Remove repeated characters
        remove_repeated_char = PreprocessOperation.remove_repeat_char(text=remove_url_email)

        # Replace mixed words
        replace_mixed_words = PreprocessOperation.replace_mixed_words(text=remove_repeated_char)

        tokenized_text = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(replace_mixed_words)

        # replace emoticon
        replace_emoticon = PreprocessOperation.replace_emoticons(word_list=tokenized_text)

        # replace emoji
        replace_emoji = PreprocessOperation.replace_emoji(wold_list=replace_emoticon)

        # replace acronym
        replace_acronym = PreprocessOperation.replace_acronym_words(word_list=replace_emoji)

        # replace negation words
        replace_negation = PreprocessOperation.replace_negation_words(word_list=replace_acronym)

        text_sentence = ""
        for a in replace_negation:
            text_sentence = text_sentence + a + " "

        # remove non alphanumeric characters and single characters
        remove_single_char = PreprocessOperation.remove_single_char(text=text_sentence)

        # remove stop words
        remove_stopwords = PreprocessOperation.remove_stop_words(text=remove_single_char)

        # Remove unnessery white space
        white_removed_text_3 = PreprocessOperation.remove_white_space(text=remove_stopwords)

        return white_removed_text_3