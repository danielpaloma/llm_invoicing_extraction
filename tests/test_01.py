import time

def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

def factorial(n: int) -> int:
    """Compute factorial recursively."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return 1 if n in (0, 1) else n * factorial(n - 1)

def main():
    # Variables to watch in debugger
    names = ["Alice", "Bob", "Charlie"]
    results = {}

    for name in names:
        msg = greet(name)
        print(msg)
        time.sleep(0.5)  # good place to test "step over" vs "step into"
        results[name] = factorial(len(name))  # factorial based on name length

    print("Results dictionary:", results)

    # Trigger an exception to test error breakpoints
    try:
        factorial(-1)
    except ValueError as e:
        print("Caught an error:", e)

if __name__ == "__main__":
    main()
