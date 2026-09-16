# AI Image Extractor

Microsserviço responsável pelo processamento de imagens de panfletos de supermercados, utilizando inteligência artificial para extrair informações estruturadas dos produtos anunciados.

Este projeto faz parte do sistema Panfleteiro e está sendo desenvolvido como um microsserviço independente, substituindo o processamento que anteriormente era realizado diretamente pela aplicação principal em Java.

## Objetivo

O serviço tem como objetivo automatizar o processamento de panfletos de supermercados.

O fluxo principal é:

1. Buscar as pastas dos mercados no Google Drive.
2. Localizar as imagens dos panfletos.
3. Baixar as imagens para processamento.
4. Enviar as imagens para um serviço de IA/LLM.
5. Extrair informações dos produtos anunciados.
6. Armazenar o resultado para posterior validação.

Fluxo simplificado:

```text
Google Drive
     │
     │ imagens
     ▼
AI Image Extractor
     │
     ├── GoogleDriveService
     │
     ├── FlyerProcessingService
     │
     └── AI Service
             │
             ▼
          LLM / IA
             │
             ▼
     Dados estruturados
