from hypothesis import given
from expr_generator.grammar import expr

@given(expr())
def test_print(expr: str):
    print(expr)