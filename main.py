import flet as ft
from views.unbox_view import TelaPrincipalView
from controllers.controller import Unbox_Controller

def main(page: ft.Page):
    """
    Função principal que inicializa o sistema MVC.
    """
    # Inicializa o controller
    controller = Unbox_Controller(page)
    
    # Inicializa a view e passa o controller
    view = TelaPrincipalView(page=page, controller=controller)
    
    # Constrói a interface
    view.construir()

if __name__ == "__main__":
    ft.app(target=main)