"""Drop-in replacement for argparse with support for environment variables."""
import re
import sys
from argparse import ArgumentParser, Namespace, SUPPRESS
from os import getenv
from typing import Optional


class ComboParser(ArgumentParser):
    """Use this instead of argparse.ArgumentParser to also make use of
    environment variables"""
    _env_prefix: str = None

    def __init__(self, env_prefix: str = None, **kwargs):
        """Create a new ComboParser, supports env_prefix option!"""
        super().__init__(**kwargs)
        self._env_prefix = env_prefix

    # pylint: disable=too-many-branches
    def parse_args(self, args=None, namespace: Namespace = None) -> Namespace:
        """Parse arguments (and add environment based values to it)"""
        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)

        pos_index = 0

        # add environment variable values as args
        for action in self._actions:
            if action.dest is not SUPPRESS and action.default is not SUPPRESS:
                value = self._env_var_by_dest(action.dest)

                action_name = type(action).__name__
                is_append_const_action = action_name == "_AppendConstAction"

                # append const actions doesnt use dest for names
                if is_append_const_action:
                    value = self._env_var_by_dest(
                        strip_slashes(action.option_strings[0])
                    )

                if value is None:
                    continue

                is_store_bool_action = False
                is_positional_action = len(action.option_strings) == 0
                is_append_action = action_name == "_AppendAction"
                is_count_action = action_name == "_CountAction"

                if action_name in ["_StoreTrueAction", "_StoreFalseAction"]:
                    is_store_bool_action = True

                if is_count_action:
                    for _ in range(int(value)):
                        args.append(action.option_strings[0])
                    continue

                if not is_positional_action:
                    args.append(action.option_strings[0])

                # store bool type doesnt need value
                if is_store_bool_action or is_append_const_action:
                    continue

                # positional arguments should be at the front
                if is_positional_action:
                    args.insert(pos_index, value)
                    pos_index += 1
                    continue

                # list type argument
                if action.nargs is not None or is_append_action:
                    for index, val in enumerate(value.split(",")):
                        if index != 0 and is_append_action:
                            args.append(action.option_strings[0])
                        args.append(val)
                    continue

                # nothing left just append
                args.append(value)

        return super().parse_args(args=args, namespace=namespace)

    def _env_var_by_dest(self, dest: str) -> Optional[str]:
        return getenv(self.create_env_var_name(dest))

    def create_env_var_name(self, name: str) -> str:
        """Create an environment variable name with prefix if set"""
        prefix = ""

        if self._env_prefix is not None:
            prefix = f"{self._env_prefix.upper()}_"
        return clean_env_name(f"{prefix}{name.upper()}")


def clean_env_name(name: str) -> str:
    """Clean the name of a variable to be an usable environment variable"""
    return re.sub(r"([^a-zA-Z_]+[^a-zA-Z0-9_]*)", "_", name)


def strip_slashes(name: str) -> str:
    """Remove slashes"""
    return name.replace("-", "")
