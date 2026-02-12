from readers.image_generator import ImageGenerator
from django.conf import settings

print(f"API Key set: {hasattr(settings, 'SEGMIND_API_KEY')}")
if hasattr(settings, 'SEGMIND_API_KEY'):
    print(f"Key preview: {settings.SEGMIND_API_KEY[:10]}...")

gen = ImageGenerator()

print("\nGenerating test image...")
image_bytes = gen.generate_image_segmind(
    prompt="professional book cover art, fantasy theme, magical forest",
    width=800,
    height=1200
)

if image_bytes:
    print(f"✓ Success! Generated {len(image_bytes)} bytes")
    with open('/tmp/test_cover.jpg', 'wb') as f:
        f.write(image_bytes)
    print("✓ Saved to /tmp/test_cover.jpg")
else:
    print("✗ Failed to generate image")