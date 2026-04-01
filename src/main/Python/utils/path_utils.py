import os

def get_base_path():
    """Get the project root base path dynamically"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
    return project_root

def get_resources_path():
    """Get the resources folder path"""
    project_root = get_base_path()
    return os.path.join(project_root, "resources/")

def ensure_resources_dir_exists():
    """Ensure the resources directory exists"""
    resources_path = get_resources_path()
    os.makedirs(resources_path, exist_ok=True)
    return resources_path

