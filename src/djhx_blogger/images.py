"""Conservative image optimization: preserve transparency, animation and formats."""

from __future__ import annotations

import os
import shutil
import tempfile
import warnings
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from .config import BloggerError

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".ico"}


def compress_image(input_path, output_path, quality=85, max_size=(1920, 1920)):
    source, target = Path(input_path), Path(output_path)
    if source.resolve() == target.resolve():
        raise BloggerError("图片输出路径不能覆盖源文件")
    if not 1 <= quality <= 95 or min(max_size) < 1:
        raise BloggerError("图片质量或尺寸参数无效")
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".blogger-image-", dir=target.parent)
    os.close(descriptor)
    candidate = Path(temporary)
    try:
        if source.suffix.lower() not in IMAGE_SUFFIXES:
            shutil.copy2(source, target)
            return
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(source) as image:
                image_format = image.format
                if getattr(image, "is_animated", False) or image_format not in {
                    "JPEG",
                    "PNG",
                    "WEBP",
                }:
                    shutil.copy2(source, target)
                    return
                image.load()
                oriented = ImageOps.exif_transpose(image)
                oriented.thumbnail(max_size, Image.Resampling.LANCZOS)
                save_options = (
                    {"icc_profile": image.info["icc_profile"]}
                    if image.info.get("icc_profile")
                    else {}
                )
                if image_format in {"JPEG", "WEBP"}:
                    save_options["quality"] = quality
                if image_format == "JPEG":
                    oriented = oriented.convert("RGB")
                    save_options["optimize"] = True
                elif image_format == "PNG":
                    if oriented.mode == "P":
                        oriented = oriented.convert(
                            "RGBA" if "transparency" in image.info else "RGB"
                        )
                    save_options["compress_level"] = 6
                oriented.save(candidate, format=image_format, **save_options)
        if candidate.stat().st_size < source.stat().st_size:
            candidate.replace(target)
        else:
            shutil.copy2(source, target)
    except (
        OSError,
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        raise BloggerError(f"无法处理图片 {source}: {exc}") from exc
    finally:
        candidate.unlink(missing_ok=True)
