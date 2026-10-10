# H17 Run3 implementation amendment v1: inference dtype transcript representation

Date: 2026-10-10. Status: reviewed, accepted before implementation closure/H0/fresh streams.
Authority: owner execution instruction "다음 작업 이어서 실행"; decision:h17-run3-open.
Scope: one serialization representation required to implement the frozen native call.
No criterion, controller-state, arm, array-key/dtype/shape, typed-tag, seed or stage-gate change.

## Frozen basis and discovered gap

Immutable v3 FINAL source_doc d528fa87b2f4f63d2 specifies exactly
Generator(PCG64(INFERENCE_stage)).integers(0,400,size=(5000,400),dtype=np.int64,endpoint=False).
The fixed R0 Archive.tag grammar has no Python class/type tag. Explicit np.int64
is a class-valued keyword; passing it directly into Archive.tag would fail after
a consumed MAIN claim. The original FINAL/schema/specification pins stay byte-identical.

## Exact reviewed representation

Execute the native call with the original kwargs, including dtype=np.int64 and
endpoint=False. Retain original method, positional args, other kwargs, native
returned int64 bytes, and full original generator before/after states unchanged.
For its saved inference call transcript ONLY, copy the kwargs map and encode
the explicit dtype=np.int64 class as the canonical native dtype string '<i8'.
Encode this string with the existing str tag inside the existing typed kwargs
dict. Do not mutate the native-call kwargs object, coerce any other type or
normalize any other generator call. No extra schema key/tag/array is introduced.

The independent verifier requires exactly '<i8' in this inference dtype field,
the frozen method/args/size/endpoint, exactly one outer call, the original PCG64
state transitions, and exact int64 result shape/range/bytes matching the saved
index matrix. A wrong string, missing dtype, changed native result, wrong call
budget, changed endpoint or altered state is INVALID before statistics.
H0 still has no inference generator, call, matrix or bootstrap. Its pure
serialization fixture is evidence-validity only and creates no RNG.

## Review and gates

The independent adversarial reviewer endorsed this narrow representation fix
and required a pure regression that normalization leaves the actual native-call
kwargs unchanged. The source/test review must verify this before pins are closed.
This amendment's exact byte hash enters the stable implementation source closure
before spent H0 and any reserved generator. MAIN pins add matching completed H0
receipts only after H0 verification; no H0/self-pin cycle.

No fresh stream was created or claim consumed for this clarification. Execution
authority remains implementation/review, stable pins, spent H0 then one BENCH.
DEV/EVAL remain owner gated; all nine fixed clauses and stop rules stay unchanged.
Historical H17/hold outcomes and adoption status remain unchanged.
