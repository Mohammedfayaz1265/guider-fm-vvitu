import base64
from PIL import Image
import io
images = ["campus1", "campus2", "campus3", "campus4"]
for img in images:
    with Image.open(f"f:/Ardent/fm-guider-vvitu/static/{img}.jpg") as i:
        i.thumbnail((400, 300))
        buffer = io.BytesIO()
        i.save(buffer, format="JPEG", quality=50)
        with open(f"f:/Ardent/{img}.txt", "w") as out:
            out.write("data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode())
