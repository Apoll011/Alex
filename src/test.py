from core.codebase_managemet.updater import Updater

u = Updater()
a, l = u.scan()

u.update_lib(l)
