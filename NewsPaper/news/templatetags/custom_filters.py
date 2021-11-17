from django import template

register = template.Library()
CENSOR_LIST = ["тест", "убийство"]


@register.filter(name='censor')
def censor(text):
    censored_text = ""
    punct_mark = ""
    for word in text.split():
        while not word[-1].isalpha():
            punct_mark = word[-1] + punct_mark
            if len(word) == 1:
                word = ""
                break
            word = word[:-1]
        if word.lower() in CENSOR_LIST:
            word = "*" * len(word)
        censored_text += word + punct_mark + " "

        punct_mark = ""

    return censored_text


