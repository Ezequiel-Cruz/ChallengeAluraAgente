import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import OCIGenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

DEFAULT_DOCUMENT_DIRS = [Path("data"), Path("documentos_fintech")]
DEFAULT_COMPARTMENT_ID = os.getenv("OCI_COMPARTMENT_ID", "").strip()
DEFAULT_OCI_ENDPOINT = os.getenv("OCI_GENAI_ENDPOINT", "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com").strip()


def resolve_document_dir(document_dir: Path | None = None) -> Path:
    """Resolve o diretório de documentos a partir do workspace atual."""
    candidates = []
    if document_dir is not None:
        candidates.append(document_dir)
    candidates.extend(DEFAULT_DOCUMENT_DIRS)

    for candidate in candidates:
        resolved = candidate if candidate.is_absolute() else Path(__file__).resolve().parent.parent / candidate
        if resolved.exists():
            return resolved

    return Path(__file__).resolve().parent.parent / "data"


def load_documents(document_dir: Path | None = None):
    """Carrega e divide PDFs regulatórios para criação da base de contexto."""
    resolved_dir = resolve_document_dir(document_dir)
    if not resolved_dir.exists():
        raise FileNotFoundError(
            f"Diretório de documentos não encontrado: {resolved_dir}. "
            "Coloque os PDFs na pasta data/ ou ajuste o caminho no script."
        )

    loader = DirectoryLoader(str(resolved_dir), glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    if not documents:
        raise FileNotFoundError(f"Nenhum PDF encontrado em {resolved_dir}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""],
    )
    return text_splitter.split_documents(documents)


def build_llm(compartment_id: str = DEFAULT_COMPARTMENT_ID, endpoint: str = DEFAULT_OCI_ENDPOINT):
    """Inicializa o modelo generativo OCI usado pelo agente."""
    if not compartment_id:
        raise ValueError(
            "OCI_COMPARTMENT_ID não está configurado. Defina a variável de ambiente com um OCID válido da OCI."
        )
    return OCIGenAI(
        model_id="cohere.command-r-plus",
        service_endpoint=endpoint,
        compartment_id=compartment_id,
        model_kwargs={"temperature": 0.1, "max_tokens": 600},
        auth_type="API_KEY",
    )


def build_chain(llm):
    """Cria a cadeia de prompt e parser para geração de respostas."""
    system_prompt = """
Você é o assistente virtual oficial de atendimento da Fintech / Banco Digital.
Sua função é responder dúvidas dos clientes com precisão, cordialidade e tom profissional.

REGRAS DE CONDUTA E SEGURANÇA:
1. Responda APENAS com base nos documentos regulatórios fornecidos no contexto abaixo.
2. Se a informação sobre limites, tarifas, fraudes ou privacidade não estiver explicitada no contexto, informe categoricamente que não possui essa informação e oriente o cliente a entrar em contato com o suporte humano.
3. NUNCA solicite ou confirme dados sensíveis do cliente (como senhas, CVV do cartão ou tokens Pix) no chat.

Contexto Regulatório:
{contexto}
"""
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{pergunta}")]
    )
    return prompt | llm | StrOutputParser()


def consultar_banco_digital(pergunta: str, chunks):
    """Consulta o agente usando os primeiros blocos processados para compor o contexto."""
    contexto = "\n\n---\n\n".join([doc.page_content for doc in chunks[:4]])
    chain = build_chain(build_llm())
    return chain.invoke({"contexto": contexto, "pergunta": pergunta})


def main():
    try:
        documents = load_documents()
    except FileNotFoundError as error:
        print(error)
        return

    try:
        pergunta = os.getenv(
            "OCI_BANK_QUERY",
            "Qual é a tarifa para saque no Banco24Horas e qual o limite do Pix noturno?",
        )
        resposta = consultar_banco_digital(pergunta, documents)
    except ValueError as error:
        print(error)
        return

    print("Pergunta:", pergunta)
    print("Resposta:\n", resposta)


if __name__ == "__main__":
    main()
