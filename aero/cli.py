import sys
import argparse
from .compiler import compile_file
from .vm import VirtualMachine

def main():
    parser = argparse.ArgumentParser(description="Aero Language Compiler & Runtime")
    parser.add_argument("file", help="Aero source file (.aero)")
    args = parser.parse_args()

    try:
        ast = compile_file(args.file)
        vm = VirtualMachine()
        vm.execute(ast)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
