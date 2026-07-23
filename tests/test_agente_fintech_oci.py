import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import importlib.util

spec = importlib.util.spec_from_file_location(
    "agente_fintech_oci",
    Path(__file__).resolve().parents[1] / "src" / "agente_fintech_oci.py",
)
agente = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agente)


class LoadDocumentsTests(unittest.TestCase):
    def test_load_documents_uses_resolved_data_directory(self):
        class FakeDirectoryLoader:
            def __init__(self, path, glob, loader_cls):
                self.path = path
                if path != str(agente.resolve_document_dir(None)):
                    raise AssertionError(f"Caminho inesperado: {path}")

            def load(self):
                return [SimpleNamespace(page_content="texto")]

        class FakeSplitter:
            def __init__(self, chunk_size, chunk_overlap, separators):
                self.chunk_size = chunk_size

            def split_documents(self, docs):
                return docs

        with patch.object(agente, "DirectoryLoader", FakeDirectoryLoader), patch.object(
            agente, "RecursiveCharacterTextSplitter", FakeSplitter
        ):
            result = agente.load_documents()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].page_content, "texto")


if __name__ == "__main__":
    unittest.main()
