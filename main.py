import flet as ft

class Cliente:
    def __init__(self, id:int, nome:str, email:str, telefone:str):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

class Quarto:
    def __init__(self, numero:int, tipo:str, preco:float, status_disponibilidade:bool):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.status_disponibilidade = status_disponibilidade  # True se disponível, False se ocupado

class Reserva:
    def __init__(self, id:int, id_cliente:int, numero_quarto:int, data_check_in:str, data_check_out:str, status:str):
        self.id = id
        self.id_cliente = id_cliente
        self.numero_quarto = numero_quarto
        self.data_check_in = data_check_in
        self.data_check_out = data_check_out
        self.status = status  # Ex: "confirmada", "pendente", "cancelada"

class Hotel:
    def __init__(self, nome:str):
        self.nome = nome
        self.lista_clientes = []
        self.lista_quartos = []
        self.historico_reservas = []
        self.id_cliente = 1
        self.id_reserva = 1
    
    # Gestão de Clientes
    def cadastrar_cliente(self, nome, email, telefone):
        cliente = Cliente(self.id_cliente, nome, email, telefone)
        self.lista_clientes.append(cliente)
        self.id_cliente += 1
        return f"Cliente {nome} cadastrado com sucesso!"
    
    def ver_todos_clientes(self):
        return [f"ID: {cliente.id}, Nome: {cliente.nome}, Email: {cliente.email}, Telefone: {cliente.telefone}" for cliente in self.lista_clientes]
    
    def editar_cliente(self, id_cliente, nome=None, email=None, telefone=None):
        for cliente in self.lista_clientes:
            if cliente.id == id_cliente:
                if nome:
                    cliente.nome = nome
                if email:
                    cliente.email = email
                if telefone:
                    cliente.telefone = telefone
                return f"Cliente {id_cliente} editado com sucesso!"
        return "Cliente não encontrado."
    
    def excluir_cliente(self, id_cliente):
        for cliente in self.lista_clientes:
            if cliente.id == id_cliente:
                self.lista_clientes.remove(cliente)
                return f"Cliente {id_cliente} excluído com sucesso!"
        return "Cliente não encontrado."
    
    # Gestão de Quartos
    def cadastrar_quarto(self, numero, tipo, preco):
        quarto = Quarto(numero, tipo, preco, True)  # Novo quarto sempre disponível
        self.lista_quartos.append(quarto)
        return f"Quarto {numero} cadastrado com sucesso!"
    
    def ver_todos_quartos(self):
        return [f"Quarto: {quarto.numero}, Tipo: {quarto.tipo}, Preço: R${quarto.preco}, Disponível: {'Sim' if quarto.status_disponibilidade else 'Não'}" for quarto in self.lista_quartos]
    
    def editar_quarto(self, numero, tipo=None, preco=None):
        for quarto in self.lista_quartos:
            if quarto.numero == numero:
                if tipo:
                    quarto.tipo = tipo
                if preco:
                    quarto.preco = preco
                return f"Quarto {numero} editado com sucesso!"
        return "Quarto não encontrado."
    
    def excluir_quarto(self, numero):
        for quarto in self.lista_quartos:
            if quarto.numero == numero:
                self.lista_quartos.remove(quarto)
                return f"Quarto {numero} excluído com sucesso!"
        return "Quarto não encontrado."
    
    # Gestão de Reservas
    def realizar_reserva(self, id_cliente, numero_quarto, data_check_in, data_check_out):
        for quarto in self.lista_quartos:
            if quarto.numero == numero_quarto:
                if quarto.status_disponibilidade:  # Verifica se o quarto está disponível
                    reserva = Reserva(self.id_reserva, id_cliente, numero_quarto, data_check_in, data_check_out, "confirmada")
                    quarto.status_disponibilidade = False  # Marca o quarto como ocupado
                    self.historico_reservas.append(reserva)
                    self.id_reserva += 1
                    return f"Reserva realizada com sucesso para o quarto {numero_quarto}!"
                else:
                    return "O quarto escolhido já está ocupado."
        return "Quarto inválido ou não encontrado."

    def visualizar_reservas(self):
        return [f"Reserva ID: {reserva.id}, Cliente ID: {reserva.id_cliente}, Quarto: {reserva.numero_quarto}, Check-in: {reserva.data_check_in}, Check-out: {reserva.data_check_out}, Status: {reserva.status}" for reserva in self.historico_reservas]
    
    def cancelar_reserva(self, id_reserva):
        for reserva in self.historico_reservas:
            if reserva.id == id_reserva:  # Corrigido para procurar pelo ID da reserva, e não o ID do cliente
                reserva.status = "cancelada"
                for quarto in self.lista_quartos:
                    if quarto.numero == reserva.numero_quarto:
                        quarto.status_disponibilidade = True  # Marca o quarto como disponível novamente
                        return f"Reserva {id_reserva} cancelada com sucesso!"
        return "Reserva não encontrada."

# Instância do Hotel
hotel1 = Hotel(nome="Hotel's Buteco Parisade")

# Função para exibir a tela inicial
def tela_inicial(page: ft.Page):
    page.add(
        ft.Column(
            [
                ft.Text(f"Bem-vindo ao {hotel1.nome}!", style="headline5"),
                ft.Button("Gerenciar Clientes", on_click=lambda _: tela_clientes(page)),
                ft.Button("Gerenciar Quartos", on_click=lambda _: tela_quartos(page)),
                ft.Button("Gerenciar Reservas", on_click=lambda _: tela_reservas(page)),
            ]
        )
    )

