#!/bin/zsh
uv run scripts/make_pairs.py && uv run scripts/score_pairs.py --split train
