import os
import json
import hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = os.path.join(ROOT, "files")
OUTPUT = os.path.join(ROOT, "manifest.json")

result = []

for folder, _, filenames in os.walk(FILES):
    for filename in filenames:
        full_path = os.path.join(folder, filename)
        relative_path = os.path.relpath(full_path, FILES).replace("\\", "/")

        sha256 = hashlib.sha256()
        with open(full_path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                sha256.update(chunk)

        result.append({
            "name": filename,
            "path": "files/" + relative_path,
            "size": os.path.getsize(full_path),
            "sha256": sha256.hexdigest()
        })

manifest = {
    "version": 1,
    "files": result
}

with open(OUTPUT, "w", encoding="utf-8") as file:
    json.dump(manifest, file, ensure_ascii=False, indent=4)

print("GRUL manifest created!")
print("Files:", len(result))
print("Output:", OUTPUT)
