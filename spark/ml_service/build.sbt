//scalaVersion := "2.13.12"
//name := "ml_service"
//organization := "ml.konsin1988"
//version := "1.0.0"
//
//libraryDependencies ++= Seq(
//    // "com.clickhouse" % "clickhouse-jdbc" % "0.6.0" classifier "all",
//    "com.clickhouse" % "clickhouse-jdbc" % "0.6.0",
//    "org.apache.spark" %% "spark-core" % "3.5.0",
//    "org.apache.spark" %% "spark-sql" % "3.5.0",
//    "org.scala-lang.modules" %% "scala-parser-combinators" % "2.3.0",
//    "com.clickhouse.spark" % "clickhouse-spark-runtime-3.5_2.13" % "0.8.1"
//)

ThisBuild / scalaVersion := "2.13.12" 

lazy val root = (project in file("."))
  .settings(
    name := "ml_service",
    version := "1.0.0",

    Compile / mainClass := Some("com.konsin1988.Main"),

    // чтобы избежать конфликтов "deduplicate"
    assembly / assemblyMergeStrategy := {
	case PathList("META-INF", "services", xs @ _*) => MergeStrategy.concat
	case PathList("META-INF", _ @ _*) => MergeStrategy.discard
	case _ => MergeStrategy.first
    },

    libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "3.5.0" % Provided,
	"org.apache.spark" %% "spark-sql"  % "3.5.0" % Provided,

	"com.clickhouse" % "clickhouse-jdbc" % "0.8.1",
	"com.clickhouse.spark" %% "clickhouse-spark-runtime-3.5" % "0.8.1",
	"org.scala-lang.modules" %% "scala-parser-combinators" % "2.3.0"
	//"io.github.cdimascio" % "java-dotenv" % "5.2.2"
    )
  )

