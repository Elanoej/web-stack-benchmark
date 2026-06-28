package dev.benchmark.user

import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import java.util.*

interface UserRepository : JpaRepository<User, UUID>, UserRepositoryCustom {
    fun findByActiveTrue(pageable: Pageable): Page<User>
}