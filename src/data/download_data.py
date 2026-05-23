import os
from datasets import load_dataset
import json

def download_and_prepare_data():
    print("Iniciando download de datasets reais (MedQuAD e Women Health)...")
    
    # 1. Carregar dataset focado em Saúde da Mulher
    # Fonte: https://huggingface.co/datasets/altaidevorg/women-health-mini
    try:
        ds_women = load_dataset("altaidevorg/women-health-mini", split="train")
        print(f"Dataset Women Health carregado: {len(ds_women)} exemplos.")
    except Exception as e:
        print(f"Erro ao carregar Women Health: {e}")
        ds_women = []

    # 2. Carregar MedQuAD (Subset simplificado)
    # Fonte: https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADataset
    try:
        ds_medquad = load_dataset("keivalya/MedQuad-MedicalQnADataset", split="train")
        # Filtrar por palavras-chave relacionadas a ginecologia/obstetrícia
        keywords = ["woman", "women", "pregnancy", "breast", "gynecology", "obstetrics", "menstrual", "urology"]
        ds_medquad_filtered = ds_medquad.filter(lambda x: any(k in x['Question'].lower() for k in keywords))
        print(f"MedQuAD filtrado (Saúde da Mulher): {len(ds_medquad_filtered)} exemplos.")
    except Exception as e:
        print(f"Erro ao carregar MedQuAD: {e}")
        ds_medquad_filtered = []

    # 3. Formatar para JSONL (instruction, context, response)
    processed_data = []
    
    # Processar Women Health
    for item in ds_women:
        conversations = item.get("conversations", [])
        instruction = ""
        response = ""
        for msg in conversations:
            if msg.get("role") == "user":
                instruction = msg.get("content", "")
            elif msg.get("role") == "assistant":
                response = msg.get("content", "")
                
        processed_data.append({
            "instruction": instruction,
            "context": "Saúde da Mulher / Ginecologia",
            "response": response
        })
        
    # Processar MedQuAD
    for item in ds_medquad_filtered:
        processed_data.append({
            "instruction": item.get("Question", ""),
            "context": "MedQuAD Medical QA",
            "response": item.get("Answer", "")
        })

    # Salvar resultado
    output_path = os.path.join("data", "real_medical_data.jsonl")
    os.makedirs("data", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in processed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    print(f"Sucesso! Dataset real salvo em: {output_path}")
    print(f"Total de exemplos: {len(processed_data)}")

if __name__ == "__main__":
    download_and_prepare_data()
