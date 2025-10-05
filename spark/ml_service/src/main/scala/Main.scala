package com.konsin1988

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Dataset, Row}
import com.clickhouse.jdbc.ClickHouseDriver
import java.util.Properties
import com.clickhouse.spark.ClickHouseCatalog
//import io.github.cdimascio.dotenv.Dotenv

object Main {
  def main(args: Array[String]): Unit = {
    
    val clickhouseHost = sys.env.getOrElse("CLICKHOUSE_HOST", "")
    val clickhousePort = sys.env.getOrElse("CLICKHOUSE_PORT", "")
    val database       = sys.env.getOrElse("CLICKHOUSE_DB", "")
    val user           = sys.env.getOrElse("CLICKHOUSE_USER", "")
    val password       = sys.env.getOrElse("CLICKHOUSE_PASSWORD", "")
    val table          = sys.env.getOrElse("CLICKHOUSE_TABLE", "")

    val spark = SparkSession.builder()
      .appName("ml_service")
      .master("local[*]")
      .config("spark.sql.catalog.clickhouse", "com.clickhouse.spark.ClickHouseCatalog")
      .config("spark.sql.catalog.clickhouse.protocol", "http")
      .config("spark.sql.catalog.clickhouse.host", clickhouseHost)
      .config("spark.sql.catalog.clickhouse.http_port", clickhousePort)
      .config("spark.sql.catalog.clickhouse.user", user)
      .config("spark.sql.catalog.clickhouse.password", password)
      .config("spark.sql.catalog.clickhouse.database", database)
      .config("spark.clickhouse.write.format", "json")
      .getOrCreate()

    val df = spark.sql("select date, total_price from clickhouse.wb_orders.wb_orders")
    df.show()

    // Выводим схему и первые строки
    df.printSchema()
    df.show(20, truncate = false)
    
    val sc = spark.sparkContext
    val data = sc.parallelize(Seq(1, 2, 3, 4, 5))
    val result = data.map(_ * 2).collect()
    println("Результат: " + result.mkString(", "))
    spark.stop()
  }
}

