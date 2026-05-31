import http from "k6/http"
import { check, sleep } from "k6"
import { BASE_URL, thresholds } from "../config.js"

// =============================================================
// CENÁRIO: Steady State
// =============================================================
// Carga constante e moderada por tempo prolongado.
// Objetivo: medir comportamento estável — latência consistente,
// ausência de memory leaks, throughput sustentado.
//
// 200 VUs sem sleep = pressão real e contínua no backend.
// Sem sleep, cada VU dispara uma nova requisição assim que
// a anterior termina — sem descanso.
// =============================================================

export const options = {
    vus: 200,
    duration: "30s",
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