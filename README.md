# 🏦 Agente de IA para Banco Digital & Fintech — Challenge Alura / OCI

[![Oracle Cloud Infrastructure](https://img.shields.io/badge/OCI-Generative%20AI-red?logo=oracle)](https://www.oracle.com/cloud/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green)](https://www.langchain.com/)

Solução de **RAG (Retrieval-Augmented Generation)** desenvolvida para o **Challenge Alura + Oracle Cloud Infrastructure (OCI)**. Este projeto cria um assistente de IA regulado para autoatendimento e consulta de documentos normativos de uma fintech/banco digital.

---

## 📌 Visão Geral

O agente processa documentos regulamentares em PDF e usa LangChain + OCI Generative AI para responder perguntas sobre tarifas, limites, LGPD, fraudes e políticas internas. A intenção é oferecer respostas baseadas exclusivamente no contexto dos documentos carregados, com guardrails para evitar informações fora do escopo.

---

## 🚀 O que está incluído

- `src/agente_fintech_oci.py` — script Python principal do agente
- `src/agente_fintech_oci.ipynb` — notebook de desenvolvimento e demonstração
- `requirements.txt` — lista de dependências Python
- `data/` — pasta onde os PDFs regulatórios devem estar para o agente carregar
- `docs/` — diretórios de apoio para dados e documentação

---

## 🏗️ Arquitetura da Solução

```text
[ Documentos PDF ]
   ├── 01_politica_privacidade.pdf
   ├── 02_termos_condicoes.pdf
   ├── 03_faq_transacoes_limites.pdf
   ├── 04_seguranca_fraudes.pdf
   └── 05_tarifas_comissoes.pdf
           │
           ▼
[ Ingestão & Chunking ] ──► PyPDFLoader + RecursiveCharacterTextSplitter
           │
           ▼
[ Prompt de Contexto ] ──► Sistema regrado + contexto recuperado
           │
           ▼
[ OCI Generative AI ] ──► OCIGenAI (Cohere Command R+)
           │
           ▼
[ Resposta Contextual ] ──► Saída segura e orientada por documentos
```

---

## ✅ Pré-requisitos

- Python 3.11 ou superior
- `pip` instalado
- credenciais OCI configuradas
- arquivos PDF dentro de `data/`

---

## ⚙️ Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se estiver usando o notebook, execute a primeira célula para instalar as dependências antes de prosseguir.

---

## 🔧 Configuração OCI

Defina as variáveis de ambiente necessárias para o acesso à OCI:

```powershell
setx OCI_COMPARTMENT_ID "ocid1.compartment.oc1..seu_compartment_ocid"
setx OCI_GENAI_ENDPOINT "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
```

Se a variável `OCI_COMPARTMENT_ID` não estiver definida, o notebook e o script mostrarão uma mensagem indicando que a chamada ao modelo OCI precisa de um OCID válido.
Se estiver executando em uma VM OCI com Instance Principal, atualize `auth_type` em `src/agente_fintech_oci.py` de `API_KEY` para `INSTANCE_PRINCIPAL`.

---

## ▶️ Execução

```powershell
python src\agente_fintech_oci.py
```

O script procura automaticamente por PDFs em `data/` e, se não encontrar nenhum, informa o erro antes de tentar usar a OCI.

Para testar com uma pergunta customizada:

```powershell
setx OCI_BANK_QUERY "Qual é a tarifa para saque no Banco24Horas?"
python src\agente_fintech_oci.py
```

---

## 💡 Uso do Notebook

O notebook `src/agente_fintech_oci.ipynb` apresenta a versão exploratória do pipeline, incluindo:

- instalação de dependências
- configuração OCI
- ingestão de PDFs
- chunking e pré-processamento de documentos
- criação do prompt e chamada ao modelo

---

## 📌 Observações importantes

- O agente deve responder apenas com base nos documentos carregados.
- Garanta que os PDFs estejam dentro de `data/` e estejam atualizados e consistentes com as políticas do banco.
- Em produção, revise políticas de segurança e autenticação antes de expor qualquer serviço.

---

## 📝 Estrutura de diretórios

```text
ChallengeAluraAgente/
├── data/
├── docs/
├── src/
│   ├── agente_fintech_oci.ipynb
│   └── agente_fintech_oci.py
├── requirements.txt
└── README.md
```
