import flet as ft
from models import Unbox_Model
from views import Unbox_View

class Unbox_Controller:
    def __init__(self, page: ft.Page):
        self.page = page
        self.model = Unbox_Model()
        self.view = Unbox_View(page)

        self.view.controller = self
        self.view.carregar_interface()
        self.preencher_categorias()

    def preencher_categorias(self):
        try:
            dados_categorias = self.model.obter_categorias()
            opcoes_drop = []
            for id, nome in dados_categorias:
                opcoes_drop.append(ft.dropdown.Option(text=nome))
                
        except Exception as e:
            self.view.mostrar_mensagem(f"Erro ao carregar categorias: {e}", ft.colors.RED)
        self.view.dd_categoria.options = opcoes_drop

    def salvar_item(self, e):
        patrimonio = self.view.txt_patrimonio.value
