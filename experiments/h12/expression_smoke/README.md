# H12 Package E implementation smoke, 2026-09-27

This is a code-path check on the previously spent seed pair `(5, 6)` with 40 rows. It is **not** Package E calibration, development, evaluation, task-readability evidence, or a behavioral verdict. The unmodified raw result is [`h12-expression-smoke/smoke.json`](h12-expression-smoke/smoke.json).

GitHub-hosted Linux [run 36262997039](https://github.com/Vinculums/Fruitfly/actions/runs/36262997039) completed successfully at source commit `1719319b74ef8f9270ec29dfe8b17fcabe22fb14`. The runner used Python 3.11.15 and NumPy 2.4.6. The raw record includes the source and draft-design SHA-256 values.

The checkpoint generator agreed with the historical runner on 22 recorded fields. At silent delay zero, the two cloned module states and 24 read-out fields matched exactly. The D=5000 value matched the zero-input analytic formula with maximum absolute error `3.042011087472929e-14`, and the read-out called the module zero times. These identities establish the exercised implementation path only. They do not establish that the 600-step task is readable or that decay changes choice.
