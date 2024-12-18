import json
import re
import boto3
from random import choice

re_sentence = """(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"""  

with open("transcribe.json") as file:
    transcribe = json.load(file)

# build array of start times
times = [item["start_time"] for item in transcribe["results"]["items"] if "start_time" in item]

translate = boto3.client('translate')
transcript = transcribe["results"]["transcripts"][0]["transcript"]
sentences = re.split(re_sentence, transcript)
word_ptr = 0
translated_arr = []

for sentence in sentences:
    translated = translate.translate_text(
        Text=sentence,
        SourceLanguageCode='pt-BR',
        TargetLanguageCode='en-US'
    )
    translated_text = translated["TranslatedText"]
    translated_arr.append({ "start_time" : times[word_ptr], "translated" : translated_text})
    word_count = len(re.findall(r'\w+', sentence))
    word_ptr += word_count

print(json.dumps(translated_arr, indent=2))
