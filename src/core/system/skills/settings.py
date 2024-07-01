import json
from pathlib import Path
from core.system.log import LOG

def get_local_settings(skill_dir, skill_name) -> dict:
    """Build a dictionary using the JSON string stored in settings.json."""
    skill_settings = {}
    settings_path = Path(skill_dir).joinpath('settings.json')
    LOG.info(settings_path)
    if settings_path.exists():
        with open(str(settings_path)) as settings_file:
            settings_file_content = settings_file.read()
        if settings_file_content:
            try:
                skill_settings = json.loads(settings_file_content)
            # TODO change to check for JSONDecodeError in 19.08
            except Exception:
                log_msg = 'Failed to load {} settings from settings.json'
                LOG.exception(log_msg.format(skill_name))

    return skill_settings


def save_settings(skill_dir, skill_settings):
    """Save skill settings to file."""
    settings_path = Path(skill_dir).joinpath('settings.json')

    # Either the file already exists in /opt, or we are writing
    # to XDG_CONFIG_DIR and always have the permission to make
    # sure the file always exists
    if not Path(settings_path).exists():
        settings_path.touch(mode=0o644)

    with open(str(settings_path), 'w') as settings_file:
        try:
            json.dump(skill_settings, settings_file)
        except Exception:
            LOG.exception('error saving skill settings to '
                          '{}'.format(settings_path))
        else:
            LOG.info('Skill settings successfully saved to '
                     '{}' .format(settings_path))
