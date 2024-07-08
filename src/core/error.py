from .resources.data_files import List


class Error:
    @staticmethod
    def get(code):
        try:
            __errors__ = List.get("errors")
            erro = str(code)
            
            text_erro = ["Error "+ erro+": #"+ __errors__[erro], code]
            return text_erro

        except:
            return [f"Error 304: Error Not Found ({code})", 304]