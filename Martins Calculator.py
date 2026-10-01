import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle


# ==========================================
# CÓDIGO BASE DA CALCULADORA
# ==========================================

def calcular(numero1, operacao, numero2):

    if operacao == "+":
        return numero1 + numero2

    elif operacao == "-":
        return numero1 - numero2

    elif operacao == "*":
        return numero1 * numero2

    elif operacao == "/":

        if numero2 == 0:
            return "Não é possível dividir por zero."

        return numero1 / numero2

    else:
        return "Operação inválida."


# ==========================================
# FUNDO DA FAIXA CINZENTA
# ==========================================

class FundoCinza(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.65, 0.65, 0.65, 1)
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

    def atualizar_fundo(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# ==========================================
# TELA MC
# ==========================================

class SplashScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(
            self.abrir_calculadora,
            3
        )

    def abrir_calculadora(self, tempo):
        self.manager.current = "calculadora"


# ==========================================
# TELA DA CALCULADORA
# ==========================================

class CalculatorScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.numero1 = None
        self.operacao = None

        layout_principal = BoxLayout(
            orientation="vertical"
        )

        # ==================================
        # FAIXA SUPERIOR
        # ==================================

        faixa = FundoCinza(
            orientation="vertical",
            size_hint_y=0.12
        )

        titulo = Label(
            text="MARTINS CALCULATOR",
            color=(0, 0, 0, 1),
            font_size="20sp"
        )

        faixa.add_widget(titulo)

        layout_principal.add_widget(faixa)

        # ==================================
        # VISOR
        # ==================================

        self.display = Label(
            text="0",
            font_size="35sp",
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            size_hint_y=0.23
        )

        layout_principal.add_widget(
            self.display
        )

        # ==================================
        # BOTÕES
        # ==================================

        teclado = GridLayout(
            cols=4,
            spacing=5,
            padding=5
        )

        botoes = [
            ("7", "numero"),
            ("8", "numero"),
            ("9", "numero"),
            ("÷", "operacao"),

            ("4", "numero"),
            ("5", "numero"),
            ("6", "numero"),
            ("×", "operacao"),

            ("1", "numero"),
            ("2", "numero"),
            ("3", "numero"),
            ("-", "operacao"),

            ("C", "operacao"),
            ("0", "numero"),
            ("=", "operacao"),
            ("+", "operacao")
        ]

        for texto, tipo in botoes:

            botao = Button(
                text=texto,
                font_size="25sp"
            )

            botao.background_normal = ""

            if tipo == "numero":

                # BOTÕES DOS NÚMEROS = LARANJA
                botao.background_color = (
                    1, 0.55, 0, 1
                )

                botao.color = (
                    0, 0, 0, 1
                )

            else:

                # BOTÕES DOS SINAIS = CINZENTO
                botao.background_color = (
                    0.55, 0.55, 0.55, 1
                )

                botao.color = (
                    0, 0, 0, 1
                )

            botao.bind(
                on_press=self.botao_pressionado
            )

            teclado.add_widget(botao)

        layout_principal.add_widget(
            teclado
        )

        self.add_widget(
            layout_principal
        )

    # ==================================
    # CONTROLO DOS BOTÕES
    # ==================================

    def botao_pressionado(self, botao):

        valor = botao.text

        # NÚMEROS
        if valor.isdigit():

            if self.display.text == "0":
                self.display.text = valor

            else:
                self.display.text += valor

        # LIMPAR
        elif valor == "C":

            self.display.text = "0"
            self.numero1 = None
            self.operacao = None

        # OPERAÇÃO
        elif valor in ["+", "-", "×", "÷"]:

            self.numero1 = float(
                self.display.text
            )

            self.operacao = valor

            self.display.text = "0"

        # RESULTADO
        elif valor == "=":

            if self.numero1 is not None:

                numero2 = float(
                    self.display.text
                )

                # Adaptar os símbolos da interface
                # para o código-base

                if self.operacao == "×":
                    operacao_base = "*"

                elif self.operacao == "÷":
                    operacao_base = "/"

                else:
                    operacao_base = self.operacao

                # USAR O CÓDIGO BASE
                resultado = calcular(
                    self.numero1,
                    operacao_base,
                    numero2
                )

                self.display.text = str(
                    resultado
                )

                self.numero1 = None
                self.operacao = None


# ==========================================
# APLICAÇÃO
# ==========================================

class MartinsCalculator(App):

    def build(self):

        gerenciador = ScreenManager()

        # Tela inicial MC
        splash = SplashScreen(
            name="splash"
        )

        mc = Label(
            text="MC",
            font_size="70sp",
            color=(1, 0.55, 0, 1)
        )

        splash.add_widget(mc)

        # Tela principal
        calculadora = CalculatorScreen(
            name="calculadora"
        )

        gerenciador.add_widget(splash)
        gerenciador.add_widget(calculadora)

        return gerenciador


# ==========================================
# INICIAR APP
# ==========================================

MartinsCalculator().run()