package webstackbenchmark

import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import java.sql.PreparedStatement
import java.sql.ResultSet
import java.time.Instant

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

            dataSource.connection.use { conn ->
                conn.autoCommit = true
                conn.prepareStatement(
                    "SELECT id, name, email, city, country, age, active, created_at " +
                    "FROM users WHERE active = true ORDER BY created_at DESC LIMIT ? OFFSET ?"
                ).use { stmt ->
                    stmt.setInt(1, size)
                    stmt.setInt(2, page * size)
                    stmt.executeQuery().use { rs ->
                        val list = mutableListOf<User>()
                        while (rs.next()) {
                            list.add(rs.toUser())
                        }
                        call.respond(list)
                    }
                }
            }
        }

        post("/users/search") {
            val body = call.receive<SearchRequest>()
            val page = call.request.queryParameters["page"]?.toIntOrNull() ?: 0
            var size = call.request.queryParameters["size"]?.toIntOrNull() ?: 20
            if (size < 1) size = 20
            if (size > 100) size = 100

            dataSource.connection.use { conn ->
                conn.autoCommit = true
                val conditions = mutableListOf<String>()
                val params = mutableListOf<Any>()

                if (!body.name.isNullOrBlank()) {
                    conditions.add("name ILIKE CONCAT('%', ?, '%')")
                    params.add(body.name)
                }
                if (!body.city.isNullOrBlank()) {
                    conditions.add("city ILIKE CONCAT('%', ?, '%')")
                    params.add(body.city)
                }

                val whereClause = if (conditions.isNotEmpty()) " AND ${conditions.joinToString(" AND ")}" else ""
                val sql =
                    "SELECT id, name, email, city, country, age, active, created_at " +
                    "FROM users WHERE active = true$whereClause ORDER BY created_at DESC LIMIT ? OFFSET ?"

                params.add(size)
                params.add(page * size)

                conn.prepareStatement(sql).use { stmt ->
                    stmt.bindParams(params)
                    stmt.executeQuery().use { rs ->
                        val list = mutableListOf<User>()
                        while (rs.next()) {
                            list.add(rs.toUser())
                        }
                        call.respond(list)
                    }
                }
            }
        }
    }
}

private fun ResultSet.toUser(): User = User(
    id = getString("id"),
    name = getString("name"),
    email = getString("email"),
    city = getString("city"),
    country = getString("country"),
    age = getInt("age"),
    active = getBoolean("active"),
    createdAt = getTimestamp("created_at").toInstant(),
)

private fun PreparedStatement.bindParams(params: List<Any>) {
    params.forEachIndexed { index, param ->
        when (param) {
            is String -> setString(index + 1, param)
            is Int -> setInt(index + 1, param)
            is Long -> setLong(index + 1, param)
            else -> setObject(index + 1, param)
        }
    }
}
