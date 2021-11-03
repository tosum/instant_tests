# MRJP Instant compiler tests

### Preparation:
* Put `insc_llvm` and `insc_jvm` in this directory

### Run tests
* `python3 test_correct.py`\
   Tests that compiled programs are correct\
   Uses `insc_jvm` and `insc_llvm` to compile the code and runs it

* `python3 test_jvm_limits.py`\
   Checks that `.limit locals` and `.limit stack` are exactly as they it should be\
   Decreases `.limit locals` and `.limit stack` by one and checks that the program crashes

### Error spam
There might be some errors printed during testing, but it's ok.\
As long as testing doesn't stop everything should be ok.

### Tests
 * `examples` - examples provided with the task
 * `other_examples` - some other examples taken from https://github.com/mluszczyk/mrjp-instant/tree/master/examples
 * `random` - random tests generated using `gen_random.py`. No division because it's hard.
