Symptom: ASan reports heap-use-after-free in cache_test.cpp:42 on Windows debug CI.
Evidence: Symbolized ASan stack shows free in Cache::clear and read in Cache::get.
Reproduction: ctest --test-dir build -R cache_test --output-on-failure reproduces with seed 17.
Root cause: Cache::get retained a pointer invalidated by Cache::clear.
Fix: Store stable keys and reacquire values after clear instead of retaining raw pointer.
Verification: ctest --test-dir build -R cache_test --output-on-failure; cmake --build build
Residual risk: TSan not run because this code path is single-threaded.
