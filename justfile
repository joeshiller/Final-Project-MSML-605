# You can use this if you want!
# Get 'just' from https://github.com/casey/just

# Run some python file in `./src`.
# For example, 'just run bench_similarity' will run 'uv run src/bench_similarity.py'.
run what:
    uv run src/{{what}}.py
