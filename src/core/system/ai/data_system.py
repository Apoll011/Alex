from core.system.config import path

class AiDataSytem:
    sig:str
    def open_file_in_data_learn(self, fpath):
        with open(f"{path}/core/nexus/{self.sig}/data_learn/{fpath}", "r") as file:
            content = file.read()
        
        return content
