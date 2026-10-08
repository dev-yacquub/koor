"""
Unit Tests for Koor Programming Language.
"""

import unittest
import textwrap
from io import StringIO
from contextlib import redirect_stdout
from koor.lexer import Lexer
from koor.parser import Parser
from koor.interpreter import Interpreter
from koor.errors import KhaladNaxwo, KhaladMagac

class TestKoorLanguage(unittest.TestCase):
    def orod(self, kood: str) -> str:
        kood = textwrap.dedent(kood).strip()
        tokens = Lexer(kood).tokens_saar()
        ast = Parser(tokens).parse()
        f = StringIO()
        vm = Interpreter(wax_soo_saar_qabte=lambda s: f.write(s + "\n"))
        vm.fuli(ast)
        return f.getvalue().strip()

    def test_user_sentence_exact(self):
        kood = '''
        x waa 12.
        haddi x ay la mid tahay 12 waxaad soo saartaa " waad guulaysatay ".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "waad guulaysatay")

    def test_user_sentence_negative(self):
        kood = '''
        x waa 10.
        haddi x ay la mid tahay 12 waxaad soo saartaa " waad guulaysatay ".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "")

    def test_arithmetic_and_modifications(self):
        kood = '''
        a waa 20.
        waxaad ku dartaa 10 a.
        waxaad ka jartaa 5 a.
        waxaad soo saartaa a.
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "25")

    def test_while_loop(self):
        kood = '''
        i waa 0.
        inta i < 3:
            waxaad soo saartaa i.
            waxaad ku dartaa 1 i.
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "0\n1\n2")

    def test_repeat_loop(self):
        kood = '''
        ku celi 3 jeer:
            waxaad soo saartaa "hello".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "hello\nhello\nhello")

    def test_functions(self):
        kood = '''
        hawl labanlaab(n):
            waxaad soo celisaa n * 2.
        waxaad soo saartaa labanlaab(7).
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "14")

    def test_name_error_suggestion(self):
        kood = '''
        magac waa "Cali".
        waxaad soo saartaa magacc.
        '''
        with self.assertRaises(KhaladMagac) as ctx:
            self.orod(kood)
        self.assertIn("Miyaad u jeedday 'magac'?", str(ctx.exception))

    def test_arrays(self):
        kood = '''
        liis waa [1, 2, 3].
        liis.ku_dar(4).
        liis[0] = 99.
        waxaad soo saartaa liis[0].
        waxaad soo saartaa dherer(liis).
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "99\n4")

    def test_strings(self):
        kood = '''
        heeso waa "  soomaali  ".
        waxaad soo saartaa heeso.jar().weyneey().
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "SOOMAALI")

    def test_dictionaries(self):
        kood = '''
        qof waa {"magac": "Faadumo", "da'": 20}.
        qof["da'"] = 21.
        waxaad soo saartaa qof["magac"].
        waxaad soo saartaa qof["da'"].
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Faadumo\n21")

    def test_string_interpolation_io(self):
        kood = '''
        magac waa "Warsame".
        da' waa 25.
        waxaad soo saartaa "Magaca: {magac}, Da'da: {da'}".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Magaca: Warsame, Da'da: 25")

    def test_break_continue(self):
        kood = '''
        i waa 0.
        inta i < 10:
            waxaad ku dartaa 1 i.
            haddii i ay la mid tahay 2:
                ka bood.
            haddii i ay la mid tahay 4:
                ka bax.
            waxaad soo saartaa i.
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "1\n3")

    def test_data_types(self):
        kood = '''
        waxaad soo saartaa nooc(10).
        waxaad soo saartaa nooc("qoraal").
        waxaad soo saartaa nooc([1, 2]).
        waxaad soo saartaa nooc({"a": 1}).
        waxaad soo saartaa nooc(run).
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "tiro\nqoraal\nliis\nqaamuus\nrun_been")


    def test_hawshu_waa_and_qabo_hawshan(self):
        kood = '''
        hawshu waa ("iskudhufasho ")
        (x*y)

        qabo hawshan ("iskudhufasho") (12,3)
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "36")

    def test_logical_operator_sidoo_kale(self):
        kood = '''
        x waa 10.
        y waa 20.
        haddii x uu ka weyn yahay 5 sidoo kale y uu ka yar yahay 30:
            waxaad soo saartaa "Labada shardi waa run".
        haddii x ay la mid tahay 10 sidoo kale y ay la mid tahay 99:
            waxaad soo saartaa "Khalad".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Labada shardi waa run")

    def test_input_waydiin(self):
        from unittest.mock import patch
        kood = '''
        magac waa waydiin("Magacaa? ").
        waxaad soo saartaa "Salaan {magac}!".
        '''
        with patch('builtins.input', return_value='Faadumo'):
            natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Salaan Faadumo!")

    def test_control_flow_hadii_kale_oo_ay_uu(self):
        kood = '''
        dhibco waa 85.
        hadii dhibco >= 90:
            waxaad soo saartaa "A".
        hadii kale oo ay dhibco >= 80:
            waxaad soo saartaa "B".
        hadii kale oo uu dhibco >= 70:
            waxaad soo saartaa "C".
        kale:
            waxaad soo saartaa "D".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "B")

        kood2 = '''
        dhibco waa 72.
        haddii dhibco >= 90:
            waxaad soo saartaa "A".
        haddii kale oo ay dhibco >= 80:
            waxaad soo saartaa "B".
        haddii kale oo uu dhibco >= 70:
            waxaad soo saartaa "C".
        haddii kale:
            waxaad soo saartaa "D".
        '''
        natiijo2 = self.orod(kood2)
        self.assertEqual(natiijo2, "C")

    def test_loop_mid_kastoo(self):
        kood = '''
        magaalooyinka waa ["Muqdisho", "Hargeysa", "Garoowe", "Kismaayo"].
        mid kastoo ku jira magaalooyinka ( mag ):
            waxaad soo saartaa "Ku soo dhawoow magaalada {mag}.".
        '''
        natiijo = self.orod(kood)
        filan = (
            "Ku soo dhawoow magaalada Muqdisho.\n"
            "Ku soo dhawoow magaalada Hargeysa.\n"
            "Ku soo dhawoow magaalada Garoowe.\n"
            "Ku soo dhawoow magaalada Kismaayo."
        )
        self.assertEqual(natiijo, filan)

    def test_nasiib_random(self):
        kood = '''
        t waa nasiib(5, 10).
        haddii t >= 5 sidoo kale t <= 10:
            waxaad soo saartaa "Sax".
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Sax")

    def test_zero_signs_arithmetic(self):
        kood = '''
        a waa 50 ku dar 20
        b waa a ka jar 10
        c waa b ku dhufo 2
        d waa c u qaybi 4
        e waa 17 haraaga 5
        waxaad soo saartaa d
        waxaad soo saartaa e
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "30.0\n2")

    def test_zero_signs_functions(self):
        kood = '''
        hawl kala_goo oo qaadata x iyo y
            waxaad soo celisaa x ka jar y

        natiijo waa kala_goo 30 iyo 12
        soo saar tiradaadu waa {natiijo}
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "tiradaadu waa 18")

    def test_zero_signs_functions_no_oo_qaadata(self):
        kood = '''
        hawl kala_goo x y
            waxaad soo celisaa x ka jar y

        natiijo waa kala_goo 50 20
        soo saar tiradaadu waa natiijo
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "tiradaadu waa 30")

    def test_zero_signs_loops_and_conditionals(self):
        kood = '''
        x waa 10
        haddii x ka weyn yahay 5
            waxaad soo saartaa "Sax"

        ku celi 2 jeer
            waxaad soo saartaa "Koor"

        ardayda waa liiska "Axmed" iyo "Caasha"
        mid kastoo ku jira ardayda qof
            waxaad soo saartaa qof
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Sax\nKoor\nKoor\nAxmed\nCaasha")

    def test_structured_function_syntax(self):
        kood = '''
        hawl
        magaceed waa : isku dhufasho
        tibxuhu waa : x , y
        hawshu waa : x ku dhufo y
        kaydi natiijada

        jawaab waa isku_dhufasho 6 7
        soo saar tiradaadu waa {jawaab}
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "tiradaadu waa 42")

    def test_structured_function_without_signs(self):
        kood = '''
        hawl
        magaceed waa kala_goo
        tibxuhu waa a b
        hawshu waa a ka jar b
        kaydi natiijada

        jawaab waa kala_goo 100 35
        soo saar natiijadu waa jawaab
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "natiijadu waa 65")

    def test_in_place_mutation_da_waxaad_ku_dartaa(self):
        kood = '''
        da' waa 20
        da' waxaad ku dartaa 5
        da' waxaad ka jartaa 2
        da' waxaad ku dhufataa 2
        da' waxaad u qaybisaa 4
        soo saar "Da'du waa: {da'}"
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Da'du waa: 11.5")

    def test_in_place_mutation_waxaad_qiimo_ku_dartaa(self):
        kood = '''
        tirsade waa 1
        waxaad 1 ku dartaa tirsade
        waxaad 5 ku dartaa tirsade
        waxaad 2 ka jartaa tirsade
        soo saar tirsade
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "5")

    def test_function_call_qabo_hawshan_unquoted_and_zero_args(self):
        kood = '''
        hawl
        magaceed waa : salaan
        hawshu waa : soo saar "Ku soo dhawoow!"

        hawl
        magaceed waa : isku dhufasho
        tibxuhu waa : x , y
        hawshu waa : x ku dhufo y
        kaydi natiijada

        qabo hawshan (salaan)
        natiijo waa qabo hawshan (isku dhufasho) (6, 7)
        soo saar "Natiijo: {natiijo}"
        '''
        natiijo = self.orod(kood)
        self.assertEqual(natiijo, "Ku soo dhawoow!\nNatiijo: 42")

    def test_while_loop_with_waxaad_1_ku_dartaa(self):
        kood = '''
        soo saar "--- Wareegga 'inta' ---"
        tirsade waa 1
        inta tirsade ka yar yahay ama la mid yahay 3
            soo saar "Tirsade waa: {tirsade}"
            waxaad 1 ku dartaa tirsade
        '''
        natiijo = self.orod(kood)
        filan = (
            "--- Wareegga 'inta' ---\n"
            "Tirsade waa: 1\n"
            "Tirsade waa: 2\n"
            "Tirsade waa: 3"
        )
        self.assertEqual(natiijo, filan)

    def test_for_each_loop_with_parens_and_inferred_list(self):
        kood = '''
        soo saar "--- Wareegga 'mid kastoo' ---"
        ardayda waa liiska "Cali" iyo "Aamina" iyo "Warsame"
        mid kastoo ku jira (qof)
            soo saar "Ku soo dhawoow {qof}!"
        '''
        natiijo = self.orod(kood)
        filan = (
            "--- Wareegga 'mid kastoo' ---\n"
            "Ku soo dhawoow Cali!\n"
            "Ku soo dhawoow Aamina!\n"
            "Ku soo dhawoow Warsame!"
        )
        self.assertEqual(natiijo, filan)

        kood2 = '''
        ardayda waa liiska "Cali" iyo "Aamina"
        mid kastoo ku jira ardayda (qof)
            soo saar "Ku soo dhawoow {qof}!"
        '''
        natiijo2 = self.orod(kood2)
        self.assertEqual(natiijo2, "Ku soo dhawoow Cali!\nKu soo dhawoow Aamina!")


if __name__ == "__main__":
    unittest.main()

