import unittest
import os
from io import StringIO
from contextlib import redirect_stdout
from algoritmo import (
    busca_binaria,
    desfazer_remocao,
    salvar_log,
    log_acoes,
    historico_remocoes
)

class TestFuncoesComplementares(unittest.TestCase):

    def setUp(self):
        self.nomes = ["Ana", "Bruno", "João", "Lucas", "Luiz", "Maria", "Pedro"]
        self.nomes.sort()
        log_acoes.clear()
        historico_remocoes.clear()

    def test_remocao_e_desfazer(self):
        nome = "Lucas"
        index = self.nomes.index(nome)
        self.nomes.remove(nome)
        historico_remocoes.append((nome, index))

        # desfazendo
        desfazer_remocao(self.nomes, nome_atual="Lucas")
        self.assertIn("Lucas", self.nomes)
        self.assertIn("Nome restaurado: Lucas", log_acoes)

    def test_desfazer_nome_errado(self):
        nome = "Maria"
        index = self.nomes.index(nome)
        self.nomes.remove(nome)
        historico_remocoes.append((nome, index))

        # tentar desfazer outro nome
        f = StringIO()
        with redirect_stdout(f):
            desfazer_remocao(self.nomes, nome_atual="João")
        saida = f.getvalue()
        self.assertIn("⚠️ Não é possível desfazer", saida)
        self.assertNotIn("Maria", self.nomes)  # não restaurou

    def test_salvar_log(self):
        log_acoes.append("Teste de log")
        salvar_log()
        with open("log_acoes.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("Teste de log", conteudo)

    def tearDown(self):
        if os.path.exists("log_acoes.txt"):
            os.remove("log_acoes.txt")

if __name__ == '__main__':
    unittest.main()
