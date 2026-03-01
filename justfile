# You can use this if you want!
# Get 'just' from https://github.com/casey/just

# Run some python file in `./scripts`.
# For example, 'just run bench_similarity' will run 'uv run scripts/bench_similarity.py'.
run-script what:
    uv run scripts/{{what}}.py
