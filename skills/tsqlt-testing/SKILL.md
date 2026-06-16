---
name: tsqlt-testing
description: Author, run, and debug tSQLt unit tests for SQL Server. Use when the user asks to write a SQL unit test, add test coverage for a stored procedure / function / trigger, fake or spy out a dependency (table, function, or procedure), assert on query results, expect an exception, or run a tSQLt suite.
---

# Writing & running tSQLt tests

tSQLt is a unit-testing framework that runs *inside* SQL Server. Tests live in the database alongside the
code they exercise.

## How a tSQLt test is structured
- A **test class is a schema**, created once per file: `EXEC tSQLt.NewTestClass '<ClassName>';`
- A **test is a stored procedure** named `[<ClassName>].[test <description>]` — the `test ` prefix is required.
- Each test runs inside a **transaction that tSQLt rolls back** automatically: tests never persist data and
  need no teardown.
- An optional `[<ClassName>].SetUp` procedure runs before **every** test in the class.
- Structure each test Assemble → Act → Assert (AAA).

## The loop (do this every time)
1. **Find or create the test class.** A new class is a new file `<Name>Tests.class.sql` that starts with
   `EXEC tSQLt.NewTestClass '<Name>Tests';` then `GO`.
2. **Write the test procedure** with `CREATE PROCEDURE <Class>.[test ...]` and AAA comments.
3. **Isolate dependencies** so the test exercises only the code under test:
   - `tSQLt.FakeTable` — replace a table with an empty, constraint-free copy you populate yourself.
   - `tSQLt.FakeFunction` — replace a function with a fake of the same signature.
   - `tSQLt.SpyProcedure` — replace a procedure with a logging stub (optionally still call the original).
   See `reference/isolation-and-mocking.md`.
4. **Assert** with the right assertion (`reference/assertions.md`). Most common: `AssertEquals` (scalars),
   `AssertEqualsTable` (row data), `ExpectException` (errors).

Then deploy the class and run it (`EXEC tSQLt.Run '<Class>'` / `EXEC tSQLt.RunAll`) — see
`reference/running-and-results.md`. Use whatever deploy/run tooling the project provides; check its README
or `CLAUDE.md`. Iterate until green.

Two habits that keep tests honest:
- **Write to the spec, not the code.** Assert what the test's name promises (the requirement). A correct
  test that fails is revealing a bug — don't soften it to match buggy code. See `reference/test-conventions.md`.
- **Fake minimally.** Insert only the columns the behaviour reads (a single key column is often enough to
  materialise a row), and fake only the tables/procedures the code touches. See `reference/isolation-and-mocking.md`.

## A complete example
```sql
EXEC tSQLt.NewTestClass 'MyTests';
GO
CREATE PROCEDURE MyTests.[test total sums the order lines]
AS
BEGIN
    -- Assemble: isolate the table and insert only what the test needs.
    EXEC tSQLt.FakeTable @TableName = 'dbo.OrderLine';
    INSERT INTO dbo.OrderLine (OrderId, Sku, Qty, UnitPrice)
    VALUES (1, 'A', 2, 10.00), (1, 'B', 1, 5.00);

    -- Act
    DECLARE @Total DECIMAL(18, 2) = dbo.fn_OrderTotal(1);

    -- Assert (expected value is a typed variable, NOT an inline CAST - see gotchas)
    DECLARE @Expected DECIMAL(18, 2) = 25.00;
    EXEC tSQLt.AssertEquals @Expected = @Expected, @Actual = @Total;
END;
GO
```

## Critical gotchas (full list in reference/gotchas.md)
- **`EXEC` arguments must be literals or variables — never expressions.** `@Actual = CAST(x AS …)`,
  `@Actual = CASE … END`, and `@Actual = @@TRANCOUNT` are **syntax errors**. `DECLARE` a variable first.
- **Match types in `AssertEquals`** — it compares `sql_variant`; make the expected value the same type as
  the actual (e.g. both `DECIMAL(18,2)`).
- **`FakeTable` makes every column nullable and drops identity/defaults/constraints/triggers/FKs.** Pass
  `@Identity = 1`, `@Defaults = 1`, `@ComputedColumns = 1` to keep those; use `ApplyConstraint` /
  `ApplyTrigger` to restore a specific one.
- **DDL in a test** (or anything that must outlive the rollback) needs the `--[@tSQLt:NoTransaction]` annotation.
- **Nested `tSQLt.Run` inside a test** (to inspect a deliberately failing inner test) should pass
  `@TestResultFormatter = 'tSQLt.NullTestResultFormatter'` so the inner summary error doesn't bubble up.
- **`AssertResultSetsHaveSameMetaData` is CLR-based** and can fail on some hosts with an "LCID 8192 is not
  supported" locale error; SQL-based assertions are unaffected. See `reference/gotchas.md`.

## Reference
- `reference/api-catalog.md` — every public procedure/function, grouped, with signatures.
- `reference/test-conventions.md` — classes, naming, SetUp, the AAA pattern, boundary testing, writing to the spec.
- `reference/assertions.md` — each assertion and when to use it.
- `reference/isolation-and-mocking.md` — FakeTable, FakeFunction, SpyProcedure, ApplyConstraint, ApplyTrigger.
- `reference/running-and-results.md` — Run / RunAll / RunTestClass / RunNew and result formatters.
- `reference/gotchas.md` — the full list of traps and how to avoid them.

tSQLt's own test suite (the `Tests/` folder in the tSQLt source repository) is an authoritative source of
idiomatic usage.
