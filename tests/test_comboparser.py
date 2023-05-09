import os

from comboparse import ComboParser

ENV_PREFIX = "PYTESTCOMBOPARSER"


def teardown():
    for key in os.environ:
        if key.startswith(ENV_PREFIX):
            del (os.environ[key])


def test_official_pydocs_example_parser():
    parser = ComboParser(env_prefix=ENV_PREFIX)

    os.environ[parser.create_env_var_name("filename")] = "test.py"
    os.environ[parser.create_env_var_name("count")] = "5"
    os.environ[parser.create_env_var_name("verbose")] = "1"
    os.environ[parser.create_env_var_name("list")] = "1,2,3,4,5"

    parser.add_argument("filename")
    parser.add_argument("-c", "--count", type=int)
    parser.add_argument("-v", "--verbose",
                        action="store_true")
    parser.add_argument("-l", "--list", nargs="+", help="<Required> Set flag",
                        required=True)

    args = parser.parse_args()

    assert args.filename == "test.py"
    assert args.count == 5
    assert args.verbose
    assert len(args.list) == 5
    assert args.list[0] == "1"
    assert args.list[-1] == "5"
    teardown()


def test_action_append():
    parser = ComboParser(env_prefix=ENV_PREFIX)

    os.environ[parser.create_env_var_name("foo")] = "1,2,3"

    parser.add_argument("--foo", action="append")

    args = parser.parse_args()

    assert len(args.foo) == 3
    teardown()


def test_action_append_const():
    parser = ComboParser(env_prefix=ENV_PREFIX)

    os.environ[parser.create_env_var_name("str")] = "1"
    os.environ[parser.create_env_var_name("int")] = "1"

    parser.add_argument('--str', dest='types', action='append_const', const=str)
    parser.add_argument('--int', dest='types', action='append_const', const=int)

    args = parser.parse_args()

    assert len(args.types) == 2
    teardown()


def test_action_count():
    parser = ComboParser(env_prefix=ENV_PREFIX)

    os.environ[parser.create_env_var_name("verbose")] = "3"

    parser.add_argument('--verbose', '-v', action='count', default=0)

    args = parser.parse_args()

    assert args.verbose == 3
    teardown()


def test_action_extend():
    parser = ComboParser(env_prefix=ENV_PREFIX)

    os.environ[parser.create_env_var_name("foo")] = "f1,f2,f3,f4"

    parser.add_argument("--foo", action="extend", nargs="+", type=str)
    parser.parse_args(["--foo", "f1", "--foo", "f2", "f3", "f4"])

    args = parser.parse_args()

    assert len(args.foo) == 4
    teardown()
