package dev.benchmark.user

import kotlinx.coroutines.flow.Flow
import org.springframework.data.r2dbc.repository.Query
import org.springframework.data.repository.kotlin.CoroutineCrudRepository
import org.springframework.data.repository.query.Param
import java.util.*

interface UserRepository: CoroutineCrudRepository<User, UUID> {
    @Query("""
        SELECT * FROM users
        WHERE active = true
        AND (:name IS NULL OR LOWER(name) LIKE LOWER(CONCAT('%', :name, '%')))
        AND (:city IS NULL OR LOWER(city) LIKE LOWER(CONCAT('%', :city, '%')))
        LIMIT :limit OFFSET :offset
    """)
    fun search(
        @Param("name") name: String?,
        @Param("city") city: String?,
        limit: Int,
        offset: Int
    ): Flow<User>
}