import Fastify from "fastify";
import postgres from "postgres";

interface User {
  id: string;
  name: string;
  email: string;
  city: string;
  country: string;
  age: number;
  active: boolean;
  created_at: Date;
}

interface SearchRequest {
  name?: string;
  city?: string;
}

const db = postgres(process.env.DATABASE_URL ?? "postgres://bench:bench123@localhost:5432/benchmark?sslmode=disable", {
  max: 20,
  idle_timeout: 30,
});

const app = Fastify({ logger: false });

app.get("/hello", async () => {
  return { message: "ok", stack: "node-fastify" };
});

app.get<{ Querystring: { page?: string; size?: string } }>("/users", async (req, reply) => {
  const page = Math.max(0, parseInt(req.query.page ?? "0"));
  let size = parseInt(req.query.size ?? "20");
  if (size < 1) size = 20;
  if (size > 100) size = 100;

  const users = await db<User[]>`
    SELECT * FROM users
    WHERE active = true
    ORDER BY created_at DESC
    LIMIT ${size} OFFSET ${page * size}
  `;

  return reply.send(users);
});

app.post<{ Querystring: { page?: string; size?: string }; Body: SearchRequest }>(
  "/users/search",
  async (req, reply) => {
    const page = Math.max(0, parseInt(req.query.page ?? "0"));
    let size = parseInt(req.query.size ?? "20");
    if (size < 1) size = 20;
    if (size > 100) size = 100;

    const { name, city } = req.body ?? {};

    const users = await db<User[]>`
      SELECT * FROM users
      WHERE active = true
      ${name ? db`AND name ILIKE ${"%" + name + "%"}` : db``}
      ${city ? db`AND city ILIKE ${"%" + city + "%"}` : db``}
      ORDER BY created_at DESC
      LIMIT ${size} OFFSET ${page * size}
    `;

    return reply.send(users);
  }
);

const port = parseInt(process.env.PORT ?? "8080");

app.listen({ port, host: "0.0.0.0" }, (err) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`Fastify running on port ${port}`);
});