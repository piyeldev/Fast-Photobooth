import os, sys
from root_path import BASE_PATH

# resource path helper
def resource_path(relative_path: str) -> str:
    return os.path.join(BASE_PATH, relative_path)