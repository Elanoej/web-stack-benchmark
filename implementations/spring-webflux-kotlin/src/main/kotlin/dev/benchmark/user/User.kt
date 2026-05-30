package dev.benchmark.user

import org.springframework.data.annotation.Id
import org.springframework.data.relational.core.mapping.Table
import java.util.UUID
import java.time.Instant

@Table("users")
data class User(

    @Id
    val id: UUID? = null,
    val name: String,
    val email: String,
    val city: String,
    val country: String,
    val age: Int,
    val active: Boolean = true,
    val createdAt: Instant = Instant.now(),
)