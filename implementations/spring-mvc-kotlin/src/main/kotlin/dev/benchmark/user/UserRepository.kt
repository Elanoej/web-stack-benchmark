package dev.benchmark.user

import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import java.util.*

interface UserRepository: JpaRepository<User, UUID> {
    fun findByActiveTrue(pageable: Pageable): Page<User>

    @Query("""
        SELECT u
        FROM User u
        WHERE LOWER(u.name) LIKE LOWER(CONCAT('%', COALESCE(:name, ''), '%'))
        AND LOWER(u.city) LIKE LOWER(CONCAT('%', COALESCE(:city, ''), '%'))
        AND u.active = true
    """)
    fun search(
        @Param("name") name: String?,
        @Param("city") city: String?,
        pageable: Pageable
    ): Page<User>
}