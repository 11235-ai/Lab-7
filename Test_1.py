import json
import requests


def analyze(text_en):
    url = "http://api.text2data.com/v3/analyze"

    payload = {
        "DocumentText": f"{text_en}",
        "IsTwitterContent": "false",
        "PrivateKey": "",
        "Secret": "",
        "RequestIdentifier": "" 
    }

    resp_an = requests.post(url, data=payload)
    data = resp_an.json()

    if data["Status"] == 1:

        #  Эмоциональная окраска текста (положительная, отрицательная, нейтральная).
        polarity = data["DocSentimentPolarity"]
        string = data["DocSentimentResultString"]
        value = data["DocSentimentValue"]

        print(f"Документ: {polarity}{string} {value:+.2f}")
        print(f"Сила эмоций: {data['Magnitude']:.2f}")
        print(f"Субъективность: {data['Subjectivity']}")

        for item in data["CoreSentences"]:
            print(f"Основной текст: {item['Text']}")

        print("Ключевые слова")

        for item in data["Keywords"]:
            text = item["Text"]
            keyword_text = item["KeywordType"]
            keyword_polarity = item["SentimentPolarity"]
            result = item["SentimentResult"]
            value = item["SentimentValue"]
            
            print(f"{text} ({keyword_text}) {keyword_polarity}{result} {value:+.2f}")

    else:
        print(data["ErrorMessage"])


def main():
    analyze(input("Введите текст для анализа: "))


if __name__ == "__main__":
    main()
