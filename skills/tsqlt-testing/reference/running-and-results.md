# Running tests & reading results

## Running (T-SQL)
```sql
EXEC tSQLt.RunAll;                          -- every test class in the database
EXEC tSQLt.Run 'MyTests';                   -- one class
EXEC tSQLt.Run 'MyTests.[test something]';  -- a single test
EXEC tSQLt.RunNew;                          -- classes created since the last EXEC tSQLt.Reset
EXEC tSQLt.RunWithXmlResults;               -- re-run the LAST run, emitting JUnit-style XML
```
Run these through whatever tooling the project uses — `sqlcmd`, SSMS, an MCP SQL server, or CI. Projects
usually wrap deploy + run in a script; check the project's README / `CLAUDE.md`.

To get JUnit-style XML for ALL tests (note `RunWithXmlResults` only re-runs the last target), run first,
then format the stored results:
```sql
EXEC tSQLt.RunAll;
EXEC tSQLt.XmlResultFormatter;
```

## Reading results
After a run, results live in `tSQLt.TestResult`:
```sql
SELECT Class, TestCase, Result, Msg FROM tSQLt.TestResult ORDER BY Class, TestCase;
```
`Result` is one of `Success`, `Failure` (an assertion failed), `Error` (an unexpected exception), or
`Skipped` (a `SkipTest`/version/platform annotation). The text summary at the end of a run reports
`N executed, S succeeded, K skipped, F failed, E errored`.

- A **Failure** means an assertion did not hold — the message shows expected vs actual.
- An **Error** means the test threw something it did not expect (often a real bug in the code under test,
  or a missing fake). Read `Msg` for the SQL error.
- `EXEC tSQLt.SetSummaryError 0` makes a run report success even if tests failed (occasionally useful in
  tooling); the default is `1`.

## Result formatters
`tSQLt.DefaultResultFormatter` prints the text summary; `tSQLt.XmlResultFormatter` produces JUnit-style XML;
`tSQLt.NullTestResultFormatter` produces nothing. Pass a formatter to a single run with
`EXEC tSQLt.Run @TestName = '…', @TestResultFormatter = 'tSQLt.NullTestResultFormatter';`.
