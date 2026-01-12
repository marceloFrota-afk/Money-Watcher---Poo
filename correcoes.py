# ==============================================================================
# IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
# ABC = Abstract Base Class (Classe Base Abstrata)
# abstractmethod = Decorador que obriga as subclasses a implementarem o método.
# Conceito: Classes Abstratas (Slides Parte 4 e 5)
from abc import ABC, abstractmethod


# ==============================================================================
# FUNÇÕES AUXILIARES (PROCEDURAL)
# ==============================================================================
# Estas funções não são POO pura, são utilitários para validação de entrada.
# Ajudam a manter o código principal limpo e evitam erros (Exceptions).

def input_int(msg, minimo=1):
    """Garante que o usuário digite um número inteiro válido."""
    while True:
        try:
            v = int(input(msg))
            if v < minimo:
                raise ValueError
            return v
        except ValueError:
            print("ERRO: Digite um valor inteiro válido.")

def input_float(msg, minimo=0):
    """Garante que o usuário digite um número decimal válido."""
    while True:
        try:
            v = float(input(msg))
            if v < minimo:
                raise ValueError
            return v
        except ValueError:
            print("ERRO: Digite um valor numérico válido.")

def input_opcao(msg, opcoes):
    """Valida se a entrada está dentro de uma lista de opções permitidas."""
    while True:
        v = input(msg)
        if v in opcoes:
            return v
        print("Opção inválida.")


# ==============================================================================
# [CONCEITO POO]: CLASSES ABSTRATAS & SOBRECARGA
# ==============================================================================

# A classe Gasto herda de ABC.
# Isso a torna um "Molde Incompleto". Não é possível fazer: g = Gasto().
# Serve para padronizar os gastos essenciais e não essenciais.
class Gasto(ABC):

    # O Construtor (__init__) define os atributos que TODO gasto tem.
    def __init__(self, valor, dia, categoria):
        self.valor = valor
        self.dia = dia
        self.categoria = categoria

    # [CONCEITO: SOBRECARGA DE OPERADORES - Slides Parte 3]
    # O método __lt__ (Less Than / Menor Que) ensina o Python a comparar dois gastos.
    # Isso permite ordenar a lista de gastos automaticamente com .sort().
    def __lt__(self, outro_gasto):
        return self.valor < outro_gasto.valor

    # [CONCEITO: MÉTODO ABSTRATO - O CONTRATO]
    # Define que todo gasto PRECISA ter esse método, mas não diz como ele funciona.
    # As classes filhas são OBRIGADAS a escrever o código deste método.
    @abstractmethod
    def eh_essencial(self):
        pass


# ==============================================================================
# [CONCEITO POO]: HERANÇA & POLIMORFISMO
# ==============================================================================

# GastoEssencial "é um" Gasto (Herança).
# Ele herda valor, dia e categoria automaticamente.
class GastoEssencial(Gasto):
    
    # [CONCEITO: POLIMORFISMO / SOBRESCRITA]
    # Implementamos o método abstrato de forma específica para esta classe.
    def eh_essencial(self):
        return True

class GastoNaoEssencial(Gasto):
    
    # [CONCEITO: POLIMORFISMO]
    # Aqui, o mesmo método retorna False. O sistema saberá qual usar.
    def eh_essencial(self):
        return False


# ==============================================================================
# [CONCEITO POO]: ENCAPSULAMENTO
# ==============================================================================

class Usuario:
    def __init__(self):
        # Atributos do objeto (Estado)
        self.salario = 0
        self.gastos = []    # Composição: Usuário tem uma lista de Gastos
        self.caixinha = 0   

    # [CONCEITO: ENCAPSULAMENTO]
    # Escondemos a lógica complexa: somar a caixinha antiga ao novo salário
    # e zerar a caixinha. O mundo externo apenas chama "definir_salario".
    def definir_salario(self, valor):
        self.salario = valor + self.caixinha
        self.caixinha = 0

    # Método tradicional para adicionar gasto
    def adicionar_gasto(self, gasto):
        self.gastos.append(gasto)

    # [CONCEITO: SOBRECARGA DE OPERADORES - Slides Parte 3]
    # O método __iadd__ permite usar o operador "+=" no objeto.
    # Ex: usuario += gasto (Açúcar Sintático para facilitar a leitura)
    def __iadd__(self, gasto):
        self.adicionar_gasto(gasto)
        return self

    def total_gastos(self):
        # Itera sobre a lista de objetos e soma seus atributos .valor
        return sum(g.valor for g in self.gastos)

    # [CONCEITO: ENCAPSULAMENTO]
    # O cálculo do saldo é protegido aqui. Se a regra mudar, mudamos só aqui.
    def saldo(self):
        return self.salario - self.total_gastos()

    def limpar_gastos(self):
        self.gastos.clear()


# ==============================================================================
# CLASSE DE CONTROLE
# ==============================================================================

class CicloFinanceiro:
    def __init__(self, duracao):
        self.duracao = duracao
        self.dia_atual = 1

    # [CONCEITO: ENCAPSULAMENTO]
    # Protege a variável dia_atual de ser alterada incorretamente.
    def avancar_dia(self):
        self.dia_atual += 1

    def acabou(self):
        return self.dia_atual > self.duracao

    def reiniciar(self):
        self.dia_atual = 1


# ==============================================================================
# CLASSE ORGANIZADORA (ASSOCIAÇÃO/COMPOSIÇÃO)
# ==============================================================================

