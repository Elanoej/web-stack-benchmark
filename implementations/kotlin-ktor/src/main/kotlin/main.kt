package webstackbenchmark

import io.ktor.server.engine.*
import io.ktor.server.netty.*
import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction

fun main() {
    val dbUrl = System.getenv("DATABASE_URL")
        ?: "postgres://bench:bench123@localhost:5432/benchmark?sslmode=disable"
    val port = (System.getenv("PORT") ?: "5000").toInt()

    val config = HikariConfig().apply {
        jdbcUrl = dbUrl
        maximumPoolSize = 30
        minimumIdle = 15
        driverClassName = "org.postgresql.Driver"
        isAutoCommit = false
        transactionIsolation = "TRANSACTION_READ_COMMITTED"
    }
    val dataSource = HikariDataSource(config)

    Database.connect(dataSource)

    transaction {
        SchemaUtils.create(Users)
    }

    embeddedServer(Netty, port = port) {
        configureSerialization()
        configureRouting()
    }.start(wait = true)
}
