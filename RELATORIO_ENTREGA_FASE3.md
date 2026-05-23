# RELATÓRIO - TECH CHALLENGE FASE 3
**Tema:** Assistente Médico Especializado em Saúde da Mulher com Fine-Tuning e LangGraph  
**Aluno:** Felippe de Barros Ribeiro  

### Links do Projeto:
* **Repositório GitHub:** [https://github.com/felipperibeiro/TechChallengeFiap-3](https://github.com/felipperibeiro/TechChallengeFiap-3)
* **Vídeo de Apresentação:** [Insira aqui o link do seu vídeo no YouTube]

---

## 1. Introdução e Objetivo
Dando continuidade ao desenvolvimento das fases anteriores, este projeto foca no desenvolvimento de um **Assistente Virtual Inteligente especializado em Saúde da Mulher**. O objetivo central foi construir um ecossistema seguro e ético de atendimento, que combina a flexibilidade e empatia conversacional de um LLM com o rigor regulatório e de segurança da informação exigido na área médica (conformidade com LGPD e prevenção de diagnósticos/prescrições indevidas). 

---

## 2. Metodologia e Tecnologias
A solução técnica foi arquitetada em três camadas principais de inteligência e segurança:

1. **Tomada de Decisão Baseada em Grafos (LangGraph):**
   * Estruturação do fluxo em um grafo de estado direcionado que avalia as entradas das usuárias.
   * **Nó de Detecção de Violência Doméstica (`detect_violence`):** Monitora gatilhos de agressão, ameaça e medo familiar, direcionando imediatamente a conversa para um canal acolhedor com suporte de assistência social e psicologia.
   * **Nó de Triagem Clínica (`triage`):** Avalia sintomas críticos (como sangramento, dor aguda e febre) para classificar o nível de risco entre "Alto" ou "Baixo/Médio", gerando encaminhamentos dinâmicos adequados (Pronto Socorro ou Consulta Eletiva).

2. **Camada de Guardrails Éticose de Privacidade (`MedicalGuardrails`):**
   * **Anonimização Automática de Dados:** Processamento de Regex para filtrar e remover CPFs de pacientes antes do envio aos modelos, preservando a privacidade (LGPD).
   * **Bloqueio de Prescrição Médica:** Monitoramento da resposta final para identificar palavras-chave ligadas à dosagem e indicação de remédios, injetando um aviso obrigatório (*disclaimer*) alertando que qualquer receita precisa de validação por um profissional de saúde habilitado.

3. **Especialização de LLM (Fine-Tuning do Llama-3 com QLoRA):**
   * Treinamento do modelo `unsloth/llama-3-8b-bnb-4bit` em GPU T4 do Google Colab usando adaptadores de baixa classificação (PEFT/LoRA).
   * Junção e curadoria de dados reais médicos (*MedQuAD* filtrado para temas de ginecologia e obstetrícia, e *Women Health* mini), totalizando mais de 10.000 exemplos de treino reais sobre a saúde feminina.

---

## 3. Resultados e Evolução do Fine-Tuning
O processo de fine-tuning realizado no Google Colab demonstrou a convergência bem-sucedida do modelo. Abaixo, apresenta-se o comportamento do erro (*training loss*) durante as 100 etapas de treinamento realizadas com o dataset real combinado:

| Step | Training Loss |
| :---: | :---: |
| 10 | 3.046749 |
| 20 | 2.040733 |
| 30 | 1.542177 |
| 40 | 1.556415 |
| 50 | 1.353251 |
| 60 | 1.297574 |
| 70 | 1.138168 |
| 80 | 1.094644 |
| 90 | 1.080742 |
| 100 | **1.009027** |

*Análise:* O decrescimento constante da perda do modelo (de ~3.04 para ~1.00) comprova a especialização bem-sucedida do Llama-3 na estrutura semântica de diálogos e protocolos de saúde feminina.

---

## 4. Exemplos de Execução do Sistema (Casos de Uso)

### Caso 1: Detecção de Violência e Acolhimento
* **Entrada (Usuária):** `"Tenho hematomas no braço e medo do que meu parceiro pode fazer."`
* **Saída (Assistente):** `"Detectamos uma situação que requer cuidado especial e sigilo. Recomendamos o acolhimento imediato pela equipe de assistência social e psicologia."`

### Caso 2: Triagem Clínica de Risco Alto (Encaminhamento de Urgência)
* **Entrada (Usuária):** `"Meu CPF é 123.456.789-00, estou com sangramento intenso e muita dor abdominal."`
* **Saída (Assistente):**
  *(Guardrail: O sistema detecta e exibe: [Guardrail]: Dados pessoais ocultados automaticamente.)*  
  `"ALERTA: Seus sintomas indicam a necessidade de atendimento urgente. Próximo passo: Encaminhamento Imediato ao Pronto Socorro."`

### Caso 3: Guardrail de Medicamentos (Bloqueio de Prescrição Direta)
* **Entrada (Usuária):** `"Gostaria de saber qual anticoncepcional posso tomar para parar a cólica."`
* **Saída (Assistente):** 
  `"[Resposta explicativa sobre métodos contraceptivos e tratamentos convencionais de cólica] ... [AVISO]: Isso é apenas uma orientação com base nos protocolos. Qualquer receita ou remédio precisa ser avaliado por um médico de verdade antes."`

---

## 5. Conclusão
O projeto consolida uma arquitetura avançada de IA para saúde de forma altamente escalável e segura. O uso combinado de grafos estruturados garante controle absoluto sobre o fluxo clínico de encaminhamento e denúncia de violência doméstica. Concomitantemente, a presença ativa de guardrails em tempo real protege a privacidade das usuárias sob a égide da LGPD e impede a automação imprudente de condutas de prescrição. Trata-se de uma solução madura e pronta para apoiar a triagem clínica eficiente em larga escala.
