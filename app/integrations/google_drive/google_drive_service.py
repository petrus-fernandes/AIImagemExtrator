from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from pathlib import Path
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveService:

    def __init__(self, application_name):
        self.application_name = application_name
        self.drive_service = self.build_drive_service()


    def list_folders(self, folder_id=None):
        if not folder_id:
            folder_id = os.getenv("GOOGLE_DRIVE_MAIN_DIRECTORY")

        query = (
            f"'{folder_id}' in parents "
            "and mimeType = 'application/vnd.google-apps.folder'"
        )

        result = (
            self.drive_service
            .files()
            .list(
                q=query,
                fields="files(id, name)"
            )
            .execute()
        )

        return result.get(
            "files",
            []
        )


    def list_images(self, folder_id):
        query = (
            f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
        )

        result = (
            self.drive_service
            .files()
            .list(
                q=query,
                fields="files(id, name, mimeType, parents)"
            )
            .execute()
        )

        return result.get(
            "files",
            []
        )

    def download_image(self, image_id, image_name):
        arquivo_local = Path("/tmp") / image_name

        with open(arquivo_local, "wb") as output_stream:
            request = self.drive_service.files().get(
                fileId=image_id,
                alt="media"
            )

            downloader = MediaIoBaseDownload(
                output_stream,
                request
            )

            done = False

            while not done:
                status, done = downloader.next_chunk()
                print(f"Baixando {image_name}: {int(status.progress() * 100)}%", flush=True)

        return arquivo_local

    def get_credentials(self):
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        return service_account.Credentials.from_service_account_file(filename=credentials_path)


    def build_drive_service(self) :
        return build(
            serviceName="drive",
            version="v3",
            credentials=self.get_credentials()
        )

    def get_processed_folder_id(self):
        return os.getenv("GOOGLE_DRIVE_PROCESSED_DIRECTORY")


    def move_to_folder(self, arquive, folder_id):
        self.drive_service.files().update(
            fileId=arquive["id"],
            addParents=folder_id,
            removeParents=arquive["parents"][0]
        ).execute()
