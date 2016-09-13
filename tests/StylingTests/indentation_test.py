import unittest
import src
import src.ErrorMessagesBuilder.error_message_handler as Err
import src.ErrorMessagesBuilder.ErrorBuilder.error_messages_constants as ErrConst
import os



class TestIndentation(unittest.TestCase):
    WARNINGS = 'Warnings'
    STATUS = 'Status'
    SUCCESS = 'Success'

    @classmethod
    def setUpClass(cls):
        cls.error = Err.ErrorMessageHandler()
        cls.indentCheck = src.CheckIndentationCommand()
        this_dir, this_filename = os.path.split(__file__)
        cls.filepath_prefix = os.path.join(this_dir, "../StylingTestFiles/")

    def testNoIndentation(self):
        config = src.load_config_file(user='Indentation/indentation-config.json', default='test-config.json')
        exp_result = None
        result = self.indentCheck.execute({"current_indentation_level": 0,
                                           "characters": "var i = 3",
                                           "indentation_level": 0, **config['check_indentation']['params']})
        self.assertEqual(result[0], exp_result)

    def testSingleIndentation(self):
        config = src.load_config_file(user='Indentation/indentation-config.json', default='test-config.json')
        exp_result = None
        result = self.indentCheck.execute({"current_indentation_level": 1,
                                           "characters": "    var i = 3",
                                           "indentation_level": 0, **config['check_indentation']['params']})
        self.assertEqual(result[0], exp_result)

    def testIndentationError(self):
        config = src.load_config_file(user='Indentation/indentation-config.json', default='test-config.json')
        file_name = self.filepath_prefix + "BasicIndentation.txt"
        file = src.get_string_to_parse(file_name)
        exp_result = [self.error.get(ErrConst.TAB_INDENTATION_ERROR, [4, 2])]
        self.lexer = src.Lexer(config)
        result = self.lexer.lex(file)
        self.assertEqual(exp_result, result[self.WARNINGS])

    def testAdvancedIndentationSuccess(self):
        config = src.load_config_file(user='Indentation/indentation-config.json', default='test-config.json')
        file_name = self.filepath_prefix + "AdvancedIndentation.txt"
        file = src.get_string_to_parse(file_name)
        exp_result = []
        self.lexer = src.Lexer(config)
        result = self.lexer.lex(file)
        self.assertEqual(exp_result, result[self.WARNINGS])

    def testIndentWithOnlyTabsWithError(self):
        config = src.load_config_file(user="Indentation/tab-only-indentation.json", default='test-config.json')
        file_name = self.filepath_prefix + "IndentWithTabsOnly.txt"
        file = src.get_string_to_parse(file_name)
        exp_result = [self.error.get(ErrConst.TAB_AND_SPACES, [10])]
        self.lexer = src.Lexer(config)
        result = self.lexer.lex(file)
        self.assertEqual(exp_result, result[self.WARNINGS])

    def testReallyAdvancedIndentation(self):
        config = src.load_config_file(user="Indentation/indentation-config.json", default='test-config.json')
        file_name = self.filepath_prefix + "SampleAdvancedIndentation.txt"
        file = src.get_string_to_parse(file_name)
        exp_result = []
        exp_status = "Success"
        self.lexer = src.Lexer(config)
        result = self.lexer.lex(file)
        self.assertEqual(exp_result, result[self.WARNINGS])
        self.assertEqual(exp_status, result[self.STATUS])
