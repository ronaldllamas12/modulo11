from __future__ import annotations

from io import BytesIO
from pathlib import Path
from uuid import uuid4

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.core.config import get_settings


class CloudinaryService:
    def __init__(self) -> None:
        self.settings = get_settings()

        if not self.settings.use_cloudinary_uploads:
            return

        if not (
            self.settings.cloudinary_cloud_name
            and self.settings.cloudinary_api_key
            and self.settings.cloudinary_api_secret
        ):
            raise RuntimeError(
                "Cloudinary no esta configurado. Define CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET en backend/.env"
            )

        cloudinary.config(
            cloud_name=self.settings.cloudinary_cloud_name,
            api_key=self.settings.cloudinary_api_key,
            api_secret=self.settings.cloudinary_api_secret,
            secure=True,
        )

    async def upload_image(self, upload: UploadFile, category: str) -> str | None:
        if upload is None:
            return None

        content = await upload.read()
        if not content:
            return None

        if not self.settings.use_cloudinary_uploads:
            return None

        suffix = Path(upload.filename or "img").suffix or ".jpg"
        folder = f"{self.settings.cloudinary_folder}/{category}".strip("/")
        result = cloudinary.uploader.upload(
            BytesIO(content),
            folder=folder,
            public_id=str(uuid4()),
            resource_type="image",
            overwrite=False,
        )
        return result.get("secure_url")
