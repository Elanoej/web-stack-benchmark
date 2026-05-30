package dev.benchmark.user

import kotlinx.coroutines.flow.toList
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/users")
class UserController(
    private val userRepository: UserRepository,
) {

    @GetMapping("/hello")
    suspend fun hello() = mapOf("message" to "ok", "stack" to "spring-webflux-kotlin")

    @GetMapping
    suspend fun findAll(
        @RequestParam("page", defaultValue = "0") page: Int,
        @RequestParam("size", defaultValue = "20") size: Int,
    ): List<User> {
        val offset = page * size
        return this.userRepository.search(null, null, limit = size, offset = offset).toList()
    }

    @PostMapping("/search")
    suspend fun search(
        @RequestBody body: SearchRequest,
        @RequestParam("page", defaultValue = "0") page: Int,
        @RequestParam("size", defaultValue = "20") size: Int,
    ): List<User> {
        val offset = page * size

        return this.userRepository.search(body.name, body.city, limit = size, offset = offset).toList()
    }
}

data class SearchRequest(
    val name: String? = null,
    val city: String? = null,
)