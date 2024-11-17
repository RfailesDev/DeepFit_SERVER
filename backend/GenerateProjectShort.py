import os
from pathlib import Path

# Список игнорируемых директорий и файлов
IGNORE_LIST = [
    ".git",
    ".idea",
    "venv",
    ".venv",
    "__pycache__",
    "node_modules",
    "target",
    "build",
    "dist",
    "renderer.py",
    "ProjectOneFile.txt",  # Игнорируем сам отчет
    "GenerateProjectShort.py"  # Игнорируем сам отчет
]

def walk_dir(root_dir, prefix="", ignore_list=IGNORE_LIST):
    contents = sorted(os.listdir(root_dir))
    paths = [os.path.join(root_dir, p) for p in contents]
    dirs = [p for p in paths if os.path.isdir(p) and os.path.basename(p) not in ignore_list]
    files = [p for p in paths if os.path.isfile(p) and os.path.basename(p) not in ignore_list]

    lines = []
    for d in dirs:
        lines.append(f"{prefix}├── {os.path.basename(d)}/")
        lines.extend(walk_dir(d, prefix + "│   ", ignore_list))
    for f in files:
        if f != files[-1]:
            lines.append(f"{prefix}├── {os.path.basename(f)}")
        else:
            lines.append(f"{prefix}└── {os.path.basename(f)}")
    return lines

def get_project_structure(root_dir, root_dir_display, ignore_list=IGNORE_LIST):
    return "\n".join([os.path.basename(root_dir_display) + "/"] + walk_dir(root_dir, ignore_list=ignore_list))

def get_readable_files(root_dir, readable_extensions, ignore_list=IGNORE_LIST):
    file_data = []
    for root, _, files in os.walk(root_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            extension = os.path.splitext(filepath)[1]
            if extension in readable_extensions and not any(ignored in filepath for ignored in ignore_list):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                file_data.append(
                    (os.path.splitext(filepath)[0].replace(root_dir, "").replace("\\", "/"), content, extension[1:]))
    return file_data

def generate_report(output_file, script_file, readable_extensions, ignore_list=IGNORE_LIST):
    root_dir = "."
    root_dir_display = str(Path(__file__).parent.name)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Project structure:\n\n")
        f.write(get_project_structure(root_dir, root_dir_display, ignore_list))
        f.write("\n\n\nProject files:\n\n")
        for filepath, content, extension in get_readable_files(root_dir, readable_extensions, ignore_list):
            full_filepath = filepath + "." + extension
            if content and script_file not in full_filepath and output_file not in full_filepath:
                filepath_with_dots = filepath.replace("\\", ".")[1:]
                f.write(f"{filepath_with_dots}.{extension}\n")
                f.write(f"```{extension}\n{content}\n```\n\n\n")

if __name__ == "__main__":
    output_file = "ProjectOneFile.txt"

    readable_extensions = [
        ".txt", ".java", ".html", ".css", ".js",  # Исходные расширения

        # Языки программирования
        ".py", ".c", ".cpp", ".cs", ".go", ".php", ".rb", ".swift", ".kts", ".rs",
        ".scala", ".pl", ".hs", ".clj", ".exs", ".erl", ".groovy", ".lua", ".r",
        ".pas", ".m", ".v", ".fs", ".jl", ".dart", ".kt", ".cl",  # Добавленные языки

        # Скриптовые языки
        ".sh", ".bash", ".bat", ".ps1", ".awk", ".perl",  # Добавленные скриптовые языки

        # Конфигурационные файлы
        ".json", ".xml", ".yaml", ".properties", ".ini", ".toml", ".cfg", ".conf",
        ".env", ".plist", ".gradle", ".sbt",  # Добавленные конфиги

        # Разметка и документация
        ".md", ".markdown", ".rst", ".adoc", ".tex", ".org", ".doxygen",  # Добавленная документация

        # Логи и данные
        ".log", ".csv", ".tsv", ".sql", ".sqlite", ".avro", ".parquet",  # Добавленные форматы данных

        # Прочие
        ".gitignore", ".dockerfile", ".makefile", ".cmake", ".qml",  # Добавленные прочие типы
        ".graphql", ".proto", ".tf", ".tfstate",  # Infrastructure as Code
        ".webmanifest", ".svg",  # Web
        ".eml", ".mbox"  # Email
    ]

    script_file = os.path.basename(__file__)
    generate_report(output_file, script_file, readable_extensions)
    print(f"Project analysis report generated in: {output_file}")
