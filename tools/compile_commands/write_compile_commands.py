"""To get rid of your editor include errors simply run this python script.
write_compile_commands is a tool similar to Hedron Compile Commands.
However it's simpler and made specificaly for 'protoforge'.
This tool works with clangd lsp, maybe with others too."""

import json
import subprocess as sp
from pathlib import Path

WORKSPACE_PATH = (
    Path(__file__).resolve().parents[2]
)  # [2] because main lives in another folder
COMMAND = "bazel aquery 'mnemonic(\"CppCompile\", //main:main)' --output=jsonproto"


def run_bazel_aquery(command) -> dict:
    # runs the aquery command in the terminal
    result = sp.run(command, shell=True, capture_output=True, check=True, text=True)
    # returns a py dictionary with the json result
    return json.loads(result.stdout or result.stderr)


# Format and filter the aquery json for compile_commands.json
def format_bazel_commands(aquery_data: dict) -> list[dict]:
    # compile_commands.json should have source file, directory and commands
    entries = []
    # getting commands
    actions = aquery_data.get("actions", [])
    for act in actions:
        if act.get("mnemonic") != "CppCompile":
            continue
        args = act.get("arguments", [])

        if args is None:
            continue
        command_str = " ".join(args)

        # getting file
        src = None
        for arg in args:
            if arg.endswith((".cc", ".c", "cxx", "cpp", ".C")):
                src = arg
                break
        if src == None:
            continue
        src_path = (WORKSPACE_PATH / src).resolve()

        # getting directory
        directory = str(WORKSPACE_PATH) + "/bazel-protoforge"

        if src and directory and command_str:
            entries.append(
                {"file": str(src_path), "directory": directory, "command": command_str}
            )

    return entries


def write_compile_commands(entries: list[dict]) -> None:
    out_path = WORKSPACE_PATH / "compile_commands.json"
    with out_path.open("w") as f:
        json.dump(entries, f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    aquery_data = run_bazel_aquery(COMMAND)
    entries = format_bazel_commands(aquery_data)
    write_compile_commands(entries)