# Função para gerenciar reservas
def tela_reservas(page: ft.Page):
    def voltar_inicial(event):
        page.controls.clear()
        tela_inicial(page)

    # Função para realizar a reserva
    def realizar_reserva_func(event):
        id_cliente = cliente_dropdown.value
        numero_quarto = quarto_dropdown.value
        data_check_in = data_check_in_input.value
        data_check_out = data_check_out_input.value
        mensagem = hotel1.realizar_reserva(id_cliente, numero_quarto, data_check_in, data_check_out)
        page.add(ft.Text(mensagem))
        page.update()

    clientes = [str(cliente.id) + " - " + cliente.nome for cliente in hotel1.lista_clientes]
    quartos = [str(quarto.numero) + " - " + quarto.tipo for quarto in hotel1.lista_quartos if quarto.status_disponibilidade]

    cliente_dropdown = ft.Dropdown(label="Escolha o Cliente", options=[ft.dropdown.Option(cliente) for cliente in clientes])
    quarto_dropdown = ft.Dropdown(label="Escolha o Quarto", options=[ft.dropdown.Option(quarto) for quarto in quartos])
    data_check_in_input = ft.TextField(label="Data de Check-in (dd/mm/aaaa)", input_format="date", autofocus=True)
    data_check_out_input = ft.TextField(label="Data de Check-out (dd/mm/aaaa)", input_format="date")

    data_check_in_input.on_submit = lambda e: data_check_out_input.focus()
    data_check_out_input.on_submit = lambda e: cliente_dropdown.focus()

    page.add(
        ft.Column(
            [
                cliente_dropdown,
                quarto_dropdown,
                data_check_in_input,
                data_check_out_input,
                ft.Button("Confirmar Reserva", on_click=realizar_reserva_func),
                ft.Button("Voltar", on_click=voltar_inicial),
            ]
        )
    )

# Função para gerenciar clientes
def tela_clientes(page: ft.Page):
    def voltar_inicial(event):
        page.controls.clear()
        tela_inicial(page)

    page.add(
        ft.Column(
            [
                ft.Text("Gerenciamento de Clientes", style="headline5"),
                ft.Button("Adicionar Cliente", on_click=lambda _: adicionar_cliente(page)),
                ft.Button("Ver Todos os Clientes", on_click=lambda _: ver_clientes(page)),
                ft.Button("Voltar", on_click=voltar_inicial),
            ]
        )
    )

# Função para adicionar cliente
def adicionar_cliente(page: ft.Page):
    def cadastrar(event):
        nome = nome_input.value
        email = email_input.value
        telefone = telefone_input.value
        mensagem = hotel1.cadastrar_cliente(nome, email, telefone)
        page.add(ft.Text(mensagem))
        page.update()

    nome_input = ft.TextField(label="Nome do Cliente")
    email_input = ft.TextField(label="Email do Cliente")
    telefone_input = ft.TextField(label="Telefone do Cliente")
    
    # Auto-move para o próximo campo ao pressionar Enter
    def on_enter(event, next_field):
        next_field.focus()

    nome_input.on_submit = lambda e: on_enter(e, email_input)
    email_input.on_submit = lambda e: on_enter(e, telefone_input)

    page.add(
        ft.Column(
            [
                nome_input,
                email_input,
                telefone_input,
                ft.Button("Cadastrar", on_click=cadastrar),
            ]
        )
    )

# Função para visualizar todos os clientes
def ver_clientes(page: ft.Page):
    clientes_text = "\n".join(hotel1.ver_todos_clientes())
    page.add(ft.Text(clientes_text))
    page.update()

# Função para gerenciar quartos
def tela_quartos(page: ft.Page):
    def voltar_inicial(event):
        page.controls.clear()
        tela_inicial(page)

    page.add(
        ft.Column(
            [
                ft.Text("Gerenciamento de Quartos", style="headline5"),
                ft.Button("Adicionar Quarto", on_click=lambda _: adicionar_quarto(page)),
                ft.Button("Ver Todos os Quartos", on_click=lambda _: ver_quartos(page)),
                ft.Button("Voltar", on_click=voltar_inicial),
            ]
        )
    )

# Função para adicionar quarto
def adicionar_quarto(page: ft.Page):
    def cadastrar(event):
        numero = numero_input.value
        tipo = tipo_input.value
        preco = preco_input.value
        mensagem = hotel1.cadastrar_quarto(numero, tipo, preco)
        page.add(ft.Text(mensagem))
        page.update()

    numero_input = ft.TextField(label="Número do Quarto")
    tipo_input = ft.TextField(label="Tipo do Quarto")
    preco_input = ft.TextField(label="Preço do Quarto")
    
    page.add(
        ft.Column(
            [
                numero_input,
                tipo_input,
                preco_input,
                ft.Button("Cadastrar", on_click=cadastrar),
            ]
        )
    )

# Função para visualizar todos os quartos
def ver_quartos(page: ft.Page):
    quartos_text = "\n".join(hotel1.ver_todos_quartos())
    page.add(ft.Text(quartos_text))
    page.update()

# Função para executar o app
def main(page: ft.Page):
    page.title = "Hotel's Buteco Parisade"
    tela_inicial(page)

# Executar o app
ft.app(target=main)
