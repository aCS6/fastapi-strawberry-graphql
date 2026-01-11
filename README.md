# Social Media GraphQL API Demo

A GraphQL API demonstration project built with **FastAPI** and **Strawberry GraphQL** for a seminar organized by [**Innovative Skills**](https://innovativeskillsbd.com/) to understand GraphQL concepts. This project focuses primarily on **GraphQL Queries**.

---

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Strawberry GraphQL** - Python GraphQL library
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (file-based)
- **uv** - Package manager

---

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Seed the Database

This creates sample data including users, posts, comments, tags, likes, and follows:

```bash
uv run python init_db.py
```

Output: `Database seeded successfully with users, posts, likes, and follows!`

### 3. Run the Project

```bash
uv run python main.py
```

The server will start at `http://localhost:8000`

### 4. Access GraphQL Playground

Open your browser and navigate to:

```
http://localhost:8000/graphql
```

This opens the **GraphiQL IDE** where you can explore and test queries.

---

## Running Tests

Run the integration tests using pytest:

```bash
uv run pytest tests/test_integration.py -v
```

---

## GraphQL Queries Reference

> **Note:** Most queries require authentication. Use the `login` mutation first to get a token, then add the `Authorization: Bearer <token>` header.

### Authentication

#### Login (Mutation)

```graphql
mutation {
  login(input: { username: "<username>", password: "12345" }) {
    accessToken
    tokenType
    user {
      id
      username
      email
    }
  }
}
```

---

### User Queries

#### Get Current User

```graphql
query {
  me {
    id
    username
    email
    bio
    avatarUrl
    createdAt
  }
}
```

#### Get User by ID

```graphql
query {
  user(id: 1) {
    id
    username
    email
    bio
    avatarUrl
    createdAt
  }
}
```

#### Get All Users

```graphql
query {
  users {
    id
    username
    email
  }
}
```

#### Get User with Posts

```graphql
query {
  user(id: 1) {
    id
    username
    posts {
      id
      content
      createdAt
    }
  }
}
```

#### Get User with Followers & Following

```graphql
query {
  user(id: 1) {
    id
    username
    followers {
      id
      username
    }
    following {
      id
      username
    }
  }
}
```

---

### Post Queries

#### Get Post by ID

```graphql
query {
  post(id: 1) {
    id
    content
    imageUrl
    createdAt
    updatedAt
    likesCount
  }
}
```

#### Get All Posts

```graphql
query {
  posts {
    id
    content
    createdAt
    likesCount
  }
}
```

#### Get Feed (Posts from followed users)

```graphql
query {
  feed {
    id
    content
    author {
      username
    }
    createdAt
  }
}
```

#### Get Post with Author

```graphql
query {
  post(id: 1) {
    id
    content
    author {
      id
      username
      avatarUrl
    }
  }
}
```

#### Get Post with Comments

```graphql
query {
  post(id: 1) {
    id
    content
    comments {
      id
      content
      author {
        username
      }
      createdAt
    }
  }
}
```

#### Get Post with Likes

```graphql
query {
  post(id: 1) {
    id
    content
    likesCount
    likes {
      id
      user {
        username
      }
    }
  }
}
```

#### Get Post with Tags

```graphql
query {
  post(id: 1) {
    id
    content
    tags {
      id
      name
    }
  }
}
```

---

### Comment Queries

#### Get Comment by ID

```graphql
query {
  comment(id: 1) {
    id
    content
    authorId
    postId
    parentCommentId
    createdAt
    updatedAt
  }
}
```

#### Get All Comments

```graphql
query {
  comments {
    id
    content
    author {
      username
    }
  }
}
```

#### Get Comment with Replies (Nested Comments)

```graphql
query {
  comment(id: 1) {
    id
    content
    replies {
      id
      content
      author {
        username
      }
    }
  }
}
```

#### Get Comment with Parent Comment

```graphql
query {
  comment(id: 10) {
    id
    content
    parentComment {
      id
      content
      author {
        username
      }
    }
  }
}
```

---

### Tag Queries

#### Get All Tags

```graphql
query {
  tags {
    id
    name
  }
}
```

#### Get Tag with Posts

```graphql
query {
  tags {
    id
    name
    posts {
      id
      content
      author {
        username
      }
    }
  }
}
```

---

### Complex Nested Queries

#### Full Post Details

```graphql
query {
  post(id: 1) {
    id
    content
    imageUrl
    createdAt
    likesCount
    author {
      id
      username
      avatarUrl
    }
    tags {
      name
    }
    comments {
      id
      content
      author {
        username
      }
      replies {
        content
        author {
          username
        }
      }
    }
    likes {
      user {
        username
      }
    }
  }
}
```

#### User Profile with All Related Data

```graphql
query {
  user(id: 1) {
    id
    username
    email
    bio
    avatarUrl
    createdAt
    followers {
      id
      username
    }
    following {
      id
      username
    }
    posts {
      id
      content
      likesCount
      tags {
        name
      }
      comments {
        content
      }
    }
  }
}
```

---

## API Endpoints

| Endpoint    | Description              |
| ----------- | ------------------------ |
| `/`         | Health check / Info      |
| `/graphql`  | GraphQL API & Playground |
| `/docs`     | OpenAPI Documentation    |

---

## Sample Data

After seeding, the database contains:

- **3 Users** - with random credentials (password: `12345` for all)
- **60 Posts** - 20 per user
- **6 Tags** - `technology`, `programming`, `graphql`, `python`, `javascript`, `ai`
- **120+ Comments** - with nested replies
- **Random Likes** - users liking posts
- **Follow Relationships** - users following each other

---

## Project Structure

```
app/
├── main.py           # FastAPI app entry point
├── database.py       # Database configuration
├── init_db.py        # Database seeding script
├── auth.py           # Authentication utilities
├── dataloaders.py    # DataLoaders for N+1 optimization
├── users/            # User domain
│   ├── models.py     # SQLAlchemy models
│   ├── schemas.py    # GraphQL types
│   ├── queries.py    # Query definitions
│   ├── mutations.py  # Mutation definitions
│   └── resolvers.py  # Resolver functions
├── posts/            # Post domain
├── comments/         # Comment domain
├── tags/             # Tag domain
├── likes/            # Like domain
└── tests/            # Integration tests
    ├── conftest.py
    └── test_integration.py
```
