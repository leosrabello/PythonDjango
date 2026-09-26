"""Testes da API de categorias e produtos."""

from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Produto


class CategoriaAPITests(APITestCase):
    url = "/api/categorias/"

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Notebooks", descricao="Portáteis e ultrabooks"
        )

    def test_lista_vem_paginada(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn("results", resposta.data)
        self.assertEqual(resposta.data["count"], 1)

    def test_detalhe_existente(self):
        resposta = self.client.get(f"{self.url}{self.categoria.id}/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["nome"], "Notebooks")

    def test_detalhe_inexistente_da_404(self):
        resposta = self.client.get(f"{self.url}999/")
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def test_criar_devolve_201(self):
        resposta = self.client.post(
            self.url, {"nome": "Smartphones", "descricao": "Celulares"}, format="json"
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 2)

    def test_criar_sem_nome_da_400(self):
        resposta = self.client.post(self.url, {"descricao": "sem nome"}, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nome", resposta.data)

    def test_criar_com_nome_em_branco_da_400(self):
        resposta = self.client.post(self.url, {"nome": "   "}, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_com_nome_duplicado_da_400(self):
        resposta = self.client.post(self.url, {"nome": "Notebooks"}, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_substitui(self):
        resposta = self.client.put(
            f"{self.url}{self.categoria.id}/",
            {"nome": "Notebooks Gamer", "descricao": "Alto desempenho"},
            format="json",
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nome, "Notebooks Gamer")

    def test_patch_altera_so_um_campo(self):
        resposta = self.client.patch(
            f"{self.url}{self.categoria.id}/",
            {"descricao": "Só a descrição"},
            format="json",
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nome, "Notebooks")
        self.assertEqual(self.categoria.descricao, "Só a descrição")

    def test_delete_devolve_204(self):
        resposta = self.client.delete(f"{self.url}{self.categoria.id}/")
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Categoria.objects.count(), 0)

    def test_delete_inexistente_da_404(self):
        resposta = self.client.delete(f"{self.url}999/")
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)


class ProdutoAPITests(APITestCase):
    url = "/api/produtos/"

    def setUp(self):
        self.notebooks = Categoria.objects.create(nome="Notebooks")
        self.smartphones = Categoria.objects.create(nome="Smartphones")
        self.produto = Produto.objects.create(
            nome="Notebook Pro",
            descricao="Notebook para trabalho",
            preco=Decimal("4999.90"),
            estoque=8,
            categoria=self.notebooks,
        )

    def test_lista_paginada_com_categoria_aninhada(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["count"], 1)
        produto = resposta.data["results"][0]
        self.assertEqual(produto["categoria"]["id"], self.notebooks.id)
        self.assertEqual(produto["categoria"]["nome"], "Notebooks")
        self.assertNotIn("categoria_id", produto)

    def test_criar_com_categoria_id_devolve_categoria_aninhada(self):
        resposta = self.client.post(
            self.url,
            {
                "nome": "Smartphone X",
                "descricao": "Tela OLED",
                "preco": "2199.90",
                "estoque": 12,
                "categoria_id": self.smartphones.id,
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data["categoria"]["id"], self.smartphones.id)
        self.assertNotIn("categoria_id", resposta.data)
        self.assertTrue(
            Produto.objects.filter(
                nome="Smartphone X", categoria=self.smartphones
            ).exists()
        )

    def test_criar_sem_categoria_da_400(self):
        resposta = self.client.post(
            self.url,
            {"nome": "Produto", "preco": "10.00", "estoque": 1},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categoria_id", resposta.data)

    def test_criar_com_categoria_inexistente_da_400(self):
        resposta = self.client.post(
            self.url,
            {
                "nome": "Produto",
                "preco": "10.00",
                "estoque": 1,
                "categoria_id": 999,
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categoria_id", resposta.data)

    def test_patch_pode_trocar_a_categoria(self):
        resposta = self.client.patch(
            f"{self.url}{self.produto.id}/",
            {"categoria_id": self.smartphones.id, "estoque": 5},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["categoria"]["id"], self.smartphones.id)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.categoria, self.smartphones)
        self.assertEqual(self.produto.estoque, 5)

    def test_delete_devolve_204(self):
        resposta = self.client.delete(f"{self.url}{self.produto.id}/")

        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Produto.objects.filter(id=self.produto.id).exists())

    def test_filtra_por_categoria(self):
        Produto.objects.create(
            nome="Smartphone X",
            preco=Decimal("2199.90"),
            estoque=3,
            categoria=self.smartphones,
        )

        resposta = self.client.get(self.url, {"categoria": self.smartphones.id})

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["count"], 1)
        self.assertEqual(resposta.data["results"][0]["nome"], "Smartphone X")

    def test_filtro_com_categoria_invalida_da_400(self):
        resposta = self.client.get(self.url, {"categoria": "abc"})

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categoria", resposta.data)

    def test_busca_por_nome_e_categoria(self):
        resposta_nome = self.client.get(self.url, {"search": "Pro"})
        resposta_categoria = self.client.get(self.url, {"search": "Notebooks"})

        self.assertEqual(resposta_nome.data["count"], 1)
        self.assertEqual(resposta_categoria.data["count"], 1)

    def test_ordenacao_por_preco(self):
        Produto.objects.create(
            nome="Mouse",
            preco=Decimal("99.90"),
            estoque=20,
            categoria=self.notebooks,
        )

        resposta = self.client.get(self.url, {"ordering": "preco"})

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["results"][0]["nome"], "Mouse")

    def test_preco_e_estoque_negativos_dao_400(self):
        resposta = self.client.post(
            self.url,
            {
                "nome": "Inválido",
                "preco": "-1.00",
                "estoque": -1,
                "categoria_id": self.notebooks.id,
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("preco", resposta.data)
        self.assertIn("estoque", resposta.data)

    def test_paginacao_limita_a_dez_resultados(self):
        for indice in range(10):
            Produto.objects.create(
                nome=f"Produto {indice:02d}",
                preco=Decimal("10.00"),
                estoque=1,
                categoria=self.notebooks,
            )

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["count"], 11)
        self.assertEqual(len(resposta.data["results"]), 10)
        self.assertIsNotNone(resposta.data["next"])
