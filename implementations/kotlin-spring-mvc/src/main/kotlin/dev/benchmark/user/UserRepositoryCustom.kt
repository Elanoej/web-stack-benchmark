package dev.benchmark.user

import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable

interface UserRepositoryCustom {
    fun search(name: String?, city: String?, pageable: Pageable): Page<User>
}
