package dev.benchmark.user

import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import java.util.*

interface UserRepository: JpaRepository<User, UUID> {
    fun findByActiveTrue(pageable: Pageable): Page<User>

    @Query(value = """
        SELECT * FROM users
        WHERE (:name IS NULL OR name ILIKE CONCAT('%', :name, '%'))
        AND (:city IS NULL OR city ILIKE CONCAT('%', :city, '%'))
        AND active = true
        """,
        countQuery = """
        SELECT count(*) FROM users
        WHERE (:name IS NULL OR name ILIKE CONCAT('%', :name, '%'))
        AND (:city IS NULL OR city ILIKE CONCAT('%', :city, '%'))
        AND active = true
        """,
        nativeQuery = true)
    fun search(
        @Param("name") name: String?,
        @Param("city") city: String?,
        pageable: Pageable
    ): Page<User>
}