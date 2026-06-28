// Porta recebida via variável de ambiente
// Uso: k6 run -e PORT=8081 scenarios/steady.js
export const BASE_URL = `http://localhost:${__ENV.PORT || 8080}`


// Thresholds - critérios de sucesso/falha
// O teste falha se esses limites forem ultrapassados
export const thresholds = {
    // 95% das requisições devem responder em menos de 500ms
    http_req_duration: ['p(95)<500'],

    // Menos de 1% de erros
    http_req_failed: ['rate<0.01'],
}

export const summaryTrendStats = ["avg", "med", "max", "p(90)", "p(95)", "p(99)"];