# Guia de Execução - Tech Challenge Fase 3 (Especialista em Saúde da Mulher)

Este guia orienta como utilizar os datasets reais e realizar o fine-tuning do modelo para o desafio da Fase 3.

## 1. Preparação dos Dados
Embora o projeto contenha um script local (`src/data/download_data.py`), o processo foi automatizado para rodar diretamente no **Google Colab**.

Os datasets utilizados são:
- **Women Health Mini**: Dataset especializado em Ginecologia e Obstetrícia.
- **MedQuAD**: Dataset médico geral (filtrado para temas femininos).

## 2. Executando no Google Colab
Siga estes passos para treinar o modelo:

1.  Acesse o [Google Colab](https://colab.research.google.com/).
2.  Faça o upload do arquivo `notebooks/fine_tuning_medical.ipynb` (ou use a versão atualizada que deixei na pasta).
3.  No Colab, altere o tipo de ambiente para **T4 GPU** (Ambiente de Execução -> Alterar tipo de ambiente).
4.  Execute as células em ordem:
    -   **Célula 1**: Instala as bibliotecas (`transformers`, `peft`, `datasets`, etc).
    -   **Célula 2**: Baixa automaticamente o dataset real do Hugging Face.
    -   **Célula 3**: Carrega o modelo Llama-3 (versão 4-bit para caber no Colab gratuito).
    -   **Célula 4**: Inicia o treinamento (Fine-tuning).

## 3. Estrutura de Arquivos Gerada
Após o treinamento, o Colab criará uma pasta chamada `llama3-medical-fase3`. 
Você deve baixar essa pasta ou salvá-la no seu Google Drive para usar no seu Agente local.

## 4. Integrando com o Agente
No arquivo `src/agents/medical_flows.py`, da para apontar o modelo para o caminho onde salvou os pesos treinados.

---
**Nota sobre o Idioma:** Os datasets reais são majoritariamente em Inglês. Para a entrega final, o modelo treinado responderá melhor em Inglês, mas da para usar o Agente para traduzir as respostas.