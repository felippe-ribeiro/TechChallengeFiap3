import os
from dotenv import load_dotenv
from src.agents.medical_flows import app_graph
from src.utils.guardrails import MedicalGuardrails

load_dotenv()

# Roda o assistente e passa a mensagem pelo fluxo do grafo
def run_assistant(user_input: str):
    print(f"\n[Usuário]: {user_input}")
    
    # Roda anonimizacao antes
    clean_input = MedicalGuardrails.anonymize_data(user_input)
    
    # Estado inicial pra rodar o LangGraph
    initial_state = {
        "messages": [clean_input],
        "category": "",
        "risk_level": "",
        "next_step": "",
        "requires_emergency": False
    }
    
    final_state = app_graph.invoke(initial_state)
    
    # Pega a resposta gerada
    response = final_state['messages'][-1]
    
    # Aplica guardrail de remedio
    safe_response = MedicalGuardrails.check_prescription(response)
    
    print(f"[Assistente]: {safe_response}")

if __name__ == "__main__":
    print("--- Assistente Médico Especializado (Saúde da Mulher) ---")
    
    # Teste 1: Triagem de Urgência
    run_assistant("Estou com sangramento intenso e muita dor abdominal.")
    
    # Teste 2: Segurança (Violência)
    run_assistant("Tenho hematomas no braço e medo do que meu parceiro pode fazer.")
    
    # Teste 3: Consulta Eletiva / Prescrição
    run_assistant("Gostaria de saber qual anticoncepcional posso tomar para parar a cólica.")
