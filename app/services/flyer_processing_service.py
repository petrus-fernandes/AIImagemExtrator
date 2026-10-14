import logging
from pathlib import Path
import base64

from app.models.flyer_validation import \
    FlyerValidation

logger = logging.getLogger(__name__)


class FlyerProcessingService:

    def __init__(
        self,
        drive_service,
        ai_service,
        flyer_validation_repository,
    ):
        self.drive_service = drive_service
        self.ai_service = ai_service
        self.flyer_validation_repository = flyer_validation_repository

    def process_pending_images(self):
        print("Iniciando processamento de panfletos", flush=True)
        market_folders = self.drive_service.list_folders()

        for market_folder in market_folders:

            market_name = market_folder["name"]
            # print(market_name, flush=True)
            url_folders = self.drive_service.list_folders(market_folder["id"])

            for url_folder in url_folders:

                url = url_folder["name"]
                # print(url, flush=True)
                images = self.drive_service.list_images(url_folder["id"])

                for image in images:
                    print(image, market_name, url, url_folder["id"], flush=True)
                    self.process_image(image, market_name, url)

    def process_image(self, image, market_name: str, url: str):

        image_name = image["name"]
        image_id = image["id"]

        logger.info("Baixando panfleto '%s' do mercado '%s'", image_name, market_name)

        local_file = self.drive_service.download_image(image_id, image_name)
        image_bytes = local_file.read_bytes()

        logger.info(
            "Enviando panfleto '%s' para processamento ao modelo de AI",
            image_name
        )

        try:
            response = self.ai_service.process_flyer(image_bytes, url, market_name)

        except Exception:
            logger.exception("Erro ao processar panfleto '%s' pela IA", image_name)
            raise

        logger.info(
            "Panfleto '%s' processado com sucesso",
            image_name)

        flyer_validation = FlyerValidation(
            image=image_bytes,
            response=response.get("choices")[0].get("message").get("content"))
        try:
            flyer_validation = self.flyer_validation_repository.save(flyer_validation)

        except Exception:
            logger.exception(
                "Erro ao processar panfleto '%s' pela IA",
                image_name)
            raise

        finally:
            Path(local_file).unlink(missing_ok=True)
            logger.info("Arquivo temporário removido: %s", image_name)

        logger.info(
            "Validação salva com id %s",
            flyer_validation.id)

        # self.send_to_processed_folder(image)

        logger.info(
            "Arquivo '%s' movido para processados",
            image_name)



    def send_to_processed_folder(self, image, folder_id=None):
        if not folder_id:
            folder_id = self.drive_service.get_processed_folder_id()
        self.drive_service.move_to_folder(image, folder_id)