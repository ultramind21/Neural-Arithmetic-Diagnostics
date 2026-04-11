from . import test_env, test_rules, test_teacher


def test_env_smoke():
    test_env.run_tests()


def test_rules_smoke():
    test_rules.run_tests()


def test_teacher_smoke():
    test_teacher.run_tests()
