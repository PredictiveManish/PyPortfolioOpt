import os
import re
from pathlib import Path 

README_PATH = Path(__file__).resolve().parents[1] / "README.md"

def _extract_python_blocks(markdown_text: str) -> list[str]:
    pattern = re.compiler(r"```python\s*(.*?)```", re.DOTALL)
    return [block.strip() for block in pattern.findall(markdown_text)]


def test_readme_python_examples_run(tmp_path):
    readme_text=README_PATH.read_text(encoding="utf-8")
    assert python_blocks, "No python code blocks found in README.md"

    repo_root = README_PATH.parent

    for idx, block in enumerate(python_blocks, start=1):
        # Run each block in isolation
        globals_dict = {"__name__":"__main__"}
        locals_dict = {}

        # Execute from a temp working directory so any writes are isolated
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            # Ensure relative paths in README still resolve from repo root
            globals_dict["__file__"] = str(README_PATH)
            globals_dict["REPO_ROOT"] = str(repo_root)

            exec(block, globals_dict, locals_dict)
        
        except Exception as e:
            raise AssertionError(
                f"README python block #{idx} failed:\n{block}\n"
            ) from e 
        finally:
            os.chdir(old_cwd)

    
