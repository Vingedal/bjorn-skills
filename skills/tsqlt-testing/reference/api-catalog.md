# tSQLt API catalog

Public tSQLt API signatures (stable across recent 1.x releases). `[brackets]` mark optional parameters.
All objects live in the `tSQLt` schema, e.g. `EXEC tSQLt.FakeTable …`.

## Test class & test management
```
tSQLt.NewTestClass   @ClassName
tSQLt.DropClass      @ClassName
tSQLt.RenameClass    @SchemaName, @NewSchemaName
```
A test class is a schema; a test is a procedure named `[Class].[test …]`; an optional `[Class].SetUp`
procedure runs before each test.

## Running tests
```
tSQLt.RunAll                                          -- run every test class
tSQLt.Run                 [@TestName], [@TestResultFormatter]   -- a class or a single [Class].[test …]
tSQLt.RunTestClass        @TestClassName              -- (alias-style) run one class
tSQLt.RunNew                                          -- run classes created since the last Reset
tSQLt.Reset                                           -- clear the "new test classes" list
tSQLt.RunWithXmlResults   [@TestName]                 -- run + emit JUnit-style XML
tSQLt.RunWithNullResults  [@TestName]                 -- run + suppress output
tSQLt.Info()                                          -- TABLE-valued function: version + environment
```

## Configuration & output
```
tSQLt.SetVerbose          [@Verbose = 1]              -- log each test as it starts/finishes
tSQLt.SetSummaryError     @SummaryError               -- 1 (default) raises an error if any test failed; 0 does not
tSQLt.SetTestResultFormatter @Formatter
tSQLt.DefaultResultFormatter / tSQLt.XmlResultFormatter / tSQLt.NullTestResultFormatter
```

## Assertions — scalars & strings
```
tSQLt.AssertEquals        @Expected (sql_variant), @Actual (sql_variant), [@Message]
tSQLt.AssertNotEquals     @Expected (sql_variant), @Actual (sql_variant), [@Message]
tSQLt.AssertEqualsString  @Expected, @Actual, [@Message]          -- NVARCHAR, NULL-safe
tSQLt.AssertLike          @ExpectedPattern, @Actual, [@Message]   -- SQL LIKE pattern
```

## Assertions — tables & result sets
```
tSQLt.AssertEqualsTable        @Expected, @Actual, [@Message], [@FailMsg]   -- compare row DATA of two tables
tSQLt.AssertEqualsTableSchema  @Expected, @Actual, [@Message]               -- compare column DEFINITIONS
tSQLt.AssertEmptyTable         @TableName, [@Message]
tSQLt.AssertResultSetsHaveSameMetaData @expectedCommand, @actualCommand     -- two query strings (CLR; see gotchas)
```

## Assertions — objects & manual failure
```
tSQLt.AssertObjectExists        @ObjectName, [@Message]
tSQLt.AssertObjectDoesNotExist  @ObjectName, [@Message]
tSQLt.Fail                      [@Message0] … [@Message9]      -- unconditionally fail the test
```

## Expectations (declare BEFORE the code that should raise)
```
tSQLt.ExpectException   [@ExpectedMessage], [@ExpectedSeverity], [@ExpectedState],
                        [@Message], [@ExpectedMessagePattern], [@ExpectedErrorNumber]
tSQLt.ExpectNoException [@Message]
```

## Isolating dependencies (test doubles)
```
tSQLt.FakeTable      @TableName, [@SchemaName], [@Identity], [@ComputedColumns], [@Defaults]
tSQLt.FakeFunction   @FunctionName, @FakeFunctionName, [@FakeDataSource]
tSQLt.SpyProcedure   @ProcedureName, [@CommandToExecute], [@CallOriginal]
tSQLt.ApplyConstraint @TableName, @ConstraintName, [@SchemaName], [@NoCascade]
tSQLt.ApplyTrigger   @TableName, @TriggerName
tSQLt.RemoveObject          @ObjectName, [@NewName OUTPUT], [@IfExists]
tSQLt.RemoveObjectIfExists  @ObjectName, [@NewName OUTPUT]
tSQLt.UndoTestDoubles       [@Force]
```
A spy records each call in a table `<Schema>.<Proc>_SpyProcedureLog` with one column per parameter
(named without the `@`) plus an internal `_id_` column.

`@SchemaName` (on `FakeTable` and `ApplyConstraint`) is a deprecated legacy parameter, kept only for
backward compatibility — pass a two-part `'schema.object'` name instead.

## Annotations
Declared as a comment on the line **immediately above** `CREATE PROCEDURE` (tSQLt reads them from the
stored procedure definition):
```
--[@tSQLt:SkipTest]('reason')                 -- report the test as skipped, never run it
--[@tSQLt:NoTransaction](DEFAULT)             -- run outside tSQLt's rollback transaction
--[@tSQLt:NoTransaction]('Class.CleanupProc') -- ...and run this cleanup procedure afterwards
--[@tSQLt:MinSqlMajorVersion](14)             -- only run on SQL major version >= 14
--[@tSQLt:MaxSqlMajorVersion](15)             -- only run on SQL major version <= 15
--[@tSQLt:RunOnlyOnHostPlatform]('Windows')   -- 'Windows' or 'Linux'
```
