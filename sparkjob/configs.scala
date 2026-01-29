object Configs {

  def inferType(col: String): String = col match {
    case "timestamp"                         => "TIMESTAMP"
    case "ingestion_date"                    => "DATE"

    case c if c.endsWith("_msisdn")           => "STRING"
    case c if c.endsWith("_id")               => "STRING"
    case c if c.endsWith("_type")             => "STRING"
    case c if c.endsWith("_reason")           => "STRING"
    case c if c.endsWith("_status")           => "STRING"
    case c if c == "apn"                      => "STRING"
    case c if c == "region"                   => "STRING"
    case c if c == "cell_id"                  => "STRING"
    case c if c == "province"                 => "STRING"
    case c if c == "technology"               => "STRING"

    case c if c.contains("duration")          => "INT"
    case c if c.contains("bytes")             => "BIGINT"
    case c if c.contains("length")            => "INT"

    case c if c.contains("amount")             => "DECIMAL(10,2)"
    case c if c.contains("latitude")           => "DOUBLE"
    case c if c.contains("longitude")          => "DOUBLE"
    case c if c.contains("capacity")           => "DOUBLE"

    case _                                    => "STRING"
  }

  def generateIcebergDDL(
      catalog: String,
      database: String,
      table: String,
      fields: Seq[String],
      partitionExpr: Option[String] = None
  ): String = {

    val columns = fields
      .map(c => s"  `${c}` ${inferType(c)}")
      .mkString(",\n")

    val partitionClause = partitionExpr
      .map(p => s"\nPARTITIONED BY ($p)")
      .getOrElse("")

    s"""
       |CREATE TABLE IF NOT EXISTS $catalog.$database.$table (
       |$columns
       |)
       |USING iceberg$partitionClause;
       |""".stripMargin
  }

}