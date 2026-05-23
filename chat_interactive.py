import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.agents.medical_flows import app_graph
from src.utils.guardrails import MedicalGuardrails

load_dotenv()

# Confere se a chave da openai ta configurada certinho
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("\n[ATENÇÃO]: Não achei a OPENAI_API_KEY no arquivo .env.")
    print("Digita sua chave da OpenAI aqui pra poder rodar o chat interativo (ou da enter pra fechar):")
    api_key = input("Chave: ").strip()
    if not api_key:
        print("Fechando...")
        sys.exit(0)
    os.environ["OPENAI_API_KEY"] = api_key

print("\nIniciando o assistente de saude da mulher...")
try:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
except Exception as e:
    print(f"Erro ao iniciar a OpenAI: {e}")
    sys.exit(1)

print("\n==================================================================")
print("     ASSISTENTE DE SAÚDE DA MULHER E TRIAGEM (INTERATIVO)")
print("==================================================================")
print("Digita 'sair' pra finalizar o programa.")
print("Dica: Digita seu CPF ou pede um remedio pra testar os guardrails funcionado!\n")

while True:
    user_input = input("\n[Você]: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["sair", "exit", "quit"]:
        print("\nConversa encerrada. Se cuida!")
        break
        
    # 1. Filtro pra tirar dados sensiveis (CPF)
    clean_input = MedicalGuardrails.anonymize_data(user_input)
    if clean_input != user_input:
        print(f"[Guardrail]: Dados pessoais ocultados automaticamente.")
        
    # 2. Rodando o grafo pra definir o nivel de urgencia e categoria
    initial_state = {
        "messages": [clean_input],
        "category": "",
        "risk_level": "",
        "next_step": "",
        "requires_emergency": False
    }
    
    graph_state = app_graph.invoke(initial_state)
    category = graph_state.get("category", "CLÍNICA_GERAL")
    requires_emergency = graph_state.get("requires_emergency", False)
    
    # 3. Manda pro modelo do GPT responder usando a analise de triagem
    prompt_sistema = (
        "Você é um Assistente Médico Especializado em Saúde da Mulher.\n"
        "Seu papel é acolher, realizar a triagem e orientar a paciente baseando-se em diretrizes médicas seguras.\n"
        f"Triagem do sistema: Categoria={category}, Emergência={requires_emergency}.\n"
        "Regras:\n"
        "1. Nunca passe dosagens ou prescreva remedios de forma direta.\n"
        "2. Se for uma urgencia ou violencia, recomende a paciente ir pro hospital ou buscar ajuda imediatamente de um jeito bem humano e acolhedor.\n"
        "3. Responda em Português de forma direta e acolhedora."
    )
    
    mensagens = [
        SystemMessage(content=prompt_sistema),
        HumanMessage(content=clean_input)
    ]
    
    try:
        response = llm.invoke(mensagens).content
    except Exception as e:
        response = f"Erro na OpenAI: {e}"
        
    # 4. Confere se a resposta do modelo nao esta receitando remedio sem aviso
    safe_response = MedicalGuardrails.check_prescription(response)
    
    print(f"\n[Assistente]: {safe_response}")
