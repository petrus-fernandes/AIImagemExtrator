from typing import Protocol
from pathlib import Path


class AIService(Protocol):

    def process_flyer(self, image_path: Path, url: str, market_external_code: str):
        pass
