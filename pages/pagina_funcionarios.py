"""
Página de Gerenciamento de Funcionários
"""
import flet as ft
from datetime import datetime
from cadastro_funcionario.funcionario import Funcionario


class PaginaFuncionarios:
    def __init__(self, page: ft.Page, cadastro_funcionario, app=None):
        self.page = page
        self.cadastro = cadastro_funcionario
        self.app = app
        self.dialog_aberto = None
        self.funcionario_selecionado = None
        
        # Campos do formulário
        self.txt_nome = ft.TextField(label="Nome Completo", width=400)
        self.txt_cpf = ft.TextField(label="CPF", width=200, max_length=14)
        self.txt_cargo = ft.TextField(label="Cargo", width=250)
        self.txt_salario = ft.TextField(label="Salário (R$)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        self.dt_admissao = ft.TextField(label="Data de Admissão (DD/MM/AAAA)", width=200)
    
    def criar_pagina(self):
        """Cria a página principal de funcionários"""
        self.tabela_funcionarios = self.criar_tabela_funcionarios()
        
        funcionarios_ativos = self.cadastro.listar(apenas_ativos=True)
        folha_total = self.cadastro.folha_pagamento(True)
        
        return ft.Column(
            [
                # Cabeçalho
                ft.Row(
                    [
                        ft.Text("👷 Gerenciamento de Funcionários", size=32, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "➕ Novo Funcionário",
                            on_click=self.abrir_dialog_cadastro,
                            bgcolor=ft.Colors.ORANGE_700,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),
                ft.Divider(height=20),
                
                # Cards de resumo
                ft.Row(
                    [
                        self.criar_card_resumo(
                            "Funcionários Ativos",
                            str(len(funcionarios_ativos)),
                            ft.Icons.PEOPLE,
                            ft.Colors.ORANGE_400,
                        ),
                        self.criar_card_resumo(
                            "Folha de Pagamento",
                            f"R$ {folha_total:,.2f}",
                            ft.Icons.ATTACH_MONEY,
                            ft.Colors.GREEN_400,
                        ),
                        self.criar_card_resumo(
                            "Salário Médio",
                            f"R$ {(folha_total / len(funcionarios_ativos) if funcionarios_ativos else 0):,.2f}",
                            ft.Icons.TRENDING_UP,
                            ft.Colors.BLUE_400,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(height=20),
                
                # Tabela
                ft.Container(
                    content=self.tabela_funcionarios,
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
                            ft.Text(valor, size=22, weight=ft.FontWeight.BOLD, color=cor),
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
            width=280,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
        )
    
    def criar_tabela_funcionarios(self):
        """Cria a tabela de funcionários"""
        funcionarios = self.cadastro.listar()
        
        linhas = []
        for func in funcionarios:
            status_cor = ft.Colors.GREEN_600 if func.esta_ativo() else ft.Colors.RED_600
            status_texto = "Ativo" if func.esta_ativo() else "Demitido"
            
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(func.id))),
                        ft.DataCell(ft.Text(func.nome)),
                        ft.DataCell(ft.Text(func.formatar_cpf())),
                        ft.DataCell(ft.Text(func.cargo)),
                        ft.DataCell(ft.Text(f"R$ {func.salario:,.2f}")),
                        ft.DataCell(ft.Text(func.data_admissao.strftime("%d/%m/%Y"))),
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
                                        on_click=lambda e, f=func: self.abrir_dialog_edicao(f),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.PERSON_OFF,
                                        icon_color=ft.Colors.ORANGE_700,
                                        tooltip="Demitir",
                                        on_click=lambda e, f=func: self.abrir_dialog_demitir(f),
                                        disabled=not func.esta_ativo(),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED_700,
                                        tooltip="Excluir",
                                        on_click=lambda e, f=func: self.confirmar_exclusao(f),
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
                ft.DataColumn(ft.Text("CPF", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cargo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Salário", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Admissão", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=linhas,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
        )
    
    def abrir_dialog_cadastro(self, e):
        """Abre dialog para cadastrar novo funcionário"""
        self.limpar_formulario()
        
        dialog = ft.AlertDialog(
            title=ft.Text("➕ Cadastrar Novo Funcionário"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.txt_nome,
                        ft.Row([self.txt_cpf, self.txt_cargo]),
                        ft.Row([self.txt_salario, self.dt_admissao]),
                        ft.Text("Dica: CPF será validado automaticamente", size=12, color=ft.Colors.GREY_600),
                    ],
                    tight=True,
                ),
                width=600,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Salvar", on_click=self.salvar_funcionario, bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def abrir_dialog_edicao(self, funcionario):
        """Abre dialog para editar funcionário"""
        self.funcionario_selecionado = funcionario
        self.txt_nome.value = funcionario.nome
        self.txt_cpf.value = funcionario.cpf
        self.txt_cargo.value = funcionario.cargo
        self.txt_salario.value = str(funcionario.salario)
        self.dt_admissao.value = funcionario.data_admissao.strftime("%d/%m/%Y")
        
        dialog = ft.AlertDialog(
            title=ft.Text("✏️ Editar Funcionário"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.txt_nome,
                        ft.Row([self.txt_cpf, self.txt_cargo]),
                        ft.Row([self.txt_salario, self.dt_admissao]),
                    ],
                    tight=True,
                ),
                width=600,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Atualizar", on_click=self.atualizar_funcionario, bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def abrir_dialog_demitir(self, funcionario):
        """Abre dialog para demitir funcionário"""
        self.funcionario_selecionado = funcionario
        
        dt_demissao = ft.TextField(label="Data de Demissão (DD/MM/AAAA)", width=200)
        
        def demitir(e):
            try:
                data_demissao = datetime.strptime(dt_demissao.value, "%d/%m/%Y")
                sucesso, msg = self.cadastro.demitir(funcionario.id, data_demissao)
                
                if sucesso:
                    self.mostrar_snackbar(msg, ft.Colors.ORANGE_700)
                    self.atualizar_tabela()
                else:
                    self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
                self.fechar_dialog(e)
            except ValueError as ex:
                self.mostrar_snackbar(f"Data inválida", ft.Colors.RED_700)
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Demitir Funcionário"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Funcionário: {funcionario.nome}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"Cargo: {funcionario.cargo}"),
                        ft.Text(f"Tempo de empresa: {funcionario.tempo_empresa()} dias"),
                        ft.Container(height=10),
                        dt_demissao,
                    ],
                    tight=True,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Confirmar Demissão", on_click=demitir, bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def salvar_funcionario(self, e):
        """Salva novo funcionário"""
        try:
            data_admissao = datetime.strptime(self.dt_admissao.value, "%d/%m/%Y")
            salario = float(self.txt_salario.value.replace(",", "."))
            
            funcionario = Funcionario(
                nome=self.txt_nome.value,
                cpf=self.txt_cpf.value,
                cargo=self.txt_cargo.value,
                salario=salario,
                data_admissao=data_admissao
            )
            
            sucesso, msg = self.cadastro.adicionar(funcionario)
            
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
                self.fechar_dialog(e)
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
        except ValueError as ex:
            self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
    
    def atualizar_funcionario(self, e):
        """Atualiza funcionário existente"""
        try:
            data_admissao = datetime.strptime(self.dt_admissao.value, "%d/%m/%Y")
            salario = float(self.txt_salario.value.replace(",", "."))
            
            funcionario_atualizado = Funcionario(
                nome=self.txt_nome.value,
                cpf=self.txt_cpf.value,
                cargo=self.txt_cargo.value,
                salario=salario,
                data_admissao=data_admissao,
                data_demissao=self.funcionario_selecionado.data_demissao
            )
            
            sucesso, msg = self.cadastro.atualizar(self.funcionario_selecionado.id, funcionario_atualizado)
            
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
                self.fechar_dialog(e)
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
        except ValueError as ex:
            self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
    
    def confirmar_exclusao(self, funcionario):
        """Confirma exclusão de funcionário"""
        def excluir(e):
            sucesso, msg = self.cadastro.remover(funcionario.id)
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
            self.fechar_dialog(e)
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir o funcionário '{funcionario.nome}'?"),
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
        self.txt_cpf.value = ""
        self.txt_cargo.value = ""
        self.txt_salario.value = ""
        self.dt_admissao.value = ""
        self.funcionario_selecionado = None
    
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
        """Atualiza a tabela de funcionários"""
        if self.app:
            # Recarrega a página inteira incluindo cards de resumo
            self.app.recarregar_pagina_atual()
        else:
            # Fallback: apenas atualiza a tabela
            self.tabela_funcionarios.rows = self.criar_tabela_funcionarios().rows
            self.page.update()
