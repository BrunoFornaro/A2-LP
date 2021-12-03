
from django.forms.models import model_to_dict
import pandas as pd
def converter_query(instancia, retornar="lista_de_dicionarios"):
    context = []
    for entrada in instancia:
        entrada = model_to_dict(entrada)
        entrada["id"] = entrada["id"] - 1
        context.append(entrada)
    if retornar == "dataframe":
        context = pd.DataFrame(context)
    return context