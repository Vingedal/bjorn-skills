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

## Naming
- Test classes: `<Area>Tests` (e.g. `FakeTableTests`, `OrderTests`).
- One class per file, conventionally named `<Area>Tests.class.sql`.
- Keep the code under test and the test classes in separate schemas.
