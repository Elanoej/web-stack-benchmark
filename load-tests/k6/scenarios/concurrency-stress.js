import http from "k6/http"
import { handleSummary } from "../summary.js"
import { check } from "k6"
import { BASE_URL, summaryTrendStats } from "../config.js"

// =============================================================
// CENÁRIO: Concurrency Stress
// =============================================================
// O cenário mais agressivo da suíte. Projetado para estressar a
// concorrência ao máximo, usando http.batch() para disparar
// TODAS as requisições simultaneamente dentro de cada VU.
//
// Diferentemente dos demais cenários (que fazem 3 requisições
// sequenciais por VU), este dispara as 3 em paralelo,
// multiplicando a concorrência efetiva:
//
//   VUs × requisições simultâneas por VU = concorrência real
//
//   Ex: 1500 VUs × 3 (batch) = 4500 requisições simultâneas
//
// Isso testa até onde cada stack consegue manter conexões
// simultâneas — connection pool, thread pool, file descriptors,
// e escalabilidade horizontal.
//
// Estágios:
//   0   →  100 VUs em 10s   (aquecimento)
//   100 →  500 VUs em 15s   (carga moderada)
//   500 → 1000 VUs em 20s   (alta concorrência)
//   1000→ 1500 VUs em 20s   (concorrência extrema)
//   1500→    0 VUs em 10s   (recuperação)
//
// O que observar:
//   - Em qual estágio cada stack começa a rejeitar conexões
//   - Degradação de latência (p95, p99) em cada patamar
//   - Stacks bloqueantes (thread-pool) vs reativas (event-loop)
//   - Saturação do connection pool do PostgreSQL
//   - Uso de CPU e memória do processo do backend
// =============================================================

export const options = {
    stages: [
        { duration: "10s", target: 100  },
        { duration: "15s", target: 500  },
        { duration: "20s", target: 1000 },
        { duration: "20s", target: 1500 },
        { duration: "10s", target: 0    },
    ],
    // Toleramos degradação maior — este cenário existe para
    // ENCONTRAR os limites do backend, não para passar.
    thresholds: {
        http_req_duration: ["p(95)<5000"],
        http_req_failed:   ["rate<0.05"],
    },
    summaryTrendStats,
}

// Parâmetros variáveis para evitar cache de query no PostgreSQL
// e forçar execução real do banco em cada requisição
const PAGES = [0, 1, 2, 3, 5, 10]
const CITIES = [
    "São Paulo", "Rio de Janeiro", "Belo Horizonte",
    "Salvador", "Brasília", "Fortaleza",
    "Curitiba", "Recife", "Porto Alegre",
]

export default function () {
    const page = PAGES[Math.floor(Math.random() * PAGES.length)]
    const city = CITIES[Math.floor(Math.random() * CITIES.length)]

    // 3 requisições simultâneas por VU via batch
    const responses = http.batch([
        { method: "GET",  url: `${BASE_URL}/hello` },
        { method: "GET",  url: `${BASE_URL}/users?page=${page}&size=20` },
        {
            method: "POST",
            url: `${BASE_URL}/users/search`,
            body: JSON.stringify({ city }),
            params: { headers: { "Content-Type": "application/json" } },
        },
    ])

    check(responses[0], { "hello: status 200": (r) => r.status === 200 })
    check(responses[1], { "users: status 200": (r) => r.status === 200 })
    check(responses[2], { "search: status 200": (r) => r.status === 200 })
}

export { handleSummary }
