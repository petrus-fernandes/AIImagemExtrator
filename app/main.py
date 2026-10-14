import time
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from sqlalchemy import \
    text

from app.database import SessionLocal

from app.integrations.ai.openai_service import OpenAIService
from app.integrations.google_drive.google_drive_service import GoogleDriveService
from app.repositories.flyer_validation_repository import FlyerValidationRepository
from app.services.flyer_processing_service import FlyerProcessingService


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Aplicação iniciando...", flush=True)

    time.sleep(2)

    application_name = os.getenv("GOOGLE_DRIVE_APPLICATION_NAME")

    service = GoogleDriveService(application_name=application_name)

    openai_service = OpenAIService()

    session = SessionLocal()

    repository = FlyerValidationRepository(session)

    flyer_service = FlyerProcessingService(
        drive_service=service,
        ai_service=openai_service,
        flyer_validation_repository=repository,
    )

    flyer_service.process_pending_images()

    print("Processamento inicial concluído")

    yield

    print("Aplicação encerrando...")


app = FastAPI(lifespan=lifespan)