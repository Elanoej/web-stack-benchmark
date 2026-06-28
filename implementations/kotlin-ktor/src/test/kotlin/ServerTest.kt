package webstackbenchmark

import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.testing.*
import kotlinx.serialization.json.Json
import kotlin.test.*

class ServerTest {

    @Test
    fun `test hello endpoint`() = testApplication {
        application {
            configureSerialization()
            configureRouting()
        }
        val response = client.get("/hello")
        assertEquals(HttpStatusCode.OK, response.status)
        val body = Json.decodeFromString<Map<String, String>>(response.bodyAsText())
        assertEquals("ok", body["message"])
        assertEquals("kotlin-ktor", body["stack"])
    }
}
