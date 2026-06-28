package webstackbenchmark

import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction

fun Application.configureRouting() {
    routing {
        get("/hello") {
            call.respond(mapOf("message" to "ok", "stack" to "kotlin-ktor"))
        }

        get("/users") {
            val page = call.request.queryParameters["page"]?.toIntOrNull() ?: 0
            var size = call.request.queryParameters["size"]?.toIntOrNull() ?: 20
            if (size < 1) size = 20
            if (size > 100) size = 100

            val users = transaction {
                Users.selectAll()
                    .where { Users.active eq true }
                    .orderBy(Users.createdAt, SortOrder.DESC)
                    .limit(size)
                    .offset((page * size).toLong())
                    .map { it.toUser() }
            }

            call.respond(users)
        }

        post("/users/search") {
            val body = call.receive<SearchRequest>()
            val page = call.request.queryParameters["page"]?.toIntOrNull() ?: 0
            var size = call.request.queryParameters["size"]?.toIntOrNull() ?: 20
            if (size < 1) size = 20
            if (size > 100) size = 100

            val users = transaction {
                Users.selectAll()
                    .where {
                        val cond = Users.active eq true
                        val withName = if (!body.name.isNullOrBlank()) {
                            cond and (Users.name ilike "%${body.name}%")
                        } else cond
                        val withCity = if (!body.city.isNullOrBlank()) {
                            withName and (Users.city ilike "%${body.city}%")
                        } else withName
                        withCity
                    }
                    .orderBy(Users.createdAt, SortOrder.DESC)
                    .limit(size)
                    .offset((page * size).toLong())
                    .map { it.toUser() }
            }

            call.respond(users)
        }
    }
}

infix fun <T : String?> ExpressionWithColumnType<T>.ilike(pattern: String): Op<Boolean> {
    return object : Op<Boolean>() {
        override fun toQueryBuilder(queryBuilder: QueryBuilder) {
            queryBuilder {
                append(this@ilike)
                append(" ILIKE '${pattern.replace("'", "''")}'")
            }
        }
    }
}
