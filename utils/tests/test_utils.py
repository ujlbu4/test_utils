import allure
import pytest

from utils.utils import todict, is_string_belong_language
from utils.constants import Language
from sure import expect, ensure


@allure.feature('framework utils')
@allure.story('todict')
class TestToDictFunction:
    def test_convert_instance_variables(self):
        class TestClass:
            def __init__(self, instance_attribute_variable=2):
                self.instance_attribute_variable = instance_attribute_variable

        json_obj = todict(TestClass(), convert_private=False, include_none_fields=True)
        json_obj.should.have.key("instance_attribute_variable").should.be.equal(2)

    def test_convert_class_attributes(self):
        class TestClass:
            class_attribute_variable = 1

            def __init__(self, instance_attribute_variable=2):
                self.instance_attribute_variable = instance_attribute_variable

        # convert_private=False
        json_obj = todict(TestClass(), convert_private=False, include_none_fields=True)
        json_obj.should.have.key("instance_attribute_variable").should.be.equal(2)
        json_obj.should_not.have.key("class_attribute_variable")

        # convert_private=True
        json_obj = todict(TestClass(), convert_private=True, include_none_fields=True)
        json_obj.should.have.key("instance_attribute_variable").should.be.equal(2)
        json_obj.should_not.have.key("class_attribute_variable")

        # include_class_attrs=True
        json_obj = todict(TestClass(), convert_private=True, include_none_fields=True, include_class_attrs=True)
        json_obj.should.have.key("class_attribute_variable").should.be.equal(1)

    def test_not_convert_callable_methods(self):
        class TestClass:
            class_attribute_variable = 1

            def __init__(self, instance_attribute_variable=2):
                self.instance_attribute_variable = instance_attribute_variable

            def method_a(self):
                pass

        json_obj = todict(TestClass(), convert_private=True, include_none_fields=True, include_class_attrs=True)
        json_obj.should_not.have.key("method_a")

    def test_convert_private_attribute_flag(self):
        class TestClass:
            def __init__(self):
                self.public_variable = 1
                self._private_variable = 2

        # convert_private=True
        json_obj = todict(TestClass(), convert_private=True, include_none_fields=True)
        json_obj.should.have.key("public_variable").should.be.equal(1)
        json_obj.should.have.key("_private_variable").should.be.equal(2)

        # convert_private=False
        json_obj = todict(TestClass(), convert_private=False, include_none_fields=True)
        json_obj.should.have.key("public_variable").should.be.equal(1)
        json_obj.should_not.have.key("_private_variable")

    def test_convert_types(self):
        class TestClass:
            def __init__(self):
                self.variable_int = 1
                self.variable_string = "hello world"
                self.variable_list = [1, 2, 3]
                self.variable_dict = {'a': 1, 'b': 2}
                self.variable_tuple = (1, 2)
                self.variable_boolean = True

        json_obj = todict(TestClass(), convert_private=True, include_none_fields=True)
        json_obj.should.have.key("variable_int").should.be.equal(1)
        json_obj.should.have.key("variable_string").should.be.equal("hello world")
        json_obj.should.have.key("variable_list").should.be.equal([1, 2, 3])
        json_obj.should.have.key("variable_dict").should.be.equal({'a': 1, 'b': 2})
        json_obj.should.have.key("variable_tuple").should.be.equal([1, 2])
        json_obj.should.have.key("variable_boolean").should.be.equal(True)

    def test_convert_inner_objects(self):
        class TestClassA:
            def __init__(self):
                self.var_dict = {'a': 1, 'b': 2}

        class TestClassB:
            def __init__(self, other_obj):
                self.obj_with_inner_obj = other_obj

        json_obj = todict(TestClassB(other_obj=TestClassA()), convert_private=True, include_none_fields=True)
        json_obj.should.have.key("obj_with_inner_obj").which \
            .should.have.key("var_dict").should.be.equal({'a': 1, 'b': 2})

    def test_include_none_fields_flag(self):
        class TestClass:
            def __init__(self):
                self.var_int0 = 0
                self.var_int1 = 1
                self.var_string_empty = ""
                self.var_string = "hello world"
                self.var_list_empty = []
                self.var_list = [1, 2, 3]
                self.var_bool_false = False
                self.var_bool_true = True
                self.var_none = None

        # include_none_fields=True
        json_obj = todict(TestClass(), convert_private=False, include_none_fields=True)
        json_obj.should.have.key("var_int0").should.be.equal(0)
        json_obj.should.have.key("var_int1").should.be.equal(1)
        json_obj.should.have.key("var_string_empty").should.be.equal("")
        json_obj.should.have.key("var_string").should.be.equal("hello world")
        json_obj.should.have.key("var_list_empty").should.be.equal([])
        json_obj.should.have.key("var_list").should.be.equal([1, 2, 3])
        json_obj.should.have.key("var_bool_false").should.be.equal(False)
        json_obj.should.have.key("var_bool_true").should.be.equal(True)
        json_obj.should.have.key("var_none").should.be.equal(None)

        # include_none_fields=False
        json_obj = todict(TestClass(), convert_private=False, include_none_fields=False)
        json_obj.should.have.key("var_int0").should.be.equal(0)
        json_obj.should.have.key("var_int1").should.be.equal(1)
        json_obj.should_not.have.key("var_string_empty")
        json_obj.should.have.key("var_string").should.be.equal("hello world")
        json_obj.should_not.have.key("var_list_empty")
        json_obj.should.have.key("var_list").should.be.equal([1, 2, 3])
        json_obj.should.have.key("var_bool_false").should.be.equal(False)
        json_obj.should.have.key("var_bool_true").should.be.equal(True)
        json_obj.should_not.have.key("var_none")


@pytest.fixture(
    params=[
        {
            'string': 'Терминатор Восстание 2',
            'language': Language.RU,
            'expected': {
                'is_belong': True
            }
        },
        {
            'string': 'Терминатор Восстание 2',
            'language': Language.EN,
            'expected': {
                'is_belong': False
            }
        },
        {
            'string': 'Terminator Rebellion 2',
            'language': Language.EN,
            'expected': {
                'is_belong': True
            }
        },
        {
            'string': 'Terminator Rebellion 2',
            'language': Language.RU,
            'expected': {
                'is_belong': False
            }
        },
        {
            'string': '2pac: Легенда',
            'language': Language.RU,
            'expected': {
                'is_belong': True
            }
        },
    ],
    ids=[
        'string=ru, language=ru, is_belong=true',
        'string=ru, language=en, is_belong=false',
        'string=en, language=en, is_belong=true',
        'string=en, language=ru, is_belong=false',
        'string=ru with few en letters, language=ru, is_belong=true',
    ]
)
def sting_belong_language_fixture(request):
    return request.param


@allure.feature('framework utils')
@allure.story('is_string_belong_language')
class TestFunctionIsStringBelongLanguage:
    def test_is_string_belong_language(self, sting_belong_language_fixture):
        params = sting_belong_language_fixture

        result = is_string_belong_language(string=params['string'], language=params['language'])
        result.should.be.equal(params['expected']['is_belong'])
