# Tech Challenge - Fase 3: Assistente Médico Especializado (Saúde da Mulher)

Este repositório contém a entrega completa para a **Fase 3 do Tech Challenge (8IADT)**. O projeto evolui as automações anteriores para um assistente virtual inteligente capaz de realizar triagem, identificar situações de risco e fornecer orientações baseadas em protocolos médicos.

## Tecnologias Utilizadas
- **LangChain**: Orquestração de pipelines de linguagem.
- **LangGraph**: Controle de fluxos de decisão clínica e segurança.
- **Fine-tuning (QLoRA)**: Especialização do modelo Llama-3 em dados médicos.
- **Python**: Linguagem base do projeto.

## 📁 Estrutura do Projeto
- `data/`: Contém o dataset sintético (`.jsonl`) utilizado para o fine-tuning.
- `notebooks/`: Notebook pronto para execução no **Google Colab** para o treinamento do modelo.
- `src/`: 
    - `agents/`: Definição dos grafos de decisão (triagem e segurança).
    - `utils/`: Guardrails de segurança e anonimização de dados.
- `main.py`: Script de demonstração dos fluxos.

## 🛠️ Como Executar Localmente

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure o ambiente**:
   Crie um arquivo `.env` (opcional, dependendo do provedor de LLM que desejar integrar).

3. **Rode a demonstração**:
   ```bash
   python main.py
   ```

## Fine-tuning (Google Colab)
Devido à necessidade de GPU, o processo de treinamento do modelo está documentado e preparado no arquivo `notebooks/fine_tuning_medical.ipynb`. 
1. Faça o upload deste arquivo no Google Colab.
2. Certifique-se de estar usando um ambiente com T4 GPU ou superior.
3. O notebook instalará automaticamente as bibliotecas e realizará o treino com os dados sintéticos fornecidos.

## Segurança e Ética
O projeto implementa:
- **Guardrails**: Impede que o assistente prescreva medicamentos sem aviso de validação humana.
- **Detecção de Violência**: Fluxo prioritário para acionamento de redes de proteção.
- **Anonimização**: Tratamento inicial de dados sensíveis.

---
**Entregável da Fase 3 - FIAP Postech**
