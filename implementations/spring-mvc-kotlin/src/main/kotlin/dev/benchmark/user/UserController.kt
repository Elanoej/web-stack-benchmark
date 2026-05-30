package dev.benchmark.user

import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/users")
class UserController(
    private val userRepository: UserRepository,
) {
    @GetMapping("/hello")
    fun hello() = mapOf("message" to "ok", "stack" to "spring-mvc-kotlin")

    @GetMapping
    fun findAll(pageable: Pageable): Page<User> {
        return userRepository.findByActiveTrue(pageable)
    }

    @PostMapping("/search")
    fun searchUsers(
        @RequestBody body: SearchRequest,
        pageable: Pageable
    ): Page<User> {
        return userRepository.search(body.name, body.city, pageable)
    }
}

data class SearchRequest(
    val name: String? = null,
    val city: String? = null,
)