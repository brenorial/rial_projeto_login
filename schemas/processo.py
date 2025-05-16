from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date, datetime
from model.processo import Processo


class ProcessoSchema(BaseModel):
    """ Define como um novo processo deve ser representado """
    numero: str
    descricao: str
    data_inicio: date
    data_fim: date 

    @validator("data_inicio", "data_fim", pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")
        return v
class ProcessoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura da busca de um processo """
    numero: str = "12345-67.2024.8.01.0001"

class ProcessoViewSchema(BaseModel):
    """ Define como um Processo será retornado """
    id: int
    numero: str
    descricao: str
    data_inicio: date
    data_fim: date
    data_insercao: date
    comentarios: Optional[List[str]] = []  

class ListagemDeProcessosSchema(BaseModel):
    """ Define como uma listagem de processos será retornada """
    processos: List[ProcessoViewSchema]

def apresenta_processo(processo: Processo):
    """ Retorna uma representação do processo """
    return {
        "id": processo.id,
        "numero": processo.numero,
        "descricao": processo.descricao,
        "data_inicio": processo.data_inicio,
        "data_fim": processo.data_fim,
        "data_insercao": processo.data_insercao,
    }

def Apresenta_Processo_Lista(processos: List[Processo]):
    """ Retorna uma representação da lista de processos """
    return {
        "processos": [apresenta_processo(processo) for processo in processos]
    }

class ProcessoDelSchema(BaseModel):
    """ Define a estrutura do dado retornado após a remoção de um processo """
    message: str
    numero: str
