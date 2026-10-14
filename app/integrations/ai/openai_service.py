from pathlib import Path
import base64
import os
import requests

PROMPT_INSTRUCTIONS = """
    Transforme a imagem enviada em um JSON no seguinte padrão usando todos os produtos enviados na imagem:
    {
        "url": "%s",
        "marketExternalCode": "%s",
        "initialDate": "",
        "expirationDate": "",
        "ads": [
            {
                "productName": "",
                "productCategory": "",
                "price": 0.0,
                "priceWithDiscount": 0.0,
                "active": true
            }
        ]
    }

    O productCategory deve ser catalogado como:
    Açougue; Frios; Laticínios; Adega; Bebidas; Higiene; Limpeza; Hortifruti;
    Mercearia; Padaria; Enlatados; Cereais; Rotisseria; Petshop; Peixaria; Auto-peças;
    Bazar; Congelados.

    O nome do produto dever possuir o nome completo como está no panfleto incluindo a grandeza de medida.

    Os produtos alcoolicos devem ser catalogados com productCategory de Adega.

    O price deve registrar o valor sem o desconto adicional de cartão da loja ou outro tipo de desconto enquanto o priceWithDiscount deve registrar o valor com o desconto adicional de cartão da loja ou outro tipo de desconto.

    Após criar o JSON, quero que revise o resultado alterando algumas informações conforme as seguintes regras:
    As datas devem estar no padrão dd/MM/YYYY.
    Todo productName deve conter a primeira letra sempre maiúscula como formatação padrão.
    As gradezas de medida como: quilograma, mililitros, litros devem ser abreviadas como: kg,ml,L.
    """

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIService:

    def process_flyer(self, image_bytes: bytes, url: str, market_external_code: str):
        image_base64 = base64.b64encode(
            image_bytes).decode(
            "utf-8")
        prompt = PROMPT_INSTRUCTIONS % (url, market_external_code)

        system_prompt = """
            Você é um extrator de ofertas de panfletos de supermercados. Use OCR e devolva os dados em formato JSON no padrão especificado pelo usuário.
            Sempre responda com JSON válido, sem comentários, sem blocos de markdown. Comece a resposta diretamente com '{'.
            Cada anuncio terá seu preço e pode ter um preço com desconto, caso não possua desconto o priceWithDiscount pode ser nulo.
            """

        payload = {
            "model": "gpt-5-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
        }

        openai_key = os.getenv("OPENAI_API_KEY")

        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=120)

        response.raise_for_status()

        return response.json()
