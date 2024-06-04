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
    def call(self, name, action="", **kargs):
        path = f"resource.Nexos.{name}"
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
        ret = ''
        if action == '':
            exec(f"{name}{jh}")
        else:
            exec(f"{name}().{action}{jh}")

        return ret