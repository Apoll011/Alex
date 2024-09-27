import os

from core.config import RESOURCE_FOLDER, USER_RESOURCE_PATH
from core.log import LOG

class PrepareWorkSpace:
    """
    Create resource folder by:
        MkDIR resources, application, ctx, data
        Download language, model, static, templates

    """

    resources_dirs = [
        "application",
        "ctx",
        "data",
    ]

    def __init__(self):
        resource_exists = self.resources_dir_exists()

        if resource_exists:
            LOG.info("Resources folder is ready for usage")
            return
        self.create_dirs()

    def resources_dir_exists(self):
        return self.ensure_folder_exists(RESOURCE_FOLDER)

    @staticmethod
    def ensure_folder_exists(folder):
        if os.path.isdir(folder):
            return True
        os.mkdir(folder)
        return False

    def create_dirs(self):
        for dir_name in self.resources_dirs:
            self.ensure_folder_exists(f"{USER_RESOURCE_PATH}/{dir_name}/")