from googletrans import Translator

translator = Translator()
print(translator.translate(u"Hello World", dest="hi").text)
