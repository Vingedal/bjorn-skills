# Isolating dependencies (test doubles)

## FakeTable — replace a table with an empty, unconstrained copy
```sql
EXEC tSQLt.FakeTable @TableName = 'dbo.OrderLine';
```
The fake keeps the column names but:
- makes **every column nullable**, and
- drops the **identity**, **defaults**, **CHECK/UNIQUE/PK/FK constraints**, and **triggers**.

So you can insert only the columns your test cares about. Keep specific behaviour with flags:
```sql
EXEC tSQLt.FakeTable @TableName = 'dbo.OrderHeader', @Identity = 1, @Defaults = 1, @ComputedColumns = 1;
```
- `@Identity = 1` — keep the IDENTITY column (needed if the code relies on `SCOPE_IDENTITY()`).
- `@Defaults = 1` — keep DEFAULT constraints.
- `@ComputedColumns = 1` — keep computed columns.

### Insert only the columns the behaviour reads
Because the fake makes every column nullable, insert **only the columns the code under test actually
reads** — not every column the real table requires. Irrelevant values add noise and falsely imply they
matter. To merely materialise "a row exists" (e.g. for a `COUNT`), insert a single column such as the key:
```sql
-- GOOD: this function only counts rows, so Id alone is enough
EXEC tSQLt.FakeTable @TableName = 'dbo.Particle';
INSERT INTO dbo.Particle (Id) VALUES (1), (2);

-- NOISY: X, Y, Value, ColorId are NOT NULL in the real table, but the count
-- ignores them and the fake made them nullable — leave them out:
-- INSERT INTO dbo.Particle (Id, X, Y, Value, ColorId) VALUES (1, 0, 0, N'?', 1), ...;
```

### Restore a specific constraint or trigger onto a fake
```sql
EXEC tSQLt.ApplyConstraint @TableName = 'dbo.OrderLine',   @ConstraintName = 'CK_OrderLine_Qty';
EXEC tSQLt.ApplyTrigger    @TableName = 'dbo.OrderHeader', @TriggerName = 'dbo.tr_OrderHeader_Audit';
```
Use these when the behaviour under test *is* the constraint or trigger.

#### Worked example: testing a foreign key
Fake both tables, re-apply the FK on the child, then drive inserts that violate / satisfy it. Re-applying
the FK alone is enough — you do **not** need to re-apply the parent's primary key:
```sql
-- "a colour that isn't in Color is rejected"
EXEC tSQLt.FakeTable @TableName = 'dbo.Particle';
EXEC tSQLt.FakeTable @TableName = 'dbo.Color';        -- referenced table, left empty
EXEC tSQLt.ApplyConstraint @TableName = 'dbo.Particle', @ConstraintName = 'FK_ParticleColor';

EXEC tSQLt.ExpectException @ExpectedMessagePattern = '%FK_ParticleColor%';
INSERT INTO dbo.Particle (ColorId) VALUES (7);        -- no Color row 7 -> violation
```
For the happy path, seed the parent key first and assert nothing is raised:
```sql
INSERT INTO dbo.Color (Id) VALUES (7);
EXEC tSQLt.ExpectNoException;
INSERT INTO dbo.Particle (ColorId) VALUES (7);
```
Matching the constraint name (`'%FK_ParticleColor%'`) proves *that* FK fired; a bare
`@ExpectedErrorNumber = 547` would accept any foreign-key violation.

## FakeFunction — replace a function with a fake of the same signature
Create a fake with a compatible signature, then swap it in:
```sql
EXEC ('CREATE FUNCTION MyTests.AlwaysPreferred(@CustomerId INT) RETURNS BIT AS BEGIN RETURN 1; END;');
EXEC tSQLt.FakeFunction @FunctionName = 'dbo.fn_IsPreferredCustomer',
                        @FakeFunctionName = 'MyTests.AlwaysPreferred';
```
After this, every caller of `dbo.fn_IsPreferredCustomer` uses the fake for the rest of the test.
The function being faked must **not** be `WITH SCHEMABINDING` (and neither should its callers, for the
swap to take effect).

## SpyProcedure — record calls (and optionally run the original)
```sql
EXEC tSQLt.SpyProcedure @ProcedureName = 'dbo.usp_SendConfirmation';
```
The procedure is replaced by a stub that **logs every call** to
`dbo.usp_SendConfirmation_SpyProcedureLog` (one column per parameter, named without the `@`, plus
`_id_`). Assert on that log:
```sql
SELECT OrderId, Email INTO #Actual FROM dbo.usp_SendConfirmation_SpyProcedureLog;
...
EXEC tSQLt.AssertEqualsTable '#Expected', '#Actual';
```
Variations:
- `@CallOriginal = 1` — log the call **and** still execute the original body.
- `@CommandToExecute = 'INSERT INTO …'` — run this command instead of the original body (it can reference
  the original parameters).

Because the stub **replaces the body**, spying also neutralises side effects: a procedure that would
otherwise send email, call out over HTTP, or `RAISERROR` becomes a harmless logger, so a test can safely
assert it was — or wasn't — called.
```sql
-- not called: the log is empty
EXEC tSQLt.AssertEmptyTable @TableName = 'dbo.usp_SendConfirmation_SpyProcedureLog';

-- called exactly once (DECLARE first — an EXEC arg can't be a subquery expression)
DECLARE @Calls INT = (SELECT COUNT(*) FROM dbo.usp_SendConfirmation_SpyProcedureLog);
EXEC tSQLt.AssertEquals @Expected = 1, @Actual = @Calls;
```

## RemoveObject / RemoveObjectIfExists / UndoTestDoubles
- `RemoveObjectIfExists @ObjectName` — drop an object if present (no error if absent).
- `UndoTestDoubles [@Force]` — restore every faked table / function / spied procedure to the original.
  Rarely needed inside a test (the rollback already restores everything), but useful mid-test when you
  want to switch from the fake back to the real object.
