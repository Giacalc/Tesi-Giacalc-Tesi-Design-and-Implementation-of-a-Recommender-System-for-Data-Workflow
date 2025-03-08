import os
from github import Github
from github import Auth
import json

auth = Auth.Token("your_token")
g = Github(auth=auth)

query = "a_galaxy_workflow extension:ga"

save_path = r"D:\TEST_RAG"
annotation_path = os.path.join(save_path, "annotation")
no_annotation_path = os.path.join(save_path, "noAnnotation")

os.makedirs(save_path, exist_ok=True)
os.makedirs(annotation_path, exist_ok=True)
os.makedirs(no_annotation_path, exist_ok=True)

def file_has_no_empty_annotations(file_content):
    try:
        data = json.loads(file_content)
        for step in data.get("steps", {}).values():
            if not step.get("annotation"):
                return False
        return True
    except json.JSONDecodeError:
        return False

def download_files():
    print(f"Numero totale di risultati trovati per '{query}': {g.search_code(query).totalCount}")

    results = g.search_code(query)
    count_with_annotation = 0
    count_no_annotation = 0
    count_skipped = 0

    for file in results:
        if file.name.endswith(".ga"):
            try:
                if file.size < 2048:  # 2KB = 2048 byte
                    print(f"File {file.name} scartato (dimensione {file.size}B < 2KB)")
                    count_skipped += 1
                    continue

                file_content = file.decoded_content.decode('utf-8')

                if file_has_no_empty_annotations(file_content):
                    file_path = os.path.join(annotation_path, file.name)
                    count_with_annotation += 1
                else:
                    file_path = os.path.join(no_annotation_path, file.name)
                    count_no_annotation += 1

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(file_content)
                    print(f"File salvato: {file_path}")

            except Exception as e:
                print(f"Errore durante l'elaborazione del file {file.name}: {e}")

    print(f"Numero totale di file salvati con annotazioni: {count_with_annotation}")
    print(f"Numero totale di file salvati senza annotazioni: {count_no_annotation}")
    print(f"Numero totale di file scartati (dimensione < 2KB): {count_skipped}")


download_files()