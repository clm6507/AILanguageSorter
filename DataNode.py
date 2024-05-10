from enum import Enum

class Language(Enum):
    ENGLISH = 0
    DUTCH = 1
    UNKNOWN = 2

class DataNode:

    data_string: str
    weight: float
    language: Language

    attribute_list: list[bool]

    #all of the attributes
    contains_english_articles: bool
    contains_english_prepositions: bool
    contains_english_demonstrative_pronouns: bool
    contains_english_nominative_pronouns: bool

    contains_dutch_articles: bool
    contains_dutch_prepositions: bool
    contains_dutch_nominative_pronouns: bool

    avg_word_length_lt_5: bool



    def __init__(this, data_string: str, language: Language = Language.UNKNOWN, weight: float = 1):
        this.data_string = this.remove_punc(data_string)
        this.language = language
        this.weight = weight

        
        this.contains_english_articles = this.english_article_check()
        this.contains_english_prepositions = this.english_preposition_check()
        this.contains_english_demonstrative_pronouns = this.english_demostrative_pronouns_check()
        this.contains_english_nominative_pronouns = this.english_nominative_pronouns_check()

        this.contains_dutch_articles = this.dutch_article_check()
        this.contains_dutch_prepositions = this.dutch_preposition_check()
        this.contains_dutch_nominative_pronouns = this.dutch_nominative_pronouns_check()

        this.avg_word_length_lt_5 = this.has_avg_word_length_lt_5()


        this.attribute_list = [this.contains_english_articles, this.contains_english_prepositions, 
                               this.contains_english_demonstrative_pronouns, this.contains_english_nominative_pronouns,
                               this.contains_dutch_articles, this.contains_dutch_prepositions,
                               this.contains_dutch_nominative_pronouns, this.avg_word_length_lt_5]
    
    #removes punctuation from line
    def remove_punc(this, data_string):
        punctuation = [".",",","\'","\"","?","!","(",")"]
        new_data_string = ""
        for letter in data_string:
            if(letter not in punctuation):
                new_data_string += letter

        return new_data_string


    #EVERYTHING 
    #BELOW
    #THIS
    #IS
    #CHECKS
    #FOR
    #ATTRIBUTES


    def english_article_check(this):
        english_articles = [ "the", "an", "a" ]
        split_string = this.data_string.lower().split()
        for word in split_string:
            if(word in english_articles):
                return True

        return False

    def dutch_article_check(this):
        dutch_articles = [ "de", "het", "een", "der", "des", "den" ]
        split_list = this.data_string.lower().split()
        for word in split_list:
            if(word in dutch_articles):
                return True
        return False

    def english_preposition_check(this):
        english_prepositions = [ "in", "from", "with", "under", "throughout", "atop", "for", "on", "of", "to", "aboard", "about",
        "above", "abreast", "absent", "across", "adjacent", "after", "against", "along", "alongside", "amid", "mid",
        "among", "apropos", "apud", "around", "as", "astride", "at", "ontop", "afore", "tofore", "behind", "ahind",
        "below", "ablow", "beneath", "neath", "beside", "between", "atween", "beyond", "ayond", "by", "chez",
        "circa", "spite", "down", "except", "into", "less", "like", "minus", "near", "nearer", "nearest", "anear", "notwithstanding",
        "off", "onto", "opposite", "out", "outen", "over", "past", "per", "pre", "qua", "sans", "sauf", "sithence", "through",
        "thru", "truout", "toward", "underneath", "up", "upon", "upside", "versus", "via", "vis-à-vis", "without", "ago",
        "apart", "aside", "aslant", "away", "withal", "towards", "amidst", "amongst", "midst", "whilst" ]

        split_list = this.data_string.lower().split()
        for word in split_list:
            if(word in english_prepositions):
                return True
        return False
    
    def dutch_preposition_check(this):
        dutch_prepositions = prepositions = ["à", "aan", "aangaande", "achter", "behalve", "behoudens", "beneden", "benevens", "benoorden", "benoordoosten", "benoordwesten",
        "beoosten", "betreffende", "bewesten", "bezijden", "bezuiden", "bezuidoosten", "bezuidwesten", "bij", "binnen", "blijkens", "boven", "bovenaan",
        "buiten", "circa", "conform", "contra", "cum", "dankzij", "door", "gedurende", "gezien", "in", "ingevolge", "inzake", "jegens", "krachtens",
        "langs", "luidens", "met", "middels", "na", "naar", "naast", "nabij", "namens", "nevens", "niettegenstaande", "nopens", "om",
        "omstreeks", "omtrent", "onder", "onderaan", "ongeacht", "onverminderd", "op", "over", "overeenkomstig", "per", "plus", "post",
        "richting", "rond", "rondom", "spijts", "staande", "te", "tegen", "tegenover", "ten", "ter", "tijdens", "tot", "tussen",
        "uit", "van", "vanaf", "vanuit", "versus", "via", "vis-à-vis", "volgens", "voor", "voorbij", "wegens", "zijdens",
        "zonder"]
        split_list = this.data_string.lower().split()
        for word in split_list:
            if(word in dutch_prepositions):
                return True
        return False

    def english_demostrative_pronouns_check(this):
        english_demonstrative_pronouns = [ "this", "that", "these", "those" ]
        split_list = this.data_string.lower().split()
        for word in split_list:
            if(word in english_demonstrative_pronouns):
                return True
        return False
    
    def english_nominative_pronouns_check(this):
        english_pronouns_nominative = [ "i", "you", "he", "she", "it", "we", "they" ]
        split_list = this.data_string.lower().split()
        for word in split_list:
            if(word in english_pronouns_nominative):
                return True
        return False

    def dutch_nominative_pronouns_check(this):
        dutch_pronouns_nominative = [ "ik", "je", "jij", "hij", "ze", "we", "wij", "jullie", "zij", "u", "ge", "gij", "men" ]
        split_list = this.data_string.lower().split()
        for word in split_list:
            if(word in dutch_pronouns_nominative):
                return True
        return False
    
    def has_avg_word_length_lt_5(this):
        split_str = this.data_string.split()
        total_char = 0
        for word in split_str:
            total_char += len(word)

        return (total_char/15.0) < (5.0)


    def __repr__(this) -> str:
        return str(this.language) + " " + str(this.attribute_list)