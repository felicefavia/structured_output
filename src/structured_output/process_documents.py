import os
from enum import Enum
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# Carica le variabili d'ambiente dal file .env
load_dotenv('.env')

# Inizializza il client passandogli la chiave salvata nel .env
client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))
MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')


class SummarySchema(BaseModel):
    invented_year: int
    summary: str
    inventors: list[str]
    key_features: list[str]


def analizza_articolo(testo_articolo: str) -> SummarySchema:
    summarization_prompt = (
        "Ti verrà fornito il contenuto di un articolo su un'invenzione. "
        "Il tuo obiettivo è riassumere l'articolo seguendo rigorosamente lo schema fornito."
    )
    
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "developer", "content": summarization_prompt},
            {"role": "user", "content": testo_articolo}
        ],
        response_format=SummarySchema
    )
    
    return response.choices[0].message.parsed


def esegui_analisi_cartella_articles():
    # Definiamo il percorso della cartella (può contenere file .txt, .md, ecc.)
    cartella_target = "articles"

    # Recuperiamo la lista di tutti i file presenti nella cartella
    file_presenti = os.listdir(cartella_target)
    
    file_da_elaborare = [f for f in file_presenti if os.path.isfile(os.path.join(cartella_target, f))]

    if not file_da_elaborare:
        print(f"La cartella '{cartella_target}' è vuota. Aggiungi dei documenti di testo da analizzare.")
        return

    print(f"Trovati {len(file_da_elaborare)} file nella cartella '{cartella_target}'. Inizio elaborazione...\n")
    print("=" * 60 + "\n")

    # Inizia il ciclo su tutti i file trovati
    for nome_file in file_da_elaborare:
        percorso_completo = os.path.join(cartella_target, nome_file)
        
        print(f"Elaborazione del file: {nome_file}")
        
        try:
            # Leggiamo il contenuto del file (usiamo encoding='utf-8' per gestire accenti e caratteri speciali)
            with open(percorso_completo, 'r', encoding='utf-8') as f:
                testo_articolo = f.read().strip()
            
            # Saltiamo il file se è vuoto
            if not testo_articolo:
                continue
                
            # Chiamata all'API passando il testo letto dal file corrente
            articolo_strutturato = analizza_articolo(testo_articolo)
            
            # Stampiamo i dati estratti per questo specifico file
            print(f"Anno di Invenzione: {articolo_strutturato.invented_year}")
            print(f"Inventori identificati: {', '.join(articolo_strutturato.inventors)}")
            print(f"Riassunto: {articolo_strutturato.summary}")
            print("Caratteristiche Chiave:")
            for feat in articolo_strutturato.key_features:
                print(f"     - {feat}")
                
        except Exception as e:
            print(f"Errore durante l'elaborazione del file {nome_file}: {e}")
            
        print("\n" + "-" * 40 + "\n")

    print("--- Fine di tutte le elaborazioni! ---")


# Lancia lo script
esegui_analisi_cartella_articles()