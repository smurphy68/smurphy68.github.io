import os
def check_routines():
    with open("routines/__init__.py", "r") as _routines:
        current_routines_in_init =_routines.readlines()
        current_routines_in_init = [r.split(" ")[1].lstrip(".") for r in current_routines_in_init if r != "\n" and "#" not in r]
    files = os.listdir("routines")
    stored_routines_in_file = [os.path.splitext(file)[0].split(".")[0] for file in files if file.endswith(".py") and file != "__init__.py" and file != "open_ai_secrets.py"]
    print("[LOADING] Routines being compared")

    if all([r in current_routines_in_init for r in stored_routines_in_file]):
        print("[EVENT] All routines loaded")
    else:
        not_in_init = set(stored_routines_in_file) - set(current_routines_in_init)
        print(f"[EVENT] {len(not_in_init)} routines not loaded: {', '.join(not_in_init)}")
        with open("routines/__init__.py", "a") as file:
            for r in not_in_init:
                file.write(f"from .{r} import *" + '\n')

def add_new_function():
    message = "This is the add new function function"
    print(message)
    return message

## Uncomment for when manually updating routine dependencies
# check_routines()

if __name__ == "__main__":
    add_new_function()