_PRIA = "PRIA"
_SID = "SID"
_WEC = "WEC"
_LIS = "LIS"
_HIS = "HIS"
_ALEX = "ALEX"
_SAMI = "SAMI"
_NAT = "NAT"
_AMI = "AMI"

class Nexus:
    @staticmethod
    def call(name, action="", **kargs):
        path = f"core.nexus.{name}"
        exec("from {} import {}".format(path, name))
        jh ="("
        i = False
        for la in kargs:
            i = True
            jh += f'{la}="{kargs[la]}",'
        if i:
            jh = jh[:-1]+")"
        else:
            jh +=")"
        if action == '':
            exec(f"{name}{jh}")
        else:
            exec(f"{name}().{action}{jh}")
