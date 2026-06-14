# Gotchas (and how to avoid them)

These are the real traps to watch for when writing tSQLt tests.

## 1. EXEC arguments must be a literal or a variable — never an expression
This is a **syntax error**:
```sql
EXEC tSQLt.AssertEquals @Expected = CAST(90.00 AS DECIMAL(18,2)), @Actual = @Net;  -- ERROR
EXEC tSQLt.AssertEquals @Expected = 1, @Actual = CASE WHEN … END;                  -- ERROR
EXEC tSQLt.AssertEquals @Expected = 0, @Actual = @@TRANCOUNT;                       -- ERROR
```
Assign to a `DECLARE`d variable first:
```sql
DECLARE @Expected DECIMAL(18,2) = 90.00;
DECLARE @TranCount INT = @@TRANCOUNT;
EXEC tSQLt.AssertEquals @Expected = @Expected, @Actual = @Net;
```

## 2. AssertEquals compares sql_variant — match the type
`AssertEquals` boxes both sides into `sql_variant`. Compare like with like: make the expected value the
same type as the actual (e.g. both `DECIMAL(18,2)`, both `INT`). A `DECLARE @Expected DECIMAL(18,2) = …`
next to a `DECIMAL(18,2)` actual is the safe habit. (This also dodges gotcha #1.)

## 3. FakeTable strips almost everything
A faked table has **all columns nullable** and **no identity, defaults, computed columns, constraints,
or triggers**. Consequences:
- `SCOPE_IDENTITY()` returns NULL unless you fake with `@Identity = 1`.
- Inserts that relied on a DEFAULT now need an explicit value, or fake with `@Defaults = 1`.
- To test a constraint or trigger, restore it with `ApplyConstraint` / `ApplyTrigger`.

## 4. DDL inside a test needs NoTransaction
Each test runs in a transaction tSQLt rolls back. Some DDL cannot run in that context, and anything you
genuinely want to persist past the test won't. Annotate such a test:
```sql
--[@tSQLt:NoTransaction]('MyTests.CleanUp')   -- provide a cleanup proc since there's no rollback
CREATE PROCEDURE MyTests.[test that does DDL] AS BEGIN … END;
```
Use `(DEFAULT)` if there is nothing to clean up.

## 5. Annotation comment placement
An annotation must be a comment on the line **immediately above** `CREATE PROCEDURE`, with nothing
between them, in the same batch (i.e. right after the preceding `GO`):
```sql
GO
--[@tSQLt:SkipTest]('reason')
CREATE PROCEDURE MyTests.[test …] AS BEGIN … END;
GO
```
(The framework's own tests split the marker as `'--[@'+'tSQLt:SkipTest]'` only so its build doesn't detect
its own annotations — in your test files write the literal `--[@tSQLt:SkipTest](…)`.)

## 6. Nested tSQLt.Run inside a test
To inspect a deliberately failing inner test, run it with the null formatter so its summary error doesn't
propagate and mark your test as errored:
```sql
EXEC tSQLt.Run @TestName = 'InnerDemo.[test …]', @TestResultFormatter = 'tSQLt.NullTestResultFormatter';
SELECT Result FROM tSQLt.TestResult WHERE Class = 'InnerDemo' AND TestCase = 'test …';
```

## 7. AssertResultSetsHaveSameMetaData — possible CLR "LCID 8192" error
This assertion (and tSQLt's other CLR result-set procedures) opens an internal `System.Data.SqlClient`
connection that, on some hosts, fails with *"The locale identifier (LCID) 8192 is not supported by SQL
Server"* — a Windows regional-settings issue in the tSQLt CLR, independent of `SET LANGUAGE`. If you hit it,
annotate that test `SkipTest`; **all SQL-based assertions are unaffected.** Remedies: change the host's
non-Unicode system locale to a standard one, or use a tSQLt build that targets `Microsoft.Data.SqlClient`.

## 8. Spy log table shape
`SpyProcedure 'S.P'` creates `S.P_SpyProcedureLog` with one column per parameter (named without the `@`)
plus an internal `_id_`. `SELECT` only the parameter columns into your `#Actual` so the comparison lines up.

## 9. tSQLt is CLR + dev-only
tSQLt needs CLR enabled and a trusted assembly (handled by `PrepareServer.sql`). Never install it on a
production database.
