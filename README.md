# comboparse

Drop-in replacement for argparse with support for environment variables.

## How does it work

If environment variables are present that fit a certain schema they are internally appended
as if you had added them as CLI arguments.

## Usage

As a drop in replacement just use comboparser instead of argparse:

```python
import comboparse

# notice the different classname its not argparse.ArgumentParser
parser = comboparse.ComboParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('filename')           
parser.add_argument('-c', '--count')      
parser.add_argument('-v', '--verbose',
                    action='store_true') 

args = parser.parse_args()
```

If the environment variables FILENAME, COUNT or VERBOSE (for flags set them with 1, true or y) these
values will be set accordingly

### Prefix environment variables

Obviously for the sake of sanity we might want to prefix our environment variables, simply add
the following parameter to the constructor:

```python
import comboparse

# notice the different classname its not argparse.ArgumentParser
parser = comboparse.ComboParser(
    # ...
    env_prefix="combo", # please note that this will be upper cased
)

# ...
```

and now the env vars from before would be COMBO_FILENAME, COMBO_COUNT, COMBO_VERBOSE

## Limitations

### Environment variable names

The names can't be adjusted beyond setting the prefix and determined by the actions "dest" value.
Aka whatever argparse would determine your "args.NAME" to be like.

### Mixing CLI arguments and environment variables

While this should work as this tool simply adds its own CLI arguments to argparser, if you
do something like

```bash
$ COUNT=10 my-tool --count 5 --verbose
```

The verbose flag will work as expected, but which count is taken isn't guaranteed by thiis library.
(aka while now maybe the environment variable has precedence, in the future this might randomly
change so don't rely on this!)

### Action Type: count

Count actions are usually provided like this:

```bash
$ my-cli-tool -vvv
Namespace(verbose=3)
```

but as an env variable you have to provide the number as is

```bash
$ VERBOSE=3 my-cli-tool
Namespace(verbose=3)
```

### Action Type: append_const

This works a bit like a normal store_true/store_false you have to use 1, true etc.

## License

MIT