class OrganizadorFinanceiro:
    CATEGORIAS = ["Alimentação", "Transporte", "Saúde", "Lazer", "Contas", "Casa"]

    def __init__(self, usuario, ciclo):
        # Associação: O Organizador "coordena" o Usuário e o Ciclo.
        self.usuario = usuario
        self.ciclo = ciclo

    def menu_operacao(self):
        print(f"\nDia {self.ciclo.dia_atual}")
        print("1 - Adicionar gasto")
        print("2 - Ver saldo")
        print("3 - Encerrar dia")

    def adicionar_gasto(self):
        print("\nCategoria:")
        for i, c in enumerate(self.CATEGORIAS, 1):
            print(f"{i} - {c}")
        
        # Seleção de dados (Procedural)
        cat = self.CATEGORIAS[input_int("Escolha: ", 1) - 1]
        tipo = input_opcao("Essencial (e) ou Não Essencial (n): ", ["e", "n"])
        valor = input_float("Valor do gasto: R$ ", 0.01)

        # Verificação de aviso (Lógica de negócio)
        saldo_atual = self.usuario.saldo()
        if valor > saldo_atual:
            print(f"AVISO: Dívida gerada de R$ {valor - saldo_atual:.2f}")

        # [POLIMORFISMO NA CRIAÇÃO]
        # Dependendo do input, instanciamos classes diferentes.
        # Mas ambas são tratadas como 'gasto' pelo sistema.
        if tipo == "e":
            gasto = GastoEssencial(valor, self.ciclo.dia_atual, cat)
        else:
            gasto = GastoNaoEssencial(valor, self.ciclo.dia_atual, cat)
        
        # [USO DA SOBRECARGA DE OPERADOR]
        # Aqui usamos o += definido no método __iadd__ da classe Usuario
        self.usuario += gasto 

    def executar(self):
        while not self.ciclo.acabou():
            self.menu_operacao()
            op = input_opcao("Opção: ", ["1", "2", "3"])

            if op == "1":
                self.adicionar_gasto()
            elif op == "2":
                print(f"Saldo atual: R$ {self.usuario.saldo():.2f}")
            else:
                self.ciclo.avancar_dia()

        self.relatorio_final()

    def relatorio_final(self):
        print("\n===== RELATÓRIO FINAL =====")

        # [USO DA SOBRECARGA DE OPERADOR]
        # Ordena a lista do maior valor para o menor.
        # Funciona graças ao método __lt__ na classe Gasto.
        self.usuario.gastos.sort(reverse=True)

        total = self.usuario.total_gastos()
        if total == 0:
            print("Nenhum gasto registrado.")
            return
        
        # [POLIMORFISMO NA LEITURA]
        # O loop chama .eh_essencial() para cada item.
        # Cada objeto responde True ou False conforme sua própria classe.
        ess_total = sum(g.valor for g in self.usuario.gastos if g.eh_essencial())
        nao_total = total - ess_total

        print(f"\nTotal gasto no ciclo: R$ {total:.2f}")
        print(f"Gastos Essenciais: R$ {ess_total:.2f} ({ess_total / total * 100:.1f}%)")
        print(f"Gastos Não Essenciais: R$ {nao_total:.2f} ({nao_total / total * 100:.1f}%)")

        print("\n--- Detalhes por Categoria (Ordenado por Valor) ---")
        for cat in self.CATEGORIAS:
            # List Comprehension para filtrar gastos da categoria atual
            gastos_cat = [g for g in self.usuario.gastos if g.categoria == cat]
            if not gastos_cat:
                continue

            total_cat = sum(g.valor for g in gastos_cat)
            print(f"{cat}: R$ {total_cat:.2f}")

        saldo = self.usuario.saldo()
        print(f"\nSaldo final: R$ {saldo:.2f}")

        # Lógica da Caixinha
        if saldo > 0:
            self.usuario.caixinha += saldo
            print(f"Guardado na caixinha: R$ {self.usuario.caixinha:.2f}")


# ==============================================================================
# MAIN (EXECUÇÃO PRINCIPAL)
# ==============================================================================

def menu_inicial():
    print("\n===== MONEY WATCHER =====")
    print("1 - Iniciar ciclo")
    print("2 - Sair")
    return input_opcao("Opção: ", ["1", "2"])

def main():
    # Instanciação do objeto principal (O Usuário persiste entre os ciclos)
    usuario = Usuario()

    while True:
        # Loop do Menu Principal (Nível 1)
        if menu_inicial() == "2":
            break

        duracao = input_int("Duração do ciclo (dias): ")
        salario = input_float("Salário (inteiro): R$ ", 0)

        # Instanciação dos objetos da rodada
        ciclo = CicloFinanceiro(duracao)
        app = OrganizadorFinanceiro(usuario, ciclo)

        # Loop de Controle do Ciclo (Nível 2)
        # Permite recomeçar o mês quantas vezes quiser
        while True:
            # 1. Limpa os gastos da tentativa anterior (Encapsulamento)
            usuario.limpar_gastos()
            # 2. Reseta o dia para 1
            ciclo.reiniciar()
            # 3. Recalcula salário somando caixinha acumulada
            usuario.definir_salario(salario)
            
            # Executa o programa
            app.executar()

            print("\n1 - Alterar informações do ciclo (voltar ao menu)")
            print("2 - Recomeçar ciclo (manter caixinha, zerar gastos)")
            print("3 - Sair totalmente")

            fim = input_opcao("Opção: ", ["1", "2", "3"])
            
            if fim == "1":
                break # Sai deste loop e pede duração/salário de novo
            elif fim == "2":
                continue # Volta para o topo do 'while True' interno
            else:
                return # Encerra o programa inteiro

if __name__ == "__main__":
    main()