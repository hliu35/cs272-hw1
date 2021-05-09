# CS272 HW1

05/09/2021
[Anthony Liu](mailto:hliu35@ucsc.edu)

To run `trec_eval` conveniently on the latest search result, run test.sh with

``` bash
./test.sh
```


**Note**: As I retained the full analytics I used to write my report, please contact my email if you need those experiment results.



To run the codes such as `main.py`, you must
1. Download PyCharm (must use)
2. Build a Docker container with `Dockerfile`.
3. Set this Docker container as PyCharm's Python interpreter (in PyCharm settings)


To run the main program that does the indexing and searching using Lucene
1. Run `main.py` in PyCharm
2. Select Similarity option when prompted
3. Wait for result and the corresponding output file `qhits.ohsu.88-91`. (Expect 1min for each stage)


To examine how I attempted to bypass Lucene for additional flexibility (but failed):
1. Run `custom_ranking.py` by right clicking in PyCharm file list


To modify the searched fields and parsing conditionals, go to `query_builder.py`
