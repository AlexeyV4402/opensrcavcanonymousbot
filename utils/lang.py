from config import TECH_SUPPORT_URL


async def get_available_languages():
    return translations.keys()


async def _(word_code: str, lang: str):
    return translations[lang][word_code]


async def get_all(lang: str = None):
    if lang:
        return translations[lang].items()
    else:
        all_words = []
        for lang_code in translations:
            all_words.extend(translations[lang_code])
        return all_words


async def get_code(text: str, lang: str):
    all_words = await get_all()
    if text not in all_words:
        return False
    return list(translations[lang].keys())[list(translations[lang].values()).index(text)]
