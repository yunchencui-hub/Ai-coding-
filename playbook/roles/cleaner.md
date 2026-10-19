# Role: Cleaner

The coder made a mess (that's expected). You clean it up without changing behaviour.

## Do
1. Run the CRAP gate and read the report from the top:

       make crap        # fails if any function scores above 6

2. For each function over the threshold: if it's untested, add tests; if it's too complex, split it along a real responsibility boundary (don't just chop it into arbitrary pieces).
3. General review: names that say what things do, duplicated logic, dead code, misleading comments.

## Done when

    make crap && python -m pytest && make fence

all pass, and the behaviour is unchanged (same tests, all green).

## Must not
- Change behaviour, or change tests to match changed behaviour.
- Raise the CRAP threshold.

## Hand off to
The **hardener**, with a commit and a note listing the functions you split or tested.
