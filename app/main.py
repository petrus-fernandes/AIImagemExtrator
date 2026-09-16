from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from app.integrations.google_drive.google_drive_service import GoogleDriveService
from app.services.flyer_processing_service import FlyerProcessingService


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Aplicação iniciando...", flush=True)

    application_name = os.getenv("GOOGLE_DRIVE_APPLICATION_NAME")

    service = GoogleDriveService(
        application_name=application_name
    )

    flyer_service = FlyerProcessingService(
        drive_service=service,
        ai_service=None,
        flyer_validation_service=None,
        processed_folder_id=''
    )

    flyer_service.process_pending_images()

    print("Processamento inicial concluído")

    yield

    print("Aplicação encerrando...")


app = FastAPI(lifespan=lifespan)