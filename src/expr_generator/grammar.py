from hypothesis import strategies as st


def constant():
    return st.text(
        alphabet=st.characters(min_codepoint=ord("0"), max_codepoint=ord("9")),
        min_size=1,
        max_size=5,
    )


def expr():
    base = constant()

    def extend_expression(children):
        factor = st.one_of(
            constant(),
            children.map(lambda e: f"({e})"),
        )

        term = st.builds(
            lambda first, rest: first + "".join(op + f for op, f in rest),
            factor,
            st.lists(
                st.tuples(st.sampled_from(["*", "/"]), factor),
                min_size=0,
                max_size=3,
            ),
        )

        expression = st.builds(
            lambda first, rest: first + "".join(op + t for op, t in rest),
            term,
            st.lists(
                st.tuples(st.sampled_from(["+", "-"]), term),
                min_size=0,
                max_size=3,
            ),
        )

        return expression

    return st.recursive(
        base,
        extend_expression,
        max_leaves=10,
    )