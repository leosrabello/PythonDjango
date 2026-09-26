"""Testes da Frente 2 — CRUD de Categoria e os status codes esperados."""

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria


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
