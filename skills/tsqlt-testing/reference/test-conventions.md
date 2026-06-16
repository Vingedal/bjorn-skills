# Test conventions

## Test class = schema
Create the class once at the top of its file, then `GO`:
```sql
EXEC tSQLt.NewTestClass 'CustomerTests';
GO
```
`NewTestClass` drops and recreates the schema, so re-deploying a test file is idempotent.
Put one class per file; a common convention is one `*.class.sql` file per class (e.g. `CustomerTests.class.sql`).

## Test = stored procedure named `test …`
```sql
CREATE PROCEDURE CustomerTests.[test a preferred customer gets the loyalty discount]
AS
BEGIN
    ...
END;
GO
```
- The name must begin with `test` (case-insensitive). Use a readable sentence in `[brackets]`.
- Only procedures whose name starts with `test` are executed as tests; helper procedures/functions in the
  same schema are ignored by the runner (handy for shared fakes).

## SetUp (runs before every test in the class)
```sql
CREATE PROCEDURE CustomerTests.SetUp
AS
BEGIN
    EXEC tSQLt.FakeTable @TableName = 'dbo.Customer';
    INSERT INTO dbo.Customer (CustomerId, Name) VALUES (1, N'Seed');
END;
GO
```
There is **no** teardown procedure: every test (and its `SetUp`) runs in a transaction that tSQLt rolls
back, so each test starts from a clean state automatically.

## Assemble / Act / Assert
Keep tests in three clear phases:
1. **Assemble** — fake the dependencies and insert just the rows the test needs.
2. **Act** — call the one thing under test (a function, a procedure, an insert that fires a trigger).
3. **Assert** — one logical expectation (a scalar, a table, or an exception).

## Isolation mindset
A good tSQLt test depends on as little of the schema as possible. Fake every table the code touches and
insert only the relevant columns/rows; fake or spy functions and procedures the code calls. This makes
tests fast, order-independent, and immune to unrelated schema changes. See `isolation-and-mocking.md`.

## Test the boundaries
When the code under test has a threshold or a range, test the **edge**, not just the middle. For an
inequality, place rows just-outside, exactly-on, and just-inside each limit and assert which side each
falls on. Rows that are only far-inside / far-outside can't tell `<` from `<=`:
```sql
-- rectangle filter keeps 0 < X < 10 (strict). One row per side of the boundary:
INSERT INTO dbo.Particle (Id, X, Y) VALUES
    (1, -0.01, 5), (2,  0.00, 5), (3,  0.01, 5),   -- of these, only Id 3 (just inside) should match
    (4,  9.99, 5), (5, 10.00, 5), (6, 10.01, 5);   -- of these, only Id 4 (just inside) should match
```
The on-the-edge rows (Id 2 and 5) are exactly what catch an off-by-one (`>` mistakenly written `>=`).

## Write tests to the contract, not the code
A test's name is its specification — assert the behaviour the name promises, taken from the requirement,
**not** from reading the current implementation. If the code is wrong, a correct test *should* fail: that
failure is the test doing its job and surfacing a bug. Never soften an assertion to make a known-buggy
result pass.
```sql
-- Requirement: "ready for experimentation if 2 particles"
--   => assert ready = 1 with two particles, even though the code currently requires > 2.
DECLARE @Expected BIT = 1;
EXEC tSQLt.AssertEquals @Expected = @Expected, @Actual = @Ready;  -- fails until the > 2 bug is fixed
```

## Naming
- Test classes: `<Area>Tests` (e.g. `FakeTableTests`, `OrderTests`).
- One class per file, conventionally named `<Area>Tests.class.sql`.
- Keep the code under test and the test classes in separate schemas.

## Organizing a class file
If you keep many tests in one class file, make the structure **uniform**: e.g. the same banner comment
before *every* test (naming the object under test), or none at all. A banner before only some tests reads
as an accident. Some teams instead keep **one object per file** (each test its own `.sql` with a standard
`USE` / `SET`-options header) under source control — follow whatever layout the project already uses.
