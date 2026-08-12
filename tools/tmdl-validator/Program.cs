using Microsoft.AnalysisServices.Tabular;

if (args.Length != 1)
{
    Console.Error.WriteLine("Usage: TmdlValidator <definition-folder>");
    return 2;
}

try
{
    var database = TmdlSerializer.DeserializeDatabaseFromFolder(args[0]);
    var model = database.Model;
    var measureCount = model.Tables.Sum(table => table.Measures.Count);

    if (model.Tables.Count == 0 || measureCount == 0 || model.Relationships.Count == 0)
    {
        Console.Error.WriteLine("The model must contain tables, measures, and relationships.");
        return 1;
    }

    Console.WriteLine(
        $"TMDL deserialized by Microsoft TOM: {model.Tables.Count} tables, " +
        $"{measureCount} measures, {model.Relationships.Count} relationships, " +
        $"{model.Roles.Count} role(s)");
    return 0;
}
catch (Exception exception)
{
    Console.Error.WriteLine(exception);
    return 1;
}
