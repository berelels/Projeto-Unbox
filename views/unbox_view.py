
import flet as ft
import sqlite3
class TelaPrincipalView:
     def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        self.controller.registrar_view(self)
 
        self.categoria = None
        self.item = None
        self.historico_list = None
        self.low_stock_card = None 
        self.low_stock_count_text = None
        self.categoria_dropdown = None
        self.patrimonio_input = None
        self.nome_item_input = None
        self.quantidade_input = None
        self.status_dropdown = None
        self.itens_data_table = None
        self.item_emprestimo_dropdown = None
        self.input_pessoa_emprestimo = None
        self.input_patrimonio_devolucao = None
        self.movimentacoes_data_table = None

        self.content_area = ft.Container(content=ft.Text("Carregando"))
        self.navigation_rail = None
       
     def construir(self):
            
            self.page.title = "UNBOX | Sistema de Inventário Escolar"
            self.page.window_width = 1000
            self.page.window_height = 800
            self.page.window_resizable = True 
            self.page.padding = 0 
            
            
            self.navigation_rail = ft.NavigationRail(
                selected_index=0, 
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100, 
                min_extended_width=200, 
                group_alignment=-1.0, 
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.Icons.DASHBOARD_OUTLINED,
                        selected_icon=ft.Icons.DASHBOARD,
                        label="Dashboard",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.CATEGORY_OUTLINED,
                        selected_icon=ft.Icons.CATEGORY,
                        label="Categorias",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.INVENTORY_2_OUTLINED,
                        selected_icon=ft.Icons.INVENTORY_2,
                        label="Itens",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.SWAP_HORIZ_OUTLINED,
                        selected_icon=ft.Icons.SWAP_HORIZ,
                        label="Movimentações",
                    ),
                ],
                on_change=self.controller.handle_navigation_change 
            )

           
            self.content_area.expand = True 
            self.content_area.padding = ft.padding.only(left=20, top=20, right=20)
            
           
            layout_principal = ft.Row(
                controls=[
                    self.navigation_rail,
                    ft.VerticalDivider(width=1), 
                    self.content_area,
                ],
                expand=True, 
                spacing=0 
            )

           
            self.page.add(layout_principal)
            
            
            self.controller.handle_navigation_change(type("E", (), {"data": "0"}))



 
     def _layout_cadastro_categoria(self):
    
        self.nome_categoria_input = ft.TextField(
        label="Nome da Categoria (Eletrônico, Mobiliário,Esportivo,Material Didático,Limpeza)",
        width=400,
        hint_text="Nome Único (Exigência do Carlos)"
    )

        self.categorias_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
        ],
        rows=[], 
    )
    
        return ft.Column([
        ft.Text(" Cadastro de Categorias", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        
        ft.Row([
            self.nome_categoria_input,
            ft.ElevatedButton(
                "Salvar Categoria",
                icon=ft.Icons.SAVE,
                
                on_click=self.controller.salvar_nova_categoria 
            ),
        ], alignment=ft.MainAxisAlignment.START),
        
        ft.Divider(),
        
        
        ft.Text("Categorias Existentes:", size=18, weight=ft.FontWeight.W_600),
        ft.Container(
            content=self.categorias_data_table,
            
            scroll=ft.ScrollMode.ADAPTIVE, 
            expand=True 
        )
    ], expand=True)

     def _layout_movimentacao(self):
        
      
        self.input_patrimonio_emprestimo = ft.TextField(
            label="Nº do Patrimônio",
            width=250,
            hint_text="Número na plaquinha de metal do item"
        )
        self.input_pessoa_emprestimo = ft.TextField(
            label="Nome do Professor/Responsável",
            width=300,
            hint_text=" Prof. Admistrador "
        )
        self.input_patrimonio_devolucao = ft.TextField(
            label="Nº do Patrimônio",
            width=250,
            hint_text="Item a ser devolvido"
        )
        self.movimentacoes_data_table = ft.DataTable(
            columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patrimônio")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Emprestado Para")),
            ft.DataColumn(ft.Text("Desde já")),
            ft.DataColumn(ft.Text("Ação")),
            ],
            rows=[]
        )

        return ft.Column([
        ft.Text(" Movimentações (Emprestimo e Devoluçao)", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(),

        ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Empréstimo (Saída do item)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_GREY_700),
                            self.input_patrimonio_emprestimo,
                            self.input_pessoa_emprestimo,
                            ft.ElevatedButton(
                                "Realizar o Empréstimo",
                                icon=ft.Icons.OUTBOX,
                               
                                on_click=self.controller.realizar_emprestimo 
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        width=400,
                    ),
                    elevation=5
                ),
                
                ft.VerticalDivider(width=1),
                
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Devolução (Entrada do item)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.DEEP_ORANGE_700),
                            self.input_patrimonio_devolucao,
                            ft.ElevatedButton(
                                "Registrar Devolução",
                                icon=ft.Icons.INBOX,
                               
                                on_click=self.controller.registrar_devolucao 
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        width=350,
                    ),
                    elevation=5
                ),
            ], wrap=True, alignment=ft.MainAxisAlignment.START),
            
            ft.Divider(height=20),
        ], expand=True)


     def _layout_cadastro_item(self):
        
      
        self.categoria_dropdown = ft.Dropdown(
            label="Categoria (Must Have: Select)",
            width=300,
            hint_text="Selecione a categoria do item (Ex: Eletrônico)",
            options=[] 
        )
        
     
        self.patrimonio_input = ft.TextField(
            label="Número de Patrimônio (Must Have: Único)",
            width=200,
            hint_text="Ex: 001234",
            
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        
       
        self.nome_item_input = ft.TextField(
            label="Nome do Item",
            width=400,
            hint_text="Ex: Projetor Epson X20, Cadeira de Escritório"
        )
        
       
        self.quantidade_input = ft.TextField(
            label="Quantidade em Estoque",
            width=150,
            hint_text="Ex: 10",
           
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        
       
        self.status_dropdown = ft.Dropdown(
            label="Status Inicial",
            width=200,
            options=[
                ft.dropdown.Option("Disponível"),
                ft.dropdown.Option("Manutenção"), 
            ],
            value="Disponível"
        )

     
        self.itens_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Patrimônio")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Qtd.")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[],
        )

        return ft.Column([
            ft.Text(" Cadastro de Itens e Ativos", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
           
            ft.Row([
                self.nome_item_input,
                self.patrimonio_input,
            ], alignment=ft.MainAxisAlignment.START),
            
           
            ft.Row([
                self.categoria_dropdown,
                self.quantidade_input,
                self.status_dropdown,
                
                ft.ElevatedButton(
                    "Salvar Item",
                    icon=ft.Icons.SAVE,
                   
                    on_click=self.controller.salvar_novo_item 
                ),
            ], alignment=ft.MainAxisAlignment.START),

            ft.Divider(),
            
           
            ft.Text("Inventário Atual:", size=18, weight=ft.FontWeight.W_600),
            ft.Container(
                content=self.itens_data_table,
                scroll=ft.ScrollMode.ADAPTIVE, 
                expand=True 
            )
        ], expand=True)
     
     

     def _layout_movimentacao(self):
        
        
        self.item_emprestimo_dropdown = ft.Dropdown(
            label="Buscar e Selecionar Item",
            width=350,
            hint_text="Digite o nome ou o patrimonio do item disponível para busca",
            options=[], 
            
            enable_filter=True,
           
        )
        
        
        self.input_pessoa_emprestimo = ft.TextField(
            label="Nome do Professor/Responsável",
            width=300,
            hint_text=" Prof. Admistrador "
        )
        
        
        self.input_patrimonio_devolucao = ft.TextField(
            label="Nº do Patrimônio (Devolução)",
            width=250,
            hint_text="Item a ser devolvido para o estoque"
        )
        self.movimentacoes_data_table = ft.DataTable(
            
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Patrimônio")),
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Emprestado Para")),
                ft.DataColumn(ft.Text("Desde já")),
                ft.DataColumn(ft.Text("Ação")),
            ],
            rows=[]
        )

        return ft.Column([
            ft.Text("Movimentações (Empréstimo e Devolução)", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.Row([
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Empréstimo (Saída do item)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_GREY_700),
                        
                            self.item_emprestimo_dropdown, 
                            self.input_pessoa_emprestimo,
                            ft.ElevatedButton(
                                "Realizar o Empréstimo",
                                icon=ft.Icons.OUTBOX,
                                on_click=self.controller.realizar_emprestimo 
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        width=400,
                    ),
                    elevation=5
                ),
                
                ft.VerticalDivider(width=1),
                
               
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Devolução (Entrada do item)", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.DEEP_ORANGE_700),
                            self.input_patrimonio_devolucao,
                            ft.ElevatedButton(
                                "Registrar Devolução",
                                icon=ft.Icons.INBOX,
                                on_click=self.controller.registrar_devolucao 
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.START),
                        padding=20,
                        width=350,
                    ),
                    elevation=5
                ),
            ], wrap=True, alignment=ft.MainAxisAlignment.START),
            
            ft.Divider(height=20),
            
            ft.Container(
                content=self.movimentacoes_data_table,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE
            )
        ], expand=True)
     
     def criar_botao_acao_admin(self, item_id: int, acao_controller, usuario: str):
       
      
        is_admin = usuario == 'ADMIN'
        
        
        if acao_controller.__name__ == 'excluir_categoria':
            icon = ft.Icons.DELETE
            color = ft.Colors.RED_600
        else: 
            icon = ft.Icons.EDIT
            color = ft.Colors.BLUE_600
            
        return ft.IconButton(
            icon=icon,
            icon_color=color,
            tooltip=f"ID: {item_id}",
            
            visible=is_admin, 
          
            on_click=lambda e: acao_controller(item_id) 
        )
     

     def _layout_dashboard(self):
        
        
        self.low_stock_count_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD)
        
        self.low_stock_card = ft.Container(
            content=ft.Column([
                ft.Text(" Alerta de Estoque Baixo", size=18, weight=ft.FontWeight.W_600),
                self.low_stock_count_text,
                ft.Text("Itens abaixo do estoque mínimo"),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=300,
            height=150,
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.BLUE_GREY_100, 
            alignment=ft.alignment.center,
        )

        return ft.Column([
            ft.Text(" Dashboard (Visão Geral)", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([
                self.low_stock_card,
            ], alignment=ft.MainAxisAlignment.START, wrap=True)
        ], expand=True)
        