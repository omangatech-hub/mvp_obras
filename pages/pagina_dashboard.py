"""
Página de Dashboard - Visão Geral do Sistema
"""
import flet as ft
from datetime import datetime


class PaginaDashboard:
    def __init__(self, page: ft.Page, cadastro_obra, cadastro_insumo, cadastro_funcionario):
        self.page = page
        self.cadastro_obra = cadastro_obra
        self.cadastro_insumo = cadastro_insumo
        self.cadastro_funcionario = cadastro_funcionario
    
    def criar_pagina(self):
        """Cria a página de dashboard"""
        return ft.Column(
            [
                # Cabeçalho
                ft.Row(
                    [
                        ft.Text("📊 Dashboard - Visão Geral", size=32, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.Text(
                            datetime.now().strftime("%d/%m/%Y %H:%M"),
                            size=16,
                            color=ft.Colors.GREY_600,
                        ),
                    ],
                ),
                ft.Divider(height=20),
                
                # Cards principais
                ft.Row(
                    [
                        self.criar_card_metrica(
                            "Obras Ativas",
                            str(len([o for o in self.cadastro_obra.listar() if not o.termino_real])),
                            ft.Icons.CONSTRUCTION,
                            ft.Colors.BLUE_400,
                        ),
                        self.criar_card_metrica(
                            "Funcionários Ativos",
                            str(len(self.cadastro_funcionario.listar(apenas_ativos=True))),
                            ft.Icons.PEOPLE,
                            ft.Colors.ORANGE_400,
                        ),
                        self.criar_card_metrica(
                            "Insumos Cadastrados",
                            str(len(self.cadastro_insumo.listar())),
                            ft.Icons.INVENTORY_2,
                            ft.Colors.PURPLE_400,
                        ),
                        self.criar_card_metrica(
                            "Estoque Baixo",
                            str(len([i for i in self.cadastro_insumo.listar() if i.quantidade_estoque < 10])),
                            ft.Icons.WARNING,
                            ft.Colors.RED_400,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(height=20),
                
                # Análise Financeira
                ft.Row(
                    [
                        self.criar_analise_obras(),
                        ft.Container(width=20),
                        self.criar_analise_custos(),
                    ],
                    expand=True,
                ),
                ft.Container(height=20),
                
                # Análise de RH e Estoque
                ft.Row(
                    [
                        self.criar_analise_rh(),
                        ft.Container(width=20),
                        self.criar_analise_estoque(),
                    ],
                    expand=True,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def criar_card_metrica(self, titulo, valor, icone, cor):
        """Cria card de métrica"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icone, size=50, color=cor),
                    ft.Text(valor, size=32, weight=ft.FontWeight.BOLD, color=cor),
                    ft.Text(titulo, size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            width=220,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        )
    
    def criar_analise_obras(self):
        """Cria análise de obras"""
        obras = self.cadastro_obra.listar()
        em_andamento = [o for o in obras if not o.termino_real]
        finalizadas = [o for o in obras if o.termino_real]
        
        # Calcular atrasos
        obras_atrasadas = 0
        dias_atraso_total = 0
        for obra in em_andamento:
            if obra.termino_previsto < datetime.now().date():
                obras_atrasadas += 1
                dias_atraso = (datetime.now().date() - obra.termino_previsto).days
                dias_atraso_total += dias_atraso
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("🏗️ Análise de Obras", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Total de obras:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(obras)), size=14, weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Row([
                        ft.Text("Em andamento:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(em_andamento)), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ]),
                    
                    ft.Row([
                        ft.Text("Finalizadas:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(finalizadas)), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ]),
                    
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Obras atrasadas:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(obras_atrasadas), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                    ]),
                    
                    ft.Row([
                        ft.Text("Média de atraso:", size=14),
                        ft.Container(expand=True),
                        ft.Text(
                            f"{dias_atraso_total / obras_atrasadas if obras_atrasadas > 0 else 0:.0f} dias",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ORANGE_700,
                        ),
                    ]),
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        )
    
    def criar_analise_custos(self):
        """Cria análise de custos"""
        obras = self.cadastro_obra.listar()
        
        custo_estimado_total = sum(o.custo_estimado for o in obras)
        custo_real_total = sum(o.custo_real for o in obras if o.custo_real)
        obras_finalizadas = [o for o in obras if o.termino_real and o.custo_real]
        
        economia_total = 0
        estouro_total = 0
        for obra in obras_finalizadas:
            diferenca = obra.custo_estimado - obra.custo_real
            if diferenca > 0:
                economia_total += diferenca
            else:
                estouro_total += abs(diferenca)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("💰 Análise de Custos", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Custo estimado total:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {custo_estimado_total:,.2f}", size=14, weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Row([
                        ft.Text("Custo real total:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {custo_real_total:,.2f}", size=14, weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Economia total:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {economia_total:,.2f}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ]),
                    
                    ft.Row([
                        ft.Text("Estouro total:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {estouro_total:,.2f}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                    ]),
                    
                    ft.Row([
                        ft.Text("Taxa de precisão:", size=14),
                        ft.Container(expand=True),
                        ft.Text(
                            f"{(1 - (estouro_total / custo_estimado_total if custo_estimado_total > 0 else 0)) * 100:.1f}%",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ]),
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        )
    
    def criar_analise_rh(self):
        """Cria análise de RH"""
        funcionarios = self.cadastro_funcionario.listar()
        ativos = self.cadastro_funcionario.listar(apenas_ativos=True)
        demitidos = [f for f in funcionarios if not f.esta_ativo()]
        
        folha_total = self.cadastro_funcionario.folha_pagamento(True)
        salario_medio = folha_total / len(ativos) if ativos else 0
        
        # Agrupar por cargo
        cargos = {}
        for func in ativos:
            if func.cargo not in cargos:
                cargos[func.cargo] = 0
            cargos[func.cargo] += 1
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("👥 Análise de RH", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Funcionários ativos:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(ativos)), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ]),
                    
                    ft.Row([
                        ft.Text("Funcionários demitidos:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(demitidos)), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                    ]),
                    
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Folha de pagamento:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {folha_total:,.2f}", size=14, weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Row([
                        ft.Text("Salário médio:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {salario_medio:,.2f}", size=14, weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Divider(height=10),
                    
                    ft.Text("Distribuição por cargo:", size=14, weight=ft.FontWeight.BOLD),
                    ft.Column(
                        [
                            ft.Row([
                                ft.Text(f"• {cargo}:", size=12),
                                ft.Container(expand=True),
                                ft.Text(str(qtd), size=12, weight=ft.FontWeight.BOLD),
                            ])
                            for cargo, qtd in sorted(cargos.items(), key=lambda x: x[1], reverse=True)[:5]
                        ],
                        spacing=4,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        )
    
    def criar_analise_estoque(self):
        """Cria análise de estoque"""
        insumos = self.cadastro_insumo.listar()
        
        valor_total = sum(i.calcular_valor_estoque() for i in insumos)
        estoque_baixo = [i for i in insumos if i.quantidade_estoque < 10]
        sem_estoque = [i for i in insumos if i.quantidade_estoque == 0]
        
        # Insumos mais valiosos
        top_valiosos = sorted(insumos, key=lambda x: x.calcular_valor_estoque(), reverse=True)[:5]
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("📦 Análise de Estoque", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Total de insumos:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(insumos)), size=14, weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Row([
                        ft.Text("Valor em estoque:", size=14),
                        ft.Container(expand=True),
                        ft.Text(f"R$ {valor_total:,.2f}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ]),
                    
                    ft.Divider(height=10),
                    
                    ft.Row([
                        ft.Text("Estoque baixo:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(estoque_baixo)), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                    ]),
                    
                    ft.Row([
                        ft.Text("Sem estoque:", size=14),
                        ft.Container(expand=True),
                        ft.Text(str(len(sem_estoque)), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                    ]),
                    
                    ft.Divider(height=10),
                    
                    ft.Text("Top 5 mais valiosos:", size=14, weight=ft.FontWeight.BOLD),
                    ft.Column(
                        [
                            ft.Row([
                                ft.Text(f"• {i.nome}:", size=12),
                                ft.Container(expand=True),
                                ft.Text(f"R$ {i.calcular_valor_estoque():,.2f}", size=12, weight=ft.FontWeight.BOLD),
                            ])
                            for i in top_valiosos
                        ],
                        spacing=4,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        )
