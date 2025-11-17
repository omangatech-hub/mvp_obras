"""
Página de Gerenciamento de Obras
"""
import flet as ft
from datetime import datetime
from cadastro_obra.obra import Obra


class PaginaObras:
    def __init__(self, page: ft.Page, cadastro_obra, app=None):
        self.page = page
        self.cadastro = cadastro_obra
        self.app = app
        self.dialog_aberto = None
        self.obra_selecionada = None
        
        # Campos do formulário
        self.txt_nome = ft.TextField(label="Nome da Obra", width=400)
        self.dt_inicio = ft.TextField(label="Data de Início (DD/MM/AAAA)", width=200)
        self.dt_termino_previsto = ft.TextField(label="Término Previsto (DD/MM/AAAA)", width=200)
        self.txt_custo_estimado = ft.TextField(label="Custo Estimado (R$)", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        
    def criar_pagina(self):
        """Cria a página principal de obras"""
        # Tabela de obras
        self.tabela_obras = self.criar_tabela_obras()
        
        return ft.Column(
            [
                # Cabeçalho
                ft.Row(
                    [
                        ft.Text("🏗️ Gerenciamento de Obras", size=32, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "➕ Nova Obra",
                            on_click=self.abrir_dialog_cadastro,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),
                ft.Divider(height=20),
                
                # Cards de resumo
                ft.Row(
                    [
                        self.criar_card_resumo(
                            "Total de Obras",
                            str(len(self.cadastro.listar())),
                            ft.Icons.CONSTRUCTION,
                            ft.Colors.BLUE_400,
                        ),
                        self.criar_card_resumo(
                            "Em Andamento",
                            str(len([o for o in self.cadastro.listar() if not o.termino_real])),
                            ft.Icons.HOURGLASS_EMPTY,
                            ft.Colors.ORANGE_400,
                        ),
                        self.criar_card_resumo(
                            "Finalizadas",
                            str(len([o for o in self.cadastro.listar() if o.termino_real])),
                            ft.Icons.CHECK_CIRCLE,
                            ft.Colors.GREEN_400,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(height=20),
                
                # Tabela
                ft.Container(
                    content=self.tabela_obras,
                    expand=True,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def criar_card_resumo(self, titulo, valor, icone, cor):
        """Cria card de resumo"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icone, size=40, color=cor),
                    ft.Column(
                        [
                            ft.Text(valor, size=28, weight=ft.FontWeight.BOLD, color=cor),
                            ft.Text(titulo, size=14, color=ft.Colors.GREY_700),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=15,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=250,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
        )
    
    def criar_tabela_obras(self):
        """Cria a tabela de obras"""
        obras = self.cadastro.listar()
        
        linhas = []
        for obra in obras:
            status_cor = ft.Colors.GREEN_600 if obra.termino_real else ft.Colors.ORANGE_600
            status_texto = "Finalizada" if obra.termino_real else "Em Andamento"
            
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(obra.id))),
                        ft.DataCell(ft.Text(obra.nome)),
                        ft.DataCell(ft.Text(obra.inicio.strftime("%d/%m/%Y"))),
                        ft.DataCell(ft.Text(obra.termino_previsto.strftime("%d/%m/%Y"))),
                        ft.DataCell(ft.Text(f"R$ {obra.custo_estimado:,.2f}")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(status_texto, color=ft.Colors.WHITE, size=12),
                                bgcolor=status_cor,
                                padding=5,
                                border_radius=5,
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=ft.Colors.BLUE_700,
                                        tooltip="Editar",
                                        on_click=lambda e, o=obra: self.abrir_dialog_edicao(o),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        icon_color=ft.Colors.GREEN_700,
                                        tooltip="Finalizar",
                                        on_click=lambda e, o=obra: self.abrir_dialog_finalizar(o),
                                        disabled=obra.termino_real is not None,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED_700,
                                        tooltip="Excluir",
                                        on_click=lambda e, o=obra: self.confirmar_exclusao(o),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ],
                )
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Início", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Término Prev.", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Custo Estimado", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=linhas,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
        )
    
    def abrir_dialog_cadastro(self, e):
        """Abre dialog para cadastrar nova obra"""
        self.limpar_formulario()
        
        dialog = ft.AlertDialog(
            title=ft.Text("➕ Cadastrar Nova Obra"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.txt_nome,
                        ft.Row([self.dt_inicio, self.dt_termino_previsto]),
                        self.txt_custo_estimado,
                    ],
                    tight=True,
                ),
                width=500,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Salvar", on_click=self.salvar_obra, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def abrir_dialog_edicao(self, obra):
        """Abre dialog para editar obra"""
        self.obra_selecionada = obra
        self.txt_nome.value = obra.nome
        self.dt_inicio.value = obra.inicio.strftime("%d/%m/%Y")
        self.dt_termino_previsto.value = obra.termino_previsto.strftime("%d/%m/%Y")
        self.txt_custo_estimado.value = str(obra.custo_estimado)
        
        dialog = ft.AlertDialog(
            title=ft.Text("✏️ Editar Obra"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.txt_nome,
                        ft.Row([self.dt_inicio, self.dt_termino_previsto]),
                        self.txt_custo_estimado,
                    ],
                    tight=True,
                ),
                width=500,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Atualizar", on_click=self.atualizar_obra, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def abrir_dialog_finalizar(self, obra):
        """Abre dialog para finalizar obra"""
        self.obra_selecionada = obra
        
        txt_termino_real = ft.TextField(label="Data de Término Real (DD/MM/AAAA)", width=200)
        txt_custo_real = ft.TextField(label="Custo Real (R$)", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        
        def finalizar(e):
            try:
                termino_real = datetime.strptime(txt_termino_real.value, "%d/%m/%Y")
                custo_real = float(txt_custo_real.value.replace(",", "."))
                
                sucesso, msg = self.cadastro.finalizar_obra(obra.id, termino_real, custo_real)
                
                if sucesso:
                    self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                    self.atualizar_tabela()
                else:
                    self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
                self.fechar_dialog(e)
            except ValueError as ex:
                self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
        
        dialog = ft.AlertDialog(
            title=ft.Text("✅ Finalizar Obra"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Obra: {obra.nome}", weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        txt_termino_real,
                        txt_custo_real,
                    ],
                    tight=True,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Finalizar", on_click=finalizar, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def salvar_obra(self, e):
        """Salva nova obra"""
        try:
            inicio = datetime.strptime(self.dt_inicio.value, "%d/%m/%Y")
            termino_previsto = datetime.strptime(self.dt_termino_previsto.value, "%d/%m/%Y")
            custo_estimado = float(self.txt_custo_estimado.value.replace(",", "."))
            
            obra = Obra(
                nome=self.txt_nome.value,
                inicio=inicio,
                termino_previsto=termino_previsto,
                custo_estimado=custo_estimado
            )
            
            sucesso, msg = self.cadastro.adicionar(obra)
            
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
                self.fechar_dialog(e)
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
        except ValueError as ex:
            self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
    
    def atualizar_obra(self, e):
        """Atualiza obra existente"""
        try:
            inicio = datetime.strptime(self.dt_inicio.value, "%d/%m/%Y")
            termino_previsto = datetime.strptime(self.dt_termino_previsto.value, "%d/%m/%Y")
            custo_estimado = float(self.txt_custo_estimado.value.replace(",", "."))
            
            obra_atualizada = Obra(
                nome=self.txt_nome.value,
                inicio=inicio,
                termino_previsto=termino_previsto,
                custo_estimado=custo_estimado,
                termino_real=self.obra_selecionada.termino_real,
                custo_real=self.obra_selecionada.custo_real
            )
            
            sucesso, msg = self.cadastro.atualizar(self.obra_selecionada.id, obra_atualizada)
            
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
                self.fechar_dialog(e)
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
        except ValueError as ex:
            self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
    
    def confirmar_exclusao(self, obra):
        """Confirma exclusão de obra"""
        def excluir(e):
            sucesso, msg = self.cadastro.remover(obra.id)
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
            self.fechar_dialog(e)
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir a obra '{obra.nome}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Excluir", on_click=excluir, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def limpar_formulario(self):
        """Limpa os campos do formulário"""
        self.txt_nome.value = ""
        self.dt_inicio.value = ""
        self.dt_termino_previsto.value = ""
        self.txt_custo_estimado.value = ""
        self.obra_selecionada = None
    
    def fechar_dialog(self, e):
        """Fecha o dialog aberto"""
        if self.dialog_aberto:
            self.dialog_aberto.open = False
            self.page.update()
    
    def mostrar_snackbar(self, mensagem, cor):
        """Mostra mensagem na tela"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE),
            bgcolor=cor,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def atualizar_tabela(self):
        """Atualiza a tabela de obras"""
        if self.app:
            # Recarrega a página inteira incluindo cards de resumo
            self.app.recarregar_pagina_atual()
        else:
            # Fallback: apenas atualiza a tabela
            self.tabela_obras.rows = self.criar_tabela_obras().rows
            self.page.update()
