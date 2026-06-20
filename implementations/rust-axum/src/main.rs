
use axum::{
    Json,
    Router,
    extract::{Query, State},
    http::StatusCode,
    routing::{get, post},
};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use sqlx::{PgPool, postgres::PgPoolOptions};
use std::{env, sync::Arc};
use uuid::Uuid;
 


#[derive(Debug, Serialize, sqlx::FromRow)]
pub struct User {
    pub id: Uuid,
    pub name: String,
    pub email: String,
    pub city: String,
    pub country: String,
    pub age: i32,
    pub active: bool,
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Deserialize)]
pub struct SearchRequest {
    pub name: Option<String>,
    pub city: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct Pagination {
    #[serde(default)]
    pub page: i64,
    #[serde(default = "default_size")]
    pub size: i64,
}

fn default_size() -> i64 { 20 }

// Estado compartilhado da aplicação
#[derive(Clone)]
pub struct AppState {
    pub db: Arc<PgPool>,
}


// Entry point
#[tokio::main]
async fn main() {
    let database_url = env::var("DATABASE_URL")
        .unwrap_or_else(|_| "postgres://bench:bench123@localhost:5432/benchmark?sslmode=disable".to_string());

    let port = env::var("PORT")
        .unwrap_or_else(|_| "8080".to_string());

    // PgPool cria um pool de conexões com o Postgres.
    // connect_lazy_with é async — espera a conexão ser estabelecida.
    // Em Rust, .await suspende a função até o Future resolver,
    // liberando a thread para outras tasks enquanto espera.
    // .expect() faz o programa crashar com a mensagem se der erro —
    // adequado para erros fatais de inicialização.
    let pool = PgPoolOptions::new()
        .max_connections(20)
        .connect(&database_url)
        .await
        .expect("Falha ao conectar no PostgreSQL");


    let state = AppState {
        db: Arc::new(pool),
    };

    // Router do Axum — equivalente ao r := gin.Default() do Go
    // .with_state() injeta o AppState em todos os handlers
    let app = Router::new()
        .route("/users/hello", get(hello))
        .route("/users", get(list_users))
        .route("/users/search", post(search_users))
        .with_state(state);

    let addr = format!("0.0.0.0:{}", port);
    println!("Servidor rodando em {}", addr);

    // Axum usa o tokio::net::TcpListener para abrir a porta
    let listener = tokio::net::TcpListener::bind(&addr)
        .await
        .expect("Falha ao abrir a porta");

    axum::serve(listener, app)
        .await
        .expect("Falha ao iniciar o servidor");

}

// =============================================================
// HANDLERS
// =============================================================
// Cada handler é uma função async que recebe extractors do Axum
// e retorna uma resposta.
//
// Extractors são tipos especiais que o Axum "extrai" da requisição:
//   State(state)    → extrai o AppState que injetamos no router
//   Query(params)   → extrai query string (?page=0&size=20)
//   Json(body)      → extrai e deserializa o body JSON
//
// O tipo de retorno usa Result<Json<T>, (StatusCode, Json<Value>)>
// que significa: ou retorna JSON de sucesso, ou retorna um status
// de erro com um JSON explicando o problema.

async fn hello() -> Json<Value> {
    Json(json!({
        "message": "ok",
        "stack": "rust-axum"
    }))
}

async fn list_users(
    State(state): State<AppState>,
    Query(params): Query<Pagination>,
) -> Result<Json<Vec<User>>, (StatusCode, Json<Value>)> {

    let offset = params.page * params.size;

    let users = sqlx::query_as::<_, User>(
        "SELECT id, name, email, city, country, age, active, created_at
        FROM users
        WHERE active = true
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2"
    )
    // $1, $2 são placeholders do Postgres (equivalente ao ? do MySQL)
    .bind(params.size)
    .bind(offset)
    .fetch_all(state.db.as_ref()) // fetch_all retorna Vec<User>
    .await
    // map_err converte o erro do sqlx para o formato que o handler retorna
    .map_err(|e| (
        StatusCode::INTERNAL_SERVER_ERROR,
        Json(json!({ "error": e.to_string() }))
    ))?;

    Ok(Json(users))
}

// POST /users/search
async fn search_users(
    State(state): State<AppState>,
    Query(params): Query<Pagination>,
    Json(body): Json<SearchRequest>,
) -> Result<Json<Vec<User>>, (StatusCode, Json<Value>)> {

    let offset = params.page * params.size;

    // Em Rust não existe interpolação dinâmica de SQL segura fora
    // de crates especializados. A abordagem mais limpa com sqlx
    // é usar uma query com todos os parâmetros e tratar None/Some
    // com IS NULL OR — mesmo padrão que usamos no Spring e FastAPI.

    let users = sqlx::query_as::<_, User>(
        "SELECT id, name, email, city, country, age, active, created_at
        FROM users
        WHERE active = true
        
        AND ($1::text IS NULL OR LOWER(name) LIKE LOWER(CONCAT('%', $1, '%')))
        AND ($2::text IS NULL OR LOWER(city) LIKE LOWER(CONCAT('%', $2, '%')))
        ORDER BY created_at DESC
        LIMIT $3 OFFSET $4"
    )
    .bind(body.name)
    .bind(body.city)
    .bind(params.size)
    .bind(offset)
    .fetch_all(state.db.as_ref())
    .await
    .map_err(|e| (
        StatusCode::INTERNAL_SERVER_ERROR,
        Json(json!({ "error": e.to_string() }))
    ))?;

    Ok(Json(users))
}