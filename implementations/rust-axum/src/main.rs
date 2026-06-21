
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
use sqlx::{PgPool, QueryBuilder, postgres::{PgConnectOptions, PgPoolOptions}};
use std::{env, str::FromStr, sync::Arc};
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

    let connect_options = PgConnectOptions::from_str(&database_url)
        .expect("URL inválida")
        .statement_cache_capacity(100);

    let pool = PgPoolOptions::new()
        .max_connections(20)
        .connect_with(connect_options)
        .await
        .expect("Falha ao conectar no PostgreSQL");

    let state = AppState {
        db: Arc::new(pool),
    };

    let app = Router::new()
        .route("/users/hello", get(hello))
        .route("/users", get(list_users))
        .route("/users/search", post(search_users))
        .with_state(state);

    let addr = format!("0.0.0.0:{}", port);
    println!("Servidor rodando em {}", addr);

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

    let mut builder = QueryBuilder::new(
        "SELECT id, name, email, city, country, age, active, created_at
        FROM users WHERE active = true"
    );

    if let Some(name) = &body.name {
        if !name.is_empty() {
            builder.push(" AND name ILIKE ");
            builder.push_bind(format!("%{}%", name));
        }
    }

    if let Some(city) = &body.city {
        if !city.is_empty() {
            builder.push(" AND city ILIKE ");
            builder.push_bind(format!("%{}%", city));
        }
    }

    builder.push(" ORDER BY created_at DESC LIMIT ");
    builder.push_bind(params.size);
    builder.push(" OFFSET ");
    builder.push_bind(offset);

    let users = builder
        .build_query_as::<User>()
        .fetch_all(state.db.as_ref())
        .await
        .map_err(|e| (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({ "error": e.to_string() }))
        ))?;

    Ok(Json(users))
}