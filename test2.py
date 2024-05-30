from manim import *

class TrigCircle(Scene):
    def construct(self):
        # Desenhando o círculo trigonométrico
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        
        # Adicionando os eixos
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY}
        )
        self.play(Create(axes))
        
        # Adicionando o ponto móvel no círculo
        moving_dot = Dot(color=RED)
        moving_dot.move_to(axes.c2p(2, 0))
        self.play(FadeIn(moving_dot))
        
        # Adicionando o ângulo em radianos
        angle = ValueTracker(0)
        arc = always_redraw(lambda: Arc(
            radius=0.5, 
            start_angle=0, 
            angle=angle.get_value(), 
            color=YELLOW
        ))
        moving_dot.add_updater(lambda d: d.move_to(
            axes.c2p(2 * np.cos(angle.get_value()), 2 * np.sin(angle.get_value()))
        ))
        self.play(Create(arc), angle.animate.set_value(PI/2), run_time=5)
        
        # Adicionando as linhas de seno e cosseno
        sine_line = always_redraw(lambda: Line(
            start=axes.c2p(2 * np.cos(angle.get_value()), 0),
            end=axes.c2p(2 * np.cos(angle.get_value()), 2 * np.sin(angle.get_value())),
            color=GREEN
        ))
        cosine_line = always_redraw(lambda: Line(
            start=axes.c2p(0, 0),
            end=axes.c2p(2 * np.cos(angle.get_value()), 0),
            color=RED
        ))
        self.play(Create(sine_line), Create(cosine_line))

        # Mostrando a relação seno, cosseno e tangente
        sine_text = always_redraw(lambda: MathTex(
            "sen(\\theta)=" + f"{np.sin(angle.get_value()):.2f}"
        ).next_to(sine_line, LEFT))
        cosine_text = always_redraw(lambda: MathTex(
            "cos(\\theta)=" + f"{np.cos(angle.get_value()):.2f}"
        ).next_to(cosine_line, DOWN))
        tangent_text = always_redraw(lambda: MathTex(
            "tan(\\theta)=" + f"{np.tan(angle.get_value()):.2f}"
        ).next_to(moving_dot, UP))
        self.play(Write(sine_text), Write(cosine_text), Write(tangent_text))

        # Animar o ponto ao redor do círculo
        self.play(angle.animate.set_value(2 * PI), run_time=20, rate_func=linear)

        # Finalizar a animação
        self.wait(5)