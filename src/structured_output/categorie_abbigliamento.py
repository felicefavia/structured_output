import os
from enum import Enum
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv('.env')

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))
MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')

class CategoriaAbbigliamento(str, Enum):
    shoes = "scarpe"
    jackets = "giacche"
    tops = "maglie"
    bottoms = "pantaloni"

class PreferenzeProfilo(BaseModel):
    categoria_prodotto: CategoriaAbbigliamento
    colore_preferito: Optional[str]
    caratteristica_chiave: str
    budget_stimato: str

def esegui_esempio_personal_shopper():
    print("--- Esecuzione Esempio 2: Estrazione Preferenze Shopper ---")
    
    shopper_prompt = (
        "Sei un assistente AI per lo shopping. Il tuo compito è analizzare la richiesta dell'utente "
        "ed estrarre i parametri di ricerca strutturati per i nostri filtri del database."
    )
    
    richiesta_utente = (
        "Sto cercando un nuovo cappotto o una giacca invernale per andare in montagna. "
        "Ho sempre un freddo tremendo, quindi per favore trovale qualcosa di caldissimo! "
        "Se possibile la vorrei di colore blu scuro, non bado a spese."
    )
    
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "developer", "content": shopper_prompt},
            {"role": "user", "content": richiesta_utente}
        ],
        response_format=PreferenzeProfilo
    )
    
    profilo_ricerca = response.choices[0].message.parsed
    
    # Stampiamo i filtri estratti pronti per una query a un database
    print(f"Categoria del filtro DB: {profilo_ricerca.categoria_prodotto.value}")
    print(f"Filtro Colore: {profilo_ricerca.colore_preferito}")
    print(f"Esigenza Principale: {profilo_ricerca.caratteristica_chiave}")
    print(f"Filtro Budget: {profilo_ricerca.budget_stimato}")


esegui_esempio_personal_shopper()