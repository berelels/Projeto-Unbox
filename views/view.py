import flet as ft

class Unbox_View:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = None

        self.BG_COLOR, self.SIDEBAR_COLOR, self.CARD_COLOR = "#0f172a", "#1e293b", "#1e293b"
        self.TEXT_COLOR, self.TEXT_SUB = "#f1f5f9", "#94a3b8"
        self.COR_ACCENT, self.COR_VERDE = "#3b82f6", "#10b981"
        self.COR_LARANJA, self.COR_VERMELHO = "#f59e0b", "#ef4444"
        #configurações gerais:
        self.page.bgcolor = self.BG_COLOR
        self.page.padding = 0
        self.snack_bar = ft.SnackBar(content=ft.Text(""))
        self.page.overlay.append(self.snack_bar)
        self.area_conteudo = ft.Container(expand=True, padding=30)
        #cadastro:
        self.txt_patrimonio = self._criar_input("Nº Patrimônio (NTB-???)")
        self.txt_nome = self._criar_input("Nome do Item")
        self.dd_categoria = self._criar_dropdown("Categoria")
        #emprestimo:
        self.txt_emp_patrimonio = self._criar_input("Patrimônio", icone=ft.icons.QR_CODE)
        self.txt_emp_pessoa = self._criar_input()
        #tabela:
        self.tabela_itens = ft.DataTable(
            width=float("inf"), heading_row_color=self.BG_COLOR, data_row_color=self.CARD_COLOR,
            heading_row_height=50, data_row_max_height=60, column_spacing=20,
            columns=[
                ft.DataColumn(ft.Text("Patrimônio", color=self.TEXT_SUB, weight="bold")),
                ft.DataColumn(ft.Text("Nome", color=self.TEXT_SUB, weight="bold")),
                ft.DataColumn(ft.Text("Categoria", color=self.TEXT_SUB, weight="bold")),
                ft.DataColumn(ft.Text("Status", color=self.TEXT_SUB, weight="bold")),], rows=[])
        