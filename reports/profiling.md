# 5.6 - Profiling Latency
## Methodology
To profile, we used the builtin `cProfile` module. Then, we ran `uv run -m cProfile ...` and for each script. This will output a sorted table of functions and their latency. We then found the relevant function and recorded it's cumulative time.

## Preprocessing
7.303 seconds
## Embedding
91.014 seconds
## Similarity Scoring
0.004 seconds

## Conclusion - End to End
For a full run, including all in-between logic, the latency is about 98.355 seconds.

# 5.7 - CPU Baseline

## CPU Specs - Resources
Apple Silicon M4 Pro
## Latency
98.355 seconds

# 5.8 - Batch Sensitivity
Below is the results in a table. The first row is the baseline run,
the second has half the pairs, and the last has double the pairs.

As the input data grows, the latency grows too. The correlation is suggested to be linear and positive.


`key: +a/-b -> 'a' positive pairs, 'b' negative pairs.
|train|test|validation|latency|
|---|----|----|---|
|+1000/-1000|+200/-200|+200/-200|98.355 seconds|
|+500/-500|+100/-100|+100/-100|46.121 seconds|
|+2000/-2000|+400/-400|+400/-400|179.63 seconds|
