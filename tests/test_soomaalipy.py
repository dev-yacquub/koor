"""
Tests for SoomaaliPy transpiler, runtime, and error translator.
"""

import io
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr

from soomaalipy.transpiler import to_python, to_somali
from soomaalipy.runtime import run_code, get_somali_builtins
from soomaalipy.errors import translate_error_message, translate_exception_name


class TestTranspiler(unittest.TestCase):

    def test_keywords_transpilation(self):
        code = (
            "haddii x == 10:\n"
            "    daabac('toban')\n"
            "haddii_kale x == 20:\n"
            "    daabac('labaatan')\n"
            "kale:\n"
            "    daabac('kale')\n"
        )
        expected = (
            "if x == 10:\n"
            "    print('toban')\n"
            "elif x == 20:\n"
            "    print('labaatan')\n"
            "else:\n"
            "    print('kale')\n"
        )
        self.assertEqual(to_python(code), expected)

    def test_functions_and_loops(self):
        code = (
            "hawl salaan(magac):\n"
            "    celi f'Salaan {magac}'\n"
            "\n"
            "inta Run:\n"
            "    jooji\n"
            "\n"
            "kasta i ku tirsan(5):\n"
            "    sii_wad\n"
        )
        expected = (
            "def salaan(magac):\n"
            "    return f'Salaan {magac}'\n"
            "\n"
            "while True:\n"
            "    break\n"
            "\n"
            "for i in range(5):\n"
            "    continue\n"
        )
        self.assertEqual(to_python(code), expected)

    def test_string_preservation(self):
        # Keywords inside strings should NEVER be touched!
        code = 'qoraal = "haddii kale hawl celi run been waxba"'
        expected = 'qoraal = "haddii kale hawl celi run been waxba"'
        self.assertEqual(to_python(code), expected)

    def test_comment_preservation(self):
        # Comments should remain intact
        code = "# Tani waa faallo: haddii kale celi"
        expected = "# Tani waa faallo: haddii kale celi"
        self.assertEqual(to_python(code), expected)

    def test_boolean_and_logic_operators(self):
        code = "a = Run iyo Been ama ma Run"
        expected = "a = True and False or not True"
        self.assertEqual(to_python(code), expected)

    def test_exceptions_and_classes(self):
        code = (
            "fasal Tijaabo:\n"
            "    dhaaf\n"
            "isku_day:\n"
            "    tuur KhaladQiimo('khalad')\n"
            "qabo KhaladQiimo:\n"
            "    dhaaf\n"
        )
        expected = (
            "class Tijaabo:\n"
            "    pass\n"
            "try:\n"
            "    raise ValueError('khalad')\n"
            "except ValueError:\n"
            "    pass\n"
        )
        self.assertEqual(to_python(code), expected)

    def test_reverse_transpiler(self):
        py_code = (
            "if x > 5:\n"
            "    print('weyn')\n"
            "else:\n"
            "    print('yar')\n"
        )
        so_code = to_somali(py_code)
        self.assertIn("haddii", so_code)
        self.assertIn("daabac", so_code)
        self.assertIn("kale", so_code)


class TestRuntimeExecution(unittest.TestCase):

    def test_run_simple_program(self):
        code = (
            "x = 10\n"
            "y = 25\n"
            "wadar = isku_dar([x, y])\n"
            "daabac(wadar)\n"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            success = run_code(code)
        self.assertTrue(success)
        self.assertEqual(buf.getvalue().strip(), "35")

    def test_run_functions(self):
        code = (
            "hawl labanlaab(n):\n"
            "    celi n * 2\n"
            "\n"
            "natiijo = labanlaab(7)\n"
            "daabac(natiijo)\n"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            success = run_code(code)
        self.assertTrue(success)
        self.assertEqual(buf.getvalue().strip(), "14")

    def test_run_oop(self):
        code = (
            "fasal Xisaab:\n"
            "    hawl __init__(self, qiimo):\n"
            "        self.qiimo = qiimo\n"
            "    hawl qaad(self):\n"
            "        celi self.qiimo * 10\n"
            "obj = Xisaab(5)\n"
            "daabac(obj.qaad())\n"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            success = run_code(code)
        self.assertTrue(success)
        self.assertEqual(buf.getvalue().strip(), "50")

    def test_builtins_availability(self):
        env = get_somali_builtins()
        self.assertIn("daabac", env)
        self.assertIn("dherer", env)
        self.assertIn("tirsan", env)
        self.assertIn("Run", env)
        self.assertIn("Been", env)


class TestErrorTranslation(unittest.TestCase):

    def test_translate_zero_division(self):
        msg = translate_error_message("division by zero")
        self.assertIn("eber", msg)

    def test_translate_name_error(self):
        msg = translate_error_message("name 'foo' is not defined")
        self.assertIn("foo", msg)
        self.assertIn("lama yaqaan", msg)

    def test_translate_index_error(self):
        msg = translate_error_message("list index out of range")
        self.assertIn("Tusmada liisku", msg)

    def test_translate_exception_name(self):
        self.assertEqual(translate_exception_name("ZeroDivisionError"), "KhaladEberLooQaybiyay")
        self.assertEqual(translate_exception_name("NameError"), "KhaladMagac")
        self.assertEqual(translate_exception_name("TypeError"), "KhaladNooc")


if __name__ == "__main__":
    unittest.main()
