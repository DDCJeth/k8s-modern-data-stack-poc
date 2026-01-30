import org.apache.spark.sql.SparkSession

object CreateIcebergTables {

  def main(args: Array[String]): Unit = {
    if (args.length < 4) {
      System.err.println("Usage: CreateIcebergTables <inputPath> <catalog> <database> <table> [partitionExpr]")
      System.exit(1)
    }

    val inputPath = args(0)
    val catalog   = args(1)
    val database  = args(2)
    val table     = args(3)
    val partitionExprOpt = if (args.length >= 5) Some(args(4)) else None

    val spark = SparkSession.builder()
      .appName("Create Iceberg Tables")
      .getOrCreate()

    // Read header only to get column names
    val df = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(inputPath)

    val fields = (df.columns.toSeq :+ "ingestion_date").distinct

    val ddl = Configs.generateIcebergDDL(catalog, database, table, fields, partitionExprOpt)

    println(s"Executing DDL for $catalog.$database.$table:\n$ddl")

    // Ensure namespace exists (catalog qualified)
    spark.sql(s"CREATE NAMESPACE IF NOT EXISTS $catalog.$database")

    // Execute DDL
    spark.sql(ddl)

    println(s"Table created (if not existed): $catalog.$database.$table")

    spark.stop()
  }
}