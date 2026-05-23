from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
import operator

# Estrutura pra guardar o estado da conversa e as decisoes do bot
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    category: str
    risk_level: str
    next_step: str
    requires_emergency: bool

# Aqui faz a triagem basica baseada no que a pessoa escreveu
def triage_node(state: AgentState):
    last_message = state['messages'][-1].lower()
    
    # Se tiver alguma palavra de alerta, joga pro risco alto
    if any(word in last_message for word in ["sangramento", "dor aguda", "febre alta", "falta de ar"]):
        return {
            "risk_level": "ALTO", 
            "requires_emergency": True,
            "next_step": "Encaminhamento Imediato ao Pronto Socorro"
        }
    else:
        return {
            "risk_level": "BAIXO/MÉDIO", 
            "requires_emergency": False,
            "next_step": "Agendamento de Consulta Eletiva"
        }

# Filtro pra ver se tem algum sinal de violencia domestica
def violence_detection_node(state: AgentState):
    last_message = state['messages'][-1].lower()
    
    # Gatilhos pra acionar a seguranca da paciente
    violence_triggers = ["medo do marido", "agressão", "hematomas", "ameaça", "violência"]
    
    if any(word in last_message for word in violence_triggers):
        return {
            "category": "SEGURANÇA_DA_MULHER",
            "next_step": "Ativar Protocolo de Proteção e Notificação SINAN"
        }
    return {"category": "CLÍNICA_GERAL"}

# Monta a resposta final dependendo do caminho que o fluxo seguiu
def response_generator(state: AgentState):
    if state.get("category") == "SEGURANÇA_DA_MULHER":
        response = "Detectamos uma situação que requer cuidado especial e sigilo. Recomendamos o acolhimento imediato pela equipe de assistência social e psicologia."
    elif state.get("requires_emergency"):
        response = f"ALERTA: Seus sintomas indicam a necessidade de atendimento urgente. Próximo passo: {state['next_step']}."
    else:
        response = f"Análise concluída. Nível de risco: {state['risk_level']}. Recomendação: {state['next_step']}."
    
    return {"messages": [response]}

# Ligando os nos do grafo (LangGraph)
workflow = StateGraph(AgentState)

workflow.add_node("detect_violence", violence_detection_node)
workflow.add_node("triage", triage_node)
workflow.add_node("generate_response", response_generator)

workflow.set_entry_point("detect_violence")

workflow.add_edge("detect_violence", "triage")
workflow.add_edge("triage", "generate_response")
workflow.add_edge("generate_response", END)

app_graph = workflow.compile()
