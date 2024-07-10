# The following lines are replaced during the release process.
# START_VERSION_BLOCK
CORE_VERSION_MAJOR = 3
CORE_VERSION_MINOR = 1
CORE_VERSION_BUILD = 8
CORE_VERSION_TYPE = "Alpha"
# END_VERSION_BLOCK

CORE_VERSION_TUPLE = (CORE_VERSION_MAJOR,
                      CORE_VERSION_MINOR,
                      CORE_VERSION_BUILD)
CORE_VERSION_STR = '.'.join(map(str, CORE_VERSION_TUPLE))+f"-{CORE_VERSION_TYPE}"


class VersionManager:
    @staticmethod
    def get():
        return {"coreVersion": CORE_VERSION_STR, "enclosureVersion": None}


def check_version(version_string):
    """
        Check if current version is equal or higher than the
        version string provided to the function

        Args:
            version_string (string): version string ('Major.Minor.Build')
    """
    version_tuple = tuple(map(int, version_string.split('.')))
    return CORE_VERSION_TUPLE >= version_tuple
