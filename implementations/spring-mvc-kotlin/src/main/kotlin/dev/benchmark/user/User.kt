package dev.benchmark.user

import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table
import java.util.UUID
import java.time.Instant

@Entity
@Table(name = "users")
data class User(
    @Id
    val id: UUID = UUID.randomUUID(),
    val name: String,
    val email: String,
    val city: String,
    val country: String,
    val age: Int,
    val active: Boolean = true,
    val createdAt: Instant = Instant.now(),
)