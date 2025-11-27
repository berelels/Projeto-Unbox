import flet as ft
from views.unbox_view import TelaPrincipalView
# Exemplo Mínimo de Estrutura (Não é o código final, é para entender o conceito)

# 1. Defina o Controlador
class AppController:
    # ... lógica de navegação aqui

# 2. Defina o Ponto de Entrada
    def main(page: ft.Page):
        # Instancia o Controller
        controller = AppController(page)
        # Instancia a View Principal
        app_view = TelaPrincipalView(page, controller)
        # Chama o método que MONTA a estrutura principal na page
        app_view.construir()
        
    # 3. Execução
    if __name__ == "__main__":
        ft.app(target=main)