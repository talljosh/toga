from math import pi, cos, sin

import toga
import toga_dummy
from toga.font import SANS_SERIF, SERIF
from toga_dummy.utils import TestCase
from toga.color import REBECCAPURPLE, BLANCHEDALMOND, CRIMSON, rgb


class CanvasTests(TestCase):
    def setUp(self):
        super().setUp()

        # Create a canvas with the dummy factory
        self.testing_canvas = toga.Canvas(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.testing_canvas._impl.interface, self.testing_canvas)
        self.assertActionPerformed(self.testing_canvas, "create Canvas")

    def test_basic_drawing(self):
        with self.testing_canvas.context() as basic_context:
            with basic_context.fill(
                color="rgba(0, 0, 0, 0.4)", preserve=True
            ) as fill_test:
                self.assertActionPerformedWith(self.testing_canvas, "new path")
                with fill_test.stroke(
                    color="rgba(0, 0, 0, 0.6)", line_width=1
                ) as stroke_test:
                    rect = stroke_test.rect(-3, -3, 6, 6)
                    self.assertIn(rect, stroke_test.drawing_objects)
                    self.assertActionPerformedWith(
                        self.testing_canvas, "rect", x=-3, y=-3, width=6, height=6
                    )
                self.assertIn(stroke_test.drawing_objects, fill_test.drawing_objects)
                self.assertActionPerformedWith(self.testing_canvas, "stroke")
            self.assertIn(fill_test.drawing_objects, basic_context.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, "fill")
        self.assertIn(
            basic_context.drawing_objects, self.testing_canvas.drawing_objects
        )

    def test_self_oval_path(self):
        xc = 50
        yc = 60
        xr = 25
        yr = 30
        translate = self.testing_canvas.translate(xc, yc)
        self.assertIn(translate, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "translate", tx=xc, ty=yc)
        scale = self.testing_canvas.scale(1.0, yr / xr)
        self.assertIn(scale, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "scale", sx=1.0, sy=yr / xr)
        with self.testing_canvas.closed_path(xr, 0.0) as closed:
            self.assertActionPerformedWith(self.testing_canvas, "move to", x=xr, y=0.0)
            arc = closed.arc(0, 0, xr, 0, 2 * pi)
            self.assertIn(arc, closed.drawing_objects)
            self.assertActionPerformedWith(
                self.testing_canvas,
                "arc",
                x=0,
                y=0,
                radius=xr,
                startangle=0,
                endangle=2 * pi,
                anticlockwise=False,
            )
        self.assertActionPerformedWith(self.testing_canvas, "closed path")

    def test_fill_checks(self):
        check_size = 32
        x = 10
        y = -10
        width = 200
        height = 200
        with self.testing_canvas.fill(color="rgba(1, 1, 1, 1)") as fill1:
            rect = fill1.rect(x, y, width, height)
            self.assertIn(rect, fill1.drawing_objects)
            self.assertActionPerformedWith(
                self.testing_canvas, "rect", x=10, y=-10, width=200, height=200
            )
        self.assertActionPerformedWith(self.testing_canvas, "fill")

        with self.testing_canvas.fill(color="rgba(1, 1, 1, 1)") as fill2:
            # Only works for check_size a power of 2
            for j in range(x & -check_size, height, check_size):
                for i in range(y & -check_size, width, check_size):
                    if (i / check_size + j / check_size) % 2 == 0:
                        rect = fill2.rect(i, j, check_size, check_size)
                        self.assertIn(rect, fill2.drawing_objects)
                        self.assertActionPerformedWith(
                            self.testing_canvas,
                            "rect",
                            x=i,
                            y=j,
                            width=check_size,
                            height=check_size,
                        )
        self.assertActionPerformedWith(self.testing_canvas, "fill")

    def test_draw_3circles(self):
        xc = 100
        yc = 150
        radius = 0.5 * 50 - 10
        alpha = 0.8
        subradius = radius * (2 / 3. - 0.1)

        with self.testing_canvas.fill(
            color="rgba(1, 0, 0, " + str(alpha) + ")"
        ) as fill1:
            ellipse1 = fill1.ellipse(
                xc + radius / 3. * cos(pi * 0.5),
                yc - radius / 3. * sin(pi * 0.5),
                subradius,
                subradius,
                2.0 * pi,
            )
            self.assertIn(ellipse1, fill1.drawing_objects)
            self.assertActionPerformedWith(
                self.testing_canvas,
                "ellipse",
                x=xc + radius / 3. * cos(pi * 0.5),
                y=yc - radius / 3. * sin(pi * 0.5),
                radiusx=subradius,
                radiusy=subradius,
                rotation=2.0 * pi,
            )
        self.assertActionPerformedWith(self.testing_canvas, "fill")

        with self.testing_canvas.fill(
            color="rgba(0, 1, 0, " + str(alpha) + ")"
        ) as fill2:
            ellipse2 = fill2.ellipse(
                xc + radius / 3. * cos(pi * (0.5 + 2 / .3)),
                yc - radius / 3. * sin(pi * (0.5 + 2 / .3)),
                subradius,
                subradius,
            )
            self.assertIn(ellipse2, fill2.drawing_objects)
            self.assertActionPerformedWith(
                self.testing_canvas,
                "ellipse",
                x=xc + radius / 3. * cos(pi * (0.5 + 2 / .3)),
                y=yc - radius / 3. * sin(pi * (0.5 + 2 / .3)),
                radiusx=subradius,
                radiusy=subradius,
            )
        self.assertActionPerformedWith(self.testing_canvas, "fill")

        with self.testing_canvas.fill(
            color="rgba(0, 0, 1, " + str(alpha) + ")"
        ) as fill3:
            ellipse3 = fill3.ellipse(
                xc + radius / 3. * cos(pi * (0.5 + 4 / .3)),
                yc - radius / 3. * sin(pi * (0.5 + 4 / .3)),
                subradius,
                subradius,
            )
            self.assertIn(ellipse3, fill3.drawing_objects)
            self.assertActionPerformedWith(
                self.testing_canvas,
                "ellipse",
                x=xc + radius / 3. * cos(pi * (0.5 + 4 / .3)),
                y=yc - radius / 3. * sin(pi * (0.5 + 4 / .3)),
                radiusx=subradius,
                radiusy=subradius,
            )
        self.assertActionPerformedWith(self.testing_canvas, "fill")

    def test_draw_triangle(self):
        with self.testing_canvas.closed_path(32, 0) as closed:
            self.assertActionPerformedWith(self.testing_canvas, "move to", x=32, y=0)
            line_to1 = closed.line_to(32, 64)
            self.assertIn(line_to1, closed.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, "line to", x=32, y=64)
            line_to2 = closed.line_to(-64, 0)
            self.assertIn(line_to2, closed.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, "line to", x=-64, y=0)
        self.assertActionPerformedWith(self.testing_canvas, "closed path")

    def test_context_repr(self):
        with self.testing_canvas.context() as context:
            self.assertEqual(repr(context), "Context()")

    def test_new_path_simple(self):
        new_path = self.testing_canvas.new_path()
        self.assertIn(new_path, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "new path")

    def test_new_path_remove(self):
        new_path = self.testing_canvas.new_path()
        self.testing_canvas.remove(new_path)
        self.assertNotIn(new_path, self.testing_canvas.drawing_objects)

    def test_new_path_repr(self):
        new_path = self.testing_canvas.new_path()
        self.assertEqual(repr(new_path), "NewPath()")

    def test_closed_path_modify(self):
        with self.testing_canvas.closed_path(0, -5) as closed:
            closed.line_to(10, 10)
            closed.line_to(10, 0)
            closed.move_to_obj.modify(0, 0)
            closed.redraw()
            self.assertActionPerformedWith(self.testing_canvas, "move to", x=0, y=0)

    def test_closed_path_repr(self):
        with self.testing_canvas.closed_path(0.5, -0.5) as closed:
            self.assertEqual(repr(closed), "ClosedPath(x=0.5, y=-0.5)")

    def test_move_to_simple(self):
        move_to1 = self.testing_canvas.move_to(5, 7)
        self.assertIn(move_to1, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "move to", x=5, y=7)

    def test_move_to_modify(self):
        move_to2 = self.testing_canvas.move_to(-5, 20.0)
        move_to2.modify(x=0, y=-10)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(self.testing_canvas, "move to", x=0, y=-10)

    def test_move_to_repr(self):
        move_to3 = self.testing_canvas.move_to(x=0.5, y=1000)
        self.assertEqual(repr(move_to3), "MoveTo(x=0.5, y=1000)")

    def test_line_to_simple(self):
        line_to = self.testing_canvas.line_to(2, 3)
        self.assertIn(line_to, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "line to", x=2, y=3)

    def test_line_to_modify(self):
        line_to = self.testing_canvas.line_to(-40.5, 50.5)
        line_to.modify(x=0, y=5)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(self.testing_canvas, "line to", x=0, y=5)

    def test_line_to_repr(self):
        line_to = self.testing_canvas.line_to(x=1.5, y=-1000)
        self.assertEqual(repr(line_to), "LineTo(x=1.5, y=-1000)")

    def test_bezier_curve_to_simple(self):
        bezier = self.testing_canvas.bezier_curve_to(1, 1, 2, 2, 5, 5)
        self.assertIn(bezier, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(
            self.testing_canvas,
            "bezier curve to",
            cp1x=1,
            cp1y=1,
            cp2x=2,
            cp2y=2,
            x=5,
            y=5,
        )

    def test_bezier_curve_to_modify(self):
        bezier = self.testing_canvas.bezier_curve_to(0, 0, -2, -2, 5.5, 5.5)
        bezier.modify(cp1x=6, cp1y=-5, cp2x=2.0, cp2y=0, x=-2, y=-3)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas,
            "bezier curve to",
            cp1x=6,
            cp1y=-5,
            cp2x=2.0,
            cp2y=0,
            x=-2,
            y=-3,
        )

    def test_bezier_curve_to_repr(self):
        bezier = self.testing_canvas.bezier_curve_to(
            cp1x=2.0, cp1y=2.0, cp2x=4.0, cp2y=4.0, x=10, y=10
        )
        self.assertEqual(
            repr(bezier),
            "BezierCurveTo(cp1x=2.0, cp1y=2.0, cp2x=4.0, cp2y=4.0, x=10, y=10)",
        )

    def test_quadratic_curve_to_simple(self):
        quad = self.testing_canvas.quadratic_curve_to(1, 1, 5, 5)
        self.assertIn(quad, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(
            self.testing_canvas, "quadratic curve to", cpx=1, cpy=1, x=5, y=5
        )

    def test_quadratic_curve_to_modify(self):
        quad = self.testing_canvas.quadratic_curve_to(-1, -1, -5, -5)
        quad.modify(0, 0.5, -0.4, 1000)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas, "quadratic curve to", cpx=0, cpy=0.5, x=-0.4, y=1000
        )

    def test_quadratic_curve_to_repr(self):
        quad = self.testing_canvas.quadratic_curve_to(1020.2, 1, -5, 0.5)
        self.assertEqual(repr(quad), "QuadraticCurveTo(cpx=1020.2, cpy=1, x=-5, y=0.5)")

    def test_arc_simple(self):
        arc = self.testing_canvas.arc(-10, -10, 10, pi / 2, 0, True)
        self.assertIn(arc, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(
            self.testing_canvas,
            "arc",
            x=-10,
            y=-10,
            radius=10,
            startangle=pi / 2,
            endangle=0,
            anticlockwise=True,
        )

    def test_arc_modify(self):
        arc = self.testing_canvas.arc(10, 10, 10.0, 2, pi, False)
        arc.modify(
            x=1000,
            y=2000,
            radius=0.1,
            startangle=pi,
            endangle=2 * pi,
            anticlockwise=False,
        )
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas,
            "arc",
            x=1000,
            y=2000,
            radius=0.1,
            startangle=pi,
            endangle=2 * pi,
            anticlockwise=False,
        )

    def test_arc_repr(self):
        arc = self.testing_canvas.arc(1, 2, 3, 2, -3.141592, False)
        self.assertEqual(
            repr(arc),
            "Arc(x=1, y=2, radius=3, startangle=2, endangle=-3.141592, anticlockwise=False)",
        )

    def test_remove_arc(self):
        arc = self.testing_canvas.arc(-10, -10, 10, pi / 2, 0, True)
        self.assertIn(arc, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(
            self.testing_canvas,
            "arc",
            x=-10,
            y=-10,
            radius=10,
            startangle=pi / 2,
            endangle=0,
            anticlockwise=True,
        )
        self.testing_canvas.remove(arc)
        self.assertNotIn(arc, self.testing_canvas.drawing_objects)

    def test_ellipse_simple(self):
        ellipse = self.testing_canvas.ellipse(1, 1, 50, 20, 0, pi, 2 * pi, False)
        self.assertIn(ellipse, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(
            self.testing_canvas,
            "ellipse",
            x=1,
            y=1,
            radiusx=50,
            radiusy=20,
            rotation=0,
            startangle=pi,
            endangle=2 * pi,
            anticlockwise=False,
        )

    def test_ellipse_modify(self):
        ellipse = self.testing_canvas.ellipse(0, -1, -50, 20.2, pi, pi, 2 * pi, False)
        ellipse.modify(
            x=1,
            y=0,
            radiusx=0.1,
            radiusy=1000,
            rotation=2 * pi,
            startangle=0,
            endangle=pi,
        )
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas,
            "ellipse",
            x=1,
            y=0,
            radiusx=0.1,
            radiusy=1000,
            rotation=2 * pi,
            startangle=0,
            endangle=pi,
            anticlockwise=False,
        )

    def test_ellipse_repr(self):
        ellipse = self.testing_canvas.ellipse(1.0, 1.0, 0, 0, 0, 2, 3.1415, False)
        self.assertEqual(
            repr(ellipse),
            "Ellipse(x=1.0, y=1.0, radiusx=0, radiusy=0, rotation=0, startangle=2, endangle=3.1415, "
            "anticlockwise=False)",
        )

    def test_rect_modify(self):
        rect = self.testing_canvas.rect(-5, 5, 10, 15)
        rect.modify(5, -5, 0.5, -0.5)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas, "rect", x=5, y=-5, width=0.5, height=-0.5
        )

    def test_rect_repr(self):
        rect = self.testing_canvas.rect(x=1000.2, y=2000, width=3000, height=-4000.0)
        self.assertEqual(
            repr(rect), "Rect(x=1000.2, y=2000, width=3000, height=-4000.0)"
        )

    def test_fill_modify(self):
        with self.testing_canvas.fill(
            color="rgb(0, 255, 0)", fill_rule="nonzero", preserve=False
        ) as filler:
            filler.modify(color=REBECCAPURPLE, fill_rule="evenodd", preserve=True)
            self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas,
            "fill",
            color=rgb(102, 51, 153),
            fill_rule="evenodd",
            preserve=True,
        )

    def test_fill_repr(self):
        with self.testing_canvas.fill(
            color=CRIMSON, fill_rule="evenodd", preserve=True
        ) as filler:
            self.assertEqual(
                repr(filler),
                "Fill(color=rgb(220, 20, 60), fill_rule=evenodd, preserve=True)",
            )

    def test_stroke_modify(self):
        with self.testing_canvas.stroke(
            color=BLANCHEDALMOND, line_width=5.0
        ) as stroker:
            stroker.modify(color=REBECCAPURPLE, line_width=1)
            self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas, "stroke", color=rgb(102, 51, 153), line_width=1
        )

    def test_stroke_repr(self):
        with self.testing_canvas.stroke() as stroker:
            self.assertEqual(
                repr(stroker), "Stroke(color=rgb(0, 0, 0), line_width=2.0)"
            )

    def test_rotate_simple(self):
        rotate = self.testing_canvas.rotate(pi)
        self.assertIn(rotate, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "rotate", radians=pi)

    def test_rotate_modify(self):
        rotate = self.testing_canvas.rotate(radians=-2 * pi)
        rotate.modify(radians=3 * pi / 2)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas, "rotate", radians=3 * pi / 2
        )

    def test_rotate_repr(self):
        rotate = self.testing_canvas.rotate(0.1)
        self.assertEqual(repr(rotate), "Rotate(radians=0.1)")

    def test_scale_simple(self):
        scale = self.testing_canvas.scale(2, 1.5)
        self.assertIn(scale, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "scale", sx=2, sy=1.5)

    def test_scale_modify(self):
        scale = self.testing_canvas.scale(sx=-2, sy=0)
        scale.modify(sx=-2.0, sy=3.0)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(self.testing_canvas, "scale", sx=-2.0, sy=3.0)

    def test_scale_repr(self):
        scale = self.testing_canvas.scale(sx=500, sy=-500)
        self.assertEqual(repr(scale), "Scale(sx=500, sy=-500)")

    def test_translate_simple(self):
        translate = self.testing_canvas.translate(5, 3.5)
        self.assertIn(translate, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "translate", tx=5, ty=3.5)

    def test_translate_modify(self):
        translate = self.testing_canvas.translate(tx=2.3, ty=-2)
        translate.modify(tx=0, ty=-500)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(self.testing_canvas, "translate", tx=0, ty=-500)

    def test_translate_repr(self):
        translate = self.testing_canvas.translate(tx=0, ty=-3.2)
        self.assertEqual(repr(translate), "Translate(tx=0, ty=-3.2)")

    def test_reset_transform_simple(self):
        reset_transform = self.testing_canvas.reset_transform()
        self.assertIn(reset_transform, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, "reset transform")

    def test_reset_transform_repr(self):
        reset_transform = self.testing_canvas.reset_transform()
        self.assertEqual(repr(reset_transform), "ResetTransform()")

    def test_write_text_simple(self):
        test_font = toga.Font(family=SANS_SERIF, size=15)
        write_text = self.testing_canvas.write_text("test text", 0, 0, test_font)
        self.assertIn(write_text, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(
            self.testing_canvas,
            "write text",
            text="test text",
            x=0,
            y=0,
            font=test_font,
        )

    def test_write_text_default(self):
        write_text = self.testing_canvas.write_text("test text")
        self.assertActionPerformedWith(
            self.testing_canvas, "write text", text="test text"
        )
        self.assertEqual(
            repr(write_text),
            "WriteText(text=test text, x=0, y=0, font=<Font: 12pt system>)",
        )

    def test_write_text_modify(self):
        write_text = self.testing_canvas.write_text("test text")
        modify_font = toga.Font(family=SERIF, size=1.2)
        write_text.modify("hello again", x=10, y=-1999, font=modify_font)
        self.testing_canvas.redraw()
        self.assertActionPerformedWith(
            self.testing_canvas,
            "write text",
            text="hello again",
            x=10,
            y=-1999,
            font=modify_font,
        )

    def test_write_text_repr(self):
        font = toga.Font(family=SERIF, size=4)
        write_text = self.testing_canvas.write_text("hello", x=10, y=-4.2, font=font)
        self.assertEqual(
            repr(write_text),
            "WriteText(text=hello, x=10, y=-4.2, font=<Font: 4pt serif>)",
        )
