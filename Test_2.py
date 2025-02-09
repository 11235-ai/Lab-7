from __future__ import annotations
from yandex_cloud_ml_sdk import YCloudML

messages = [
    {
        "role": "system",
        "text": "Сгенерируй случайный текст, 100 слов, английский",
    },
]


def main():
    sdk = YCloudML(
        folder_id="",
        auth="",
    )

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)
    )

    for alternative in result:
        print(alternative)


if __name__ == "__main__":
    main()
