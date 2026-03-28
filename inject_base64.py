import os
index_path = r"f:\Ardent\fm-guider-vvitu\templates\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()
for i in range(1, 5):
    txt_path = rf"f:\Ardent\campus{i}.txt"
    with open(txt_path, "r", encoding="utf-8") as tf:
        b64 = tf.read().strip()
    
    # Replace the src path with the base64 string
    content = content.replace(f"/static/campus{i}.jpg", b64)
with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Injected base64 images into {index_path} successfully.")
