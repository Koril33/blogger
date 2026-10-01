import pytest
from PIL import Image

from djhx_blogger.config import BloggerError
from djhx_blogger.images import compress_image


def test_transparent_png_and_palette_alpha(tmp_path):
    for mode in ("RGBA", "P"):
        source, output = tmp_path / f"{mode}.png", tmp_path / f"{mode}-out.png"
        image = Image.new(mode, (800, 800))
        if mode == "P":
            image.info["transparency"] = 0
        image.save(source)
        compress_image(source, output, max_size=(100, 100))
        with Image.open(output) as result:
            assert result.convert("RGBA").getpixel((0, 0))[3] == 0
            assert result.width <= 800


def test_animation_and_unsupported_images_are_copied(tmp_path):
    source, output = tmp_path / "animated.gif", tmp_path / "out.gif"
    Image.new("RGB", (32, 32), "red").save(
        source,
        save_all=True,
        append_images=[Image.new("RGB", (32, 32), "blue")],
        duration=100,
        loop=0,
    )
    compress_image(source, output)
    assert source.read_bytes() == output.read_bytes()
    with Image.open(output) as result:
        assert result.n_frames == 2


def test_non_image_copy_and_no_source_overwrite(tmp_path):
    source, target = tmp_path / "sample.pdf", tmp_path / "out.pdf"
    source.write_bytes(b"attachment")
    compress_image(source, target)
    assert target.read_bytes() == b"attachment"
    with pytest.raises(BloggerError, match="覆盖"):
        compress_image(source, source)


def test_jpeg_orientation_and_size(tmp_path):
    source, output = tmp_path / "input.jpg", tmp_path / "out.jpg"
    exif = Image.Exif()
    exif[274] = 6
    Image.effect_noise((1800, 800), 100).convert("RGB").save(source, quality=95, exif=exif)
    compress_image(source, output, max_size=(500, 500))
    assert output.stat().st_size < source.stat().st_size
    with Image.open(output) as result:
        assert result.height <= 500
        assert result.height > result.width
        assert result.getexif().get(274) is None


def test_decompression_bombs_fail_without_output(tmp_path, monkeypatch):
    source, target = tmp_path / "image.png", tmp_path / "out.png"
    Image.new("RGB", (20, 20)).save(source)
    monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 100)
    with pytest.raises(BloggerError, match="无法处理图片"):
        compress_image(source, target)
    assert not target.exists()
