# Assertions — which one to use

## Scalars
- **`AssertEquals @Expected, @Actual, [@Message]`** — equality of two scalar values (`sql_variant`);
  two `NULL`s count as equal. Make the expected value the **same type** as the actual (e.g. both
  `DECIMAL(18,2)`) — see gotchas.
  ```sql
  DECLARE @Expected DECIMAL(18,2) = 25.00;
  EXEC tSQLt.AssertEquals @Expected = @Expected, @Actual = @Total;
  ```
- **`AssertNotEquals @Expected, @Actual, [@Message]`** — the two values must differ.
- **`AssertEqualsString @Expected, @Actual, [@Message]`** — string compare (`NVARCHAR`) with clearer diff
  output for text. Like `AssertEquals`, it treats two `NULL`s as equal.
- **`AssertLike @ExpectedPattern, @Actual, [@Message]`** — the actual must match a SQL `LIKE` pattern.

**Pick the tightest assertion that matches the intent.** Use `AssertEqualsString` / `AssertEquals` when the
**whole** value is the contract; reach for `AssertLike` only when a substring or shape is genuinely what
matters. Beware over-loose patterns — `AssertLike '%3%'` for "the message mentions 3 particles" also passes
on `'33'` or any stray `3`; prefer the exact message, or a pattern specific enough to mean what you intend.

## Tables and result sets
- **`AssertEqualsTable @Expected, @Actual, [@Message], [@FailMsg]`** — compares the **data** in two tables
  (usually temp tables), ignoring row order. The canonical pattern:
  ```sql
  SELECT col1, col2 INTO #Actual FROM ...;          -- the result under test
  SELECT TOP (0) * INTO #Expected FROM #Actual;      -- same shape, no rows
  INSERT INTO #Expected (col1, col2) VALUES (...);   -- the rows you expect
  EXEC tSQLt.AssertEqualsTable '#Expected', '#Actual';
  ```
- **`AssertEqualsTableSchema @Expected, @Actual, [@Message]`** — compares **column definitions** (names,
  types, nullability), not data. Build `#Expected` to match the contract you expect.
- **`AssertEmptyTable @TableName, [@Message]`** — the table has no rows.
- **`AssertResultSetsHaveSameMetaData @expectedCommand, @actualCommand`** — pass two **query strings**;
  passes when their result-set metadata matches. CLR-based — see the LCID note in `gotchas.md`.

## Objects
- **`AssertObjectExists @ObjectName, [@Message]`** / **`AssertObjectDoesNotExist @ObjectName, [@Message]`**
  — for tables, procedures, functions, constraints, etc.

## Exceptions
- **`ExpectException [@ExpectedMessage], [@ExpectedMessagePattern], [@ExpectedErrorNumber], [@ExpectedSeverity], [@ExpectedState], [@Message]`**
  — call it **before** the code that should throw. Match by exact message, a `LIKE` pattern, and/or the
  error number:
  ```sql
  EXEC tSQLt.ExpectException @ExpectedErrorNumber = 50001;
  EXEC dbo.usp_PlaceOrder @CustomerId = 999, ...;   -- THROW 50001
  ```
  With no parameters it just asserts that *some* exception was raised.
- **`ExpectNoException [@Message]`** — asserts the code that follows runs without raising.

## Manual failure
- **`Fail [@Message0] … [@Message9]`** — unconditionally fails the current test (use inside an `IF`).
