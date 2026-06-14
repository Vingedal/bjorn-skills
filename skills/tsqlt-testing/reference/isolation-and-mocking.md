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

### Restore a specific constraint or trigger onto a fake
```sql
EXEC tSQLt.ApplyConstraint @TableName = 'dbo.OrderLine',   @ConstraintName = 'CK_OrderLine_Qty';
EXEC tSQLt.ApplyTrigger    @TableName = 'dbo.OrderHeader', @TriggerName = 'dbo.tr_OrderHeader_Audit';
```
Use these when the behaviour under test *is* the constraint or trigger.

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

## RemoveObject / RemoveObjectIfExists / UndoTestDoubles
- `RemoveObjectIfExists @ObjectName` — drop an object if present (no error if absent).
- `UndoTestDoubles [@Force]` — restore every faked table / function / spied procedure to the original.
  Rarely needed inside a test (the rollback already restores everything), but useful mid-test when you
  want to switch from the fake back to the real object.
