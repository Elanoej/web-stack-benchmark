import http from "k6/http"
import { check, sleep } from "k6"
import { BASE_URL, tresholds } from "../config.js"

export const options = {
    // Cenário: 50 usuários simultâneos por 30 segundos
    vus: 50,
    duration: "30s",
    tresholds,
}

export default function() {
    // Testa os três endpoints em sequência
    // simula um usuário real navegando na API

    // 1. health check
    const hello = http.get(`${BASE_URL}/users/hello`)
    check(hello, { "hello: status 200": (r) => r.status === 200 })

    // 2. listagem
    const users = http.get(`${BASE_URL}/users?page=0&size=20`)
    check(users, { "users: stats 200": (r) => r.status === 200 })

    // busca
    const search = http.post(
        `${BASE_URL}/users/search`,
        JSON.stringify({ city: "São Paulo"}),
        { headers: { 'Content-Type': 'application/json' } }
    )
    check(search, { "search: status 200": (r) => r.status === 200 })

    // pausa entre iterações - simula tempo de "pensar" do usuário
    // remover isso aumenta agressividade do teste
    sleep(1)
}