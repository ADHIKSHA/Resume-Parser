

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 



def basicdetails(lines,text):
    import spacy
    from spacy.matcher import Matcher

    # load pre-trained model
    nlp = spacy.load('en_core_web_sm')

    # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab)
    dictionary={}
    def extract_name(resume_text,lines):
        for line in lines:
            words= word_tokenize(line)
            stop_words = set(stopwords.words('english')) 
            for w in words:
                if w in stop_words:
                    continue
                    
            nlp_text = nlp(line)
        
            # First name and Last name are always Proper Nouns
            pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        
            matcher.add('NAME', None, pattern)
        
            matches = matcher(nlp_text)
            for match_id, start, end in matches:
                span = nlp_text[start:end]
                return span.text

    print('Name')
    name=extract_name(text,lines)
    print(name)
    dictionary["Name"]=name

    import re

    def extract_mobile_number(text):
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
        
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number


    print('Phone')
    phone=(extract_mobile_number(text))
    print(phone)
    dictionary['Phone']=phone

    def extract_email(email):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    print('email')
    email=(extract_email(text))
    print(email)
    dictionary["Email"]=email





    word_tokens = word_tokenize(text) 
    #print(word_tokens)

    def extract_degrees(lines):
        degrees=['b.tech','ba','ma','xii','b.sc','m.sc','m.tech','high','senior','x','bachelor','bachelors','master','masters','speicalization','mba','msc','10+2']
        in_degrees=[]
        for w in lines:
            w=w.lower()
            if w in degrees:
                if w=='senior' and 'xii' in in_degrees or w=='junior' and 'x' in in_degrees or w=='bachelor' and 'b.tech' in in_degrees or w=='b.tech' and 'bachelor' in in_degrees or w=='masters' and 'm.tech' in in_degrees or w=='msc' and 'm.sc' in in_degrees or w=='m.sc' and 'msc' in in_degrees :
                    continue
                in_degrees.append(w)
        return in_degrees

    degrees=[]
    for w in word_tokens:
        if w.lower()=="education":
            degrees=extract_degrees(word_tokens)
            count_edu=len(degrees)
            #finddates=extract_dates(text,count_edu)
            print(degrees)


    dictionary['degrees']=degrees
    return dictionary



