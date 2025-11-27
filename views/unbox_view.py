
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
        
        self.content_area = ft.Container(content=ft.Text("Carregando"))
        self.navigation_rail = None
       
     def construir(self):
            
            self.page.title = "EduStock | Sistema de Inventário Escolar"
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
                        icon=ft.icons.DASHBOARD_OUTLINED,
                        selected_icon=ft.icons.DASHBOARD,
                        label="Dashboard",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.CATEGORY_OUTLINED,
                        selected_icon=ft.icons.CATEGORY,
                        label="Categorias",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.INVENTORY_2_OUTLINED,
                        selected_icon=ft.icons.INVENTORY_2,
                        label="Itens",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.SWAP_HORIZ_OUTLINED,
                        selected_icon=ft.icons.SWAP_HORIZ,
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
            
            
            self.controller.handle_navigation_change(ft.ControlEvent(data="0"))
        

