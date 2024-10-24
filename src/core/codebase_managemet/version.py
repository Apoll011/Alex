from enum import Enum


class VERSION_TYPE(Enum):
    DEVELOPMENT = -1
    BETA = 0
    ALPHA = 1
    TESTING = 2
    PRODUCTION = 3

    def title(self):
        return self.name.title()

    @staticmethod
    def from_title(title: str):
        for version_name in list(VERSION_TYPE):
            if version_name.name == title.upper():
                return version_name
        raise Exception(f"{title} is not a valid version type.")


class VersionManager:
    CORE_VERSION_MAJOR = 5
    CORE_VERSION_MINOR = 0
    CORE_VERSION_BUILD = 41
    CORE_VERSION_TYPE = VERSION_TYPE.BETA
    # END_VERSION_BLOCK

    CORE_VERSION_TUPLE = (
        CORE_VERSION_MAJOR,
        CORE_VERSION_MINOR,
        CORE_VERSION_BUILD,
        CORE_VERSION_TYPE.value,
    )
    CORE_VERSION_STR = (
            ".".join(map(str, CORE_VERSION_TUPLE[0:-1])) + f"-{CORE_VERSION_TYPE.title()}"
    )

    @staticmethod
    def get():
        """

        :return: A dict containing the coreVersion and enclosureVersion
        """
        return {
            "coreVersion": VersionManager.CORE_VERSION_STR,
            "enclosureVersion": None,
        }

    @staticmethod
    def get_tuple():
        return VersionManager.CORE_VERSION_TUPLE

    @staticmethod
    def check_version(version_string: str):
        """
        Check if current version is equal or higher than the
        version string provided to the function
        :param version_string: version string ('Major.Minor.Build-Type(Development, Beta, Alpha, Testing, Production)')
        """
        version = version_string.split("-")
        if len(version) > 1:
            version_list = list(map(int, version[0].split(".")))
            version_type = VERSION_TYPE.from_title(version[1]).value
            version_list.append(version_type)
            version_tuple = tuple(version_list)
        else:
            version_tuple = tuple(map(int, version_string.split(".")))
        return VersionManager.check_version_tuple(version_tuple)

    @staticmethod
    def check_version_tuple(version_tuple: tuple):
        """
        Check if current version is equal or higher than the
        version tutple provided to the function
        :param version_tuple: version tutple ('Major.Minor.Build-Type(Development, Beta, Alpha, Testing, Production)')
        """
        return VersionManager.CORE_VERSION_TUPLE <= version_tuple

    @staticmethod
    def versionify(version):
        return ".".join(map(str, version))
