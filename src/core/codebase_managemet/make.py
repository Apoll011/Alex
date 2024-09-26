import os

from core.config import RESOURCE_FOLDER
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
    resource_online_dirs = [
        "language",
        "model",
        "static",
        "templates",
        "audio"
    ]

    def __init__(self):
        resource_exists = self.resources_dir_exists()

        if resource_exists and self.check_resource_content_full():
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

    def check_resource_content_full(self):
        for dir_name in self.resources_dirs + self.resource_online_dirs:
            if not os.path.isdir(f"{RESOURCE_FOLDER}/{dir_name}/"):
                return False
        return True

    def create_dirs(self):
        for dir_name in self.resources_dirs:
            self.ensure_folder_exists(f"{RESOURCE_FOLDER}/{dir_name}/")

    def get_online_resources_dir(self):
        # For dirs in resources compare .version with the server version if greater download server version get smaller required version of the other packets and download them too

        raise NotImplementedError

    def get_alex(self):

        raise NotImplementedError
