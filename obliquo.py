from manim import *
import json

class MovimentoObliquo(Scene):
    def construct(self):
        

        # Lê os parâmetros do arquivo
        with open("parametros.json", "r") as f:
            params = json.load(f)


        # Eixos cartesianos
        plano = Axes(
            x_range=[0, 30, 2],
            y_range=[0, 20, 2],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)
        label_x = MathTex("x\\ (m)").next_to(plano.x_axis, RIGHT).shift(DOWN * 0.5)
        label_y = MathTex("y\\ (m)").next_to(plano.y_axis, UP).shift(LEFT * 0.5)
        
        # Parâmetros do movimento
        v0 = float(params["velocidade_inicial"])
        ang = float(params["angulo"])
        theta = ang * DEGREES
        g = 9.8

        traj = lambda t: [
            v0 * np.cos(theta) * t,
            v0 * np.sin(theta) * t - 0.5 * g * t**2,
            0
        ]

        # Cálculo da altura máxima (velocidade vertical = 0)
        t_max = v0 * np.sin(theta) / g
        y_max = v0 * np.sin(theta) * t_max - 0.5 * g * t_max**2

        # Linha assintótica na altura máxima
        linha = DashedLine(
            start=plano.c2p(0, y_max),
            end=plano.c2p(30, y_max),
            color=RED
        )


        self.play(Create(plano))
        self.play(Write(label_x), Write(label_y))
     

        # Tempo total e pontos
        t_total = 2 * v0 * np.sin(theta) / g
        n_pontos = 100
        tempos = np.linspace(0, t_total, n_pontos)
        pontos = [plano.c2p(*traj(t)) for t in tempos]

        # Criação da bolinha com always_redraw (ligada ao ValueTracker)
        tempo = ValueTracker(0)
        bola = always_redraw(lambda: Dot(color=YELLOW).move_to(
            plano.c2p(*traj(tempo.get_value()))
        ))

        # Vetor horizontal que segue a bola
        vetor_x = always_redraw(lambda: Arrow(
            start=plano.c2p(*traj(tempo.get_value())),
            end=plano.c2p(*traj(tempo.get_value())) + RIGHT * 0.7,
            buff=0,
            color=BLUE,
            stroke_width=4,
        max_tip_length_to_length_ratio=0.2
        ))
        self.add(vetor_x)

        label_vx = always_redraw(lambda: MathTex(r"\vec{v}_x", color=BLUE).next_to(vetor_x.get_end(), RIGHT, buff=0.1))
        self.add(label_vx)

        # Função da velocidade vertical
        v_y = lambda t: v0 * np.sin(theta) - g * t

        # Vetor vertical que muda com o tempo
        vetor_y = always_redraw(lambda: Arrow(
            start=plano.c2p(*traj(tempo.get_value())),
            end=plano.c2p(*traj(tempo.get_value())) + UP * np.sign(v_y(tempo.get_value())) * abs(v_y(tempo.get_value())) * 0.05,
            buff=0,
            color=GREEN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2
        ))
        self.add(vetor_y)

        label_vy = always_redraw(lambda: MathTex(r"\vec{v}_y", color=GREEN).next_to(vetor_y.get_end(), UP if v_y(tempo.get_value()) > 0 else DOWN, buff=0.1))
        self.add(label_vy)
        self.add(bola)
        self.play(Create(linha))

        # Criar linha pontilhada manualmente em tempo real
        linhas = VGroup()
        for i in range(0, n_pontos - 1, 2):  # pula um sim, outro não (pontilhado)
            linha = always_redraw(lambda i=i: Line(
                pontos[i], pontos[i + 1], color=YELLOW, stroke_width=2
            ).set_opacity(1 if tempo.get_value() >= tempos[i+1] else 0))
            linhas.add(linha)

        self.add(linhas)
        

        # Anima o tempo — bolinha e linhas acompanham
        self.play(tempo.animate.set_value(t_total), run_time=3, rate_func=linear)
  

        self.wait(2)
