"""
Interface Moderna em Flet para o Sistema de Gestão de Obras
Tiago Rizzetto
"""
import flet as ft
import os
from datetime import datetime
from cadastro_obra.cadastro import CadastroObra
from cadastro_insumo.cadastro import CadastroInsumo
from cadastro_funcionario.cadastro import CadastroFuncionario
from pages.pagina_obras import PaginaObras
from pages.pagina_insumos import PaginaInsumos
from pages.pagina_funcionarios import PaginaFuncionarios
from pages.pagina_dashboard import PaginaDashboard


class SistemaGestaoObras:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gestão de Obras - Tiago Rizzetto"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window_width = 1400
        self.page.window_height = 800
        self.page.window_min_width = 1200
        self.page.window_min_height = 700
        
        # Inicializa cadastros
        self.cadastro_obra = CadastroObra("obras.json")
        self.cadastro_insumo = CadastroInsumo("insumos.db")
        self.cadastro_funcionario = CadastroFuncionario("funcionarios.json")
        
        # Inicializa páginas (passar self para permitir recarregamento)
        self.pg_obras = PaginaObras(page, self.cadastro_obra, self)
        self.pg_insumos = PaginaInsumos(page, self.cadastro_insumo, self)
        self.pg_funcionarios = PaginaFuncionarios(page, self.cadastro_funcionario, self)
        self.pg_dashboard = PaginaDashboard(page, self.cadastro_obra, self.cadastro_insumo, self.cadastro_funcionario)
        
        # Página atual
        self.pagina_atual = 0
        
        # Configurar página
        self.setup_page()
    
    def setup_page(self):
        """Configura a página inicial"""
        # Container principal com menu lateral
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Início"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CONSTRUCTION_OUTLINED,
                    selected_icon=ft.Icons.CONSTRUCTION,
                    label="Obras"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    selected_icon=ft.Icons.INVENTORY_2,
                    label="Insumos"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PEOPLE_OUTLINED,
                    selected_icon=ft.Icons.PEOPLE,
                    label="Funcionários"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard"
                ),
            ],
            on_change=self.mudar_pagina,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )
        
        # Container de conteúdo
        self.conteudo = ft.Container(
            content=self.criar_tela_inicial(),
            expand=True,
            padding=20,
        )
        
        # Layout principal
        self.page.add(
            ft.Row(
                [
                    self.rail,
                    ft.VerticalDivider(width=1),
                    self.conteudo,
                ],
                expand=True,
                spacing=0,
            )
        )
    
    def criar_tela_inicial(self):
        """Cria a tela inicial com logo e boas-vindas"""
        logo_path = "logojpg.PNG"
        
        # Verifica se o logo existe
        logo_widget = None
        if os.path.exists(logo_path):
            logo_widget = ft.Image(
                src=logo_path,
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            logo_widget = ft.Container(
                content=ft.Icon(
                    ft.Icons.ACCOUNT_BALANCE,
                    size=150,
                    color=ft.Colors.BLUE_700,
                ),
                width=300,
                height=300,
                alignment=ft.alignment.center,
            )
        
        return ft.Column(
            [
                ft.Container(height=50),
                # Logo
                ft.Container(
                    content=logo_widget,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=20),
                # Título
                ft.Text(
                    "Gestão de Obra",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                ft.Text(
                    "Tiago Rizzetto",
                    size=28,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.BLUE_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=40),
                # Cards de estatísticas
                ft.Row(
                    [
                        self.criar_card_estatistica(
                            "Obras",
                            str(len(self.cadastro_obra.listar())),
                            ft.Icons.CONSTRUCTION,
                            ft.Colors.BLUE_400,
                        ),
                        self.criar_card_estatistica(
                            "Insumos",
                            str(len(self.cadastro_insumo.listar())),
                            ft.Icons.INVENTORY_2,
                            ft.Colors.GREEN_400,
                        ),
                        self.criar_card_estatistica(
                            "Funcionários",
                            str(len(self.cadastro_funcionario.listar(apenas_ativos=True))),
                            ft.Icons.PEOPLE,
                            ft.Colors.ORANGE_400,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Container(height=30),
                # Mensagem
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Bem-vindo ao Sistema de Gestão de Obras",
                                size=20,
                                color=ft.Colors.GREY_700,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                "Selecione uma opção no menu lateral para começar",
                                size=16,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def criar_card_estatistica(self, titulo, valor, icone, cor):
        """Cria um card de estatística"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icone, size=50, color=cor),
                    ft.Container(height=10),
                    ft.Text(valor, size=36, weight=ft.FontWeight.BOLD, color=cor),
                    ft.Text(titulo, size=16, color=ft.Colors.GREY_700),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=200,
            height=180,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK12,
            ),
        )
    
    def mudar_pagina(self, e):
        """Muda a página ao clicar no menu"""
        indice = e.control.selected_index
        self.pagina_atual = indice
        
        if indice == 0:
            self.conteudo.content = self.criar_tela_inicial()
        elif indice == 1:
            self.conteudo.content = self.pg_obras.criar_pagina()
        elif indice == 2:
            self.conteudo.content = self.pg_insumos.criar_pagina()
        elif indice == 3:
            self.conteudo.content = self.pg_funcionarios.criar_pagina()
        elif indice == 4:
            self.conteudo.content = self.pg_dashboard.criar_pagina()
        
        self.page.update()
    
    def recarregar_pagina_atual(self):
        """Recarrega a página atual após mudanças nos dados"""
        if self.pagina_atual == 0:
            self.conteudo.content = self.criar_tela_inicial()
        elif self.pagina_atual == 1:
            self.conteudo.content = self.pg_obras.criar_pagina()
        elif self.pagina_atual == 2:
            self.conteudo.content = self.pg_insumos.criar_pagina()
        elif self.pagina_atual == 3:
            self.conteudo.content = self.pg_funcionarios.criar_pagina()
        elif self.pagina_atual == 4:
            self.conteudo.content = self.pg_dashboard.criar_pagina()
        
        self.page.update()
    
    def criar_pagina_obras(self):
        """Cria a página de obras (compatibilidade)"""
        return self.pg_obras.criar_pagina()
    
    def criar_pagina_insumos(self):
        """Cria a página de insumos (compatibilidade)"""
        return self.pg_insumos.criar_pagina()
    
    def criar_pagina_funcionarios(self):
        """Cria a página de funcionários (compatibilidade)"""
        return self.pg_funcionarios.criar_pagina()
    
    def criar_pagina_dashboard(self):
        """Cria a página de dashboard (compatibilidade)"""
        return self.pg_dashboard.criar_pagina()


def main(page: ft.Page):
    """Função principal"""
    SistemaGestaoObras(page)


if __name__ == "__main__":
    ft.app(target=main)
