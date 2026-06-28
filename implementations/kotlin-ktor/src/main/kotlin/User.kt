package webstackbenchmark

import kotlinx.serialization.Contextual
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.javatime.CurrentDateTime
import org.jetbrains.exposed.sql.javatime.datetime
import java.time.Instant

@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
    val city: String,
    val country: String,
    val age: Int,
    val active: Boolean,
    @SerialName("created_at")
    @Contextual
    val createdAt: Instant,
)

@Serializable
data class SearchRequest(
    val name: String? = null,
    val city: String? = null,
)

object Users : Table("users") {
    val id = uuid("id").autoGenerate()
    val name = varchar("name", 100)
    val email = varchar("email", 150)
    val city = varchar("city", 100)
    val country = varchar("country", 100)
    val age = integer("age")
    val active = bool("active").default(true)
    val createdAt = datetime("created_at").defaultExpression(CurrentDateTime)

    override val primaryKey = PrimaryKey(id)
}

fun ResultRow.toUser(): User = User(
    id = this[Users.id].toString(),
    name = this[Users.name],
    email = this[Users.email],
    city = this[Users.city],
    country = this[Users.country],
    age = this[Users.age],
    active = this[Users.active],
    createdAt = this[Users.createdAt].toInstant(java.time.ZoneOffset.UTC),
)
