package webstackbenchmark

import io.ktor.server.engine.*
import io.ktor.server.netty.*
import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction

val dataSource: HikariDataSource by lazy {
    val dbUrl = System.getenv("DATABASE_URL")
        ?: "postgres://bench:bench123@localhost:5432/benchmark?sslmode=disable"

    HikariConfig().apply {
        jdbcUrl = dbUrl
        maximumPoolSize = 30
        minimumIdle = 15
        driverClassName = "org.postgresql.Driver"
        isAutoCommit = false
        transactionIsolation = "TRANSACTION_READ_COMMITTED"
    }.let { HikariDataSource(it) }
}

fun main() {
    val port = (System.getenv("PORT") ?: "5000").toInt()

    Database.connect(dataSource)

    transaction {
        SchemaUtils.create(Users)
    }

    embeddedServer(Netty, port = port) {
        configureSerialization()
        configureRouting()
    }.start(wait = true)
}
