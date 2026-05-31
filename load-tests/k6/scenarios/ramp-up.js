import http from "k6/http"
import { check } from "k6"
import { BASE_URL, thresholds } from "../config.js"

// =============================================================
// CENÁRIO: Ramp-up
// =============================================================
// Aumenta a carga gradualmente em estágios.
// Objetivo: encontrar o ponto onde cada backend começa a
// degradar — latência sobe, erros aparecem, throughput cai.
//
// Leitura: compare em qual estágio cada backend "dobra".
// MVC pode degradar antes do WebFlux por esgotamento de threads.
//
// Estágios:
//   0  → 50  VUs em 10s  (aquecimento)
//   50 → 150 VUs em 20s  (carga moderada)
//   150→ 300 VUs em 20s  (carga alta)
//   300→ 500 VUs em 20s  (stress)
//   500→ 0   VUs em 10s  (recuperação)
// =============================================================

export const options = {
    stages: [
        { duration: "10s", target: 50  },  // aquecimento
        { duration: "20s", target: 150 },  // carga moderada
        { duration: "20s", target: 300 },  // carga alta
        { duration: "20s", target: 500 },  // stress
        { duration: "10s", target: 0   },  // recuperação
    ],
    thresholds,
}

export default function () {
    const hello = http.get(`${BASE_URL}/users/hello`)
    check(hello, { "hello: status 200": (r) => r.status === 200 })

    const users = http.get(`${BASE_URL}/users?page=0&size=20`)
    check(users, { "users: status 200": (r) => r.status === 200 })

    const search = http.post(
        `${BASE_URL}/users/search`,
        JSON.stringify({ city: "São Paulo" }),
        { headers: { "Content-Type": "application/json" } }
    )
    check(search, { "search: status 200": (r) => r.status === 200 })
}