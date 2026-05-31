import http from "k6/http"
import { check, sleep } from "k6"
import { BASE_URL, thresholds } from "../config.js"

// =============================================================
// CENÁRIO: Spike
// =============================================================
// Carga normal → pico repentino e brutal → volta ao normal.
// Objetivo: medir resiliência — o backend se recupera?
// Quantos erros durante o pico? A latência normaliza depois?
//
// Esse cenário simula situações reais:
// um post viral, Black Friday, notificação push em massa.
//
// Estágios:
//   0   →  50 VUs em 10s   (baseline normal)
//   50  →  50 VUs por 20s  (sustenta o normal)
//   50  → 500 VUs em 5s    (PICO — subida abrupta)
//   500 → 500 VUs por 10s  (sustenta o pico)
//   500 →  50 VUs em 5s    (volta ao normal)
//   50  →  50 VUs por 20s  (recuperação — backend voltou?)
//   50  →   0 VUs em 5s    (fim)
//
// O que observar:
//   - Taxa de erro durante o pico (http_req_failed)
//   - Latência p99 durante o pico
//   - Se a latência volta ao normal após o pico
// =============================================================

export const options = {
    stages: [
        { duration: "10s", target: 50  },  // aquecimento
        { duration: "20s", target: 50  },  // baseline estável
        { duration: "5s",  target: 500 },  // PICO — subida em 5s
        { duration: "10s", target: 500 },  // sustenta o pico
        { duration: "5s",  target: 50  },  // volta ao normal
        { duration: "20s", target: 50  },  // recuperação
        { duration: "5s",  target: 0   },  // fim
    ],
    // Thresholds mais permissivos para o spike —
    // alguma degradação durante o pico é esperada e aceitável.
    // O que não pode acontecer é não se recuperar.
    thresholds: {
        http_req_duration: ["p(95)<2000"], // até 2s no pico
        http_req_failed:   ["rate<0.05"],  // até 5% de erro
    },
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

    // Pequena pausa no spike para não saturar o SO com
    // conexões TCP abertas demais ao mesmo tempo
    sleep(0.1)
}