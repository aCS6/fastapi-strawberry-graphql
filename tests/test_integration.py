import pytest
from httpx import AsyncClient


# ==============================================================================
# USER QUERIES
# ==============================================================================

class TestUserQueries:
    """Tests for User-related GraphQL queries."""

    @pytest.mark.asyncio
    async def test_me_query(self, client, auth_headers):
        """Test the 'me' query returns the authenticated user."""
        query = """
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
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert data["data"]["me"] is not None
        assert data["data"]["me"]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_me_query_unauthenticated(self, client):
        """Test that 'me' query fails without authentication."""
        query = """
        query {
            me {
                id
                username
            }
        }
        """
        response = await client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Not authenticated" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_user_query_by_id(self, client, auth_headers, db_session):
        """Test the 'user(id)' query to get a specific user."""
        from users.models import User
        # Get any existing user ID
        user = db_session.query(User).first()
        
        query = f"""
        query {{
            user(id: {user.id}) {{
                id
                username
                email
                bio
                avatarUrl
            }}
        }}
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert data["data"]["user"]["id"] == user.id

    @pytest.mark.asyncio
    async def test_user_query_not_found(self, client, auth_headers):
        """Test the 'user(id)' query with an invalid ID."""
        query = """
        query {
            user(id: 99999) {
                id
                username
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "not found" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_users_query(self, client, auth_headers):
        """Test the 'users' query returns all users."""
        query = """
        query {
            users {
                id
                username
                email
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert len(data["data"]["users"]) > 0

    @pytest.mark.asyncio
    async def test_user_with_posts(self, client, auth_headers, db_session):
        """Test fetching a user with their posts (nested query)."""
        from users.models import User
        user = db_session.query(User).first()
        
        query = f"""
        query {{
            user(id: {user.id}) {{
                id
                username
                posts {{
                    id
                    content
                    createdAt
                }}
            }}
        }}
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert "posts" in data["data"]["user"]
        assert isinstance(data["data"]["user"]["posts"], list)

    @pytest.mark.asyncio
    async def test_user_with_followers_and_following(self, client, auth_headers, db_session):
        """Test fetching a user with their followers and following."""
        from users.models import User
        user = db_session.query(User).first()
        
        query = f"""
        query {{
            user(id: {user.id}) {{
                id
                username
                followers {{
                    id
                    username
                }}
                following {{
                    id
                    username
                }}
            }}
        }}
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert "followers" in data["data"]["user"]
        assert "following" in data["data"]["user"]


# ==============================================================================
# POST QUERIES
# ==============================================================================

class TestPostQueries:
    """Tests for Post-related GraphQL queries."""

    @pytest.mark.asyncio
    async def test_posts_query(self, client, auth_headers):
        """Test the 'posts' query returns all posts."""
        query = """
        query {
            posts {
                id
                content
                imageUrl
                createdAt
                updatedAt
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert isinstance(data["data"]["posts"], list)

    @pytest.mark.asyncio
    async def test_post_query_by_id(self, client, auth_headers, db_session):
        """Test the 'post(id)' query to get a specific post."""
        from posts.models import Post
        post = db_session.query(Post).first()
        
        if post:
            query = f"""
            query {{
                post(id: {post.id}) {{
                    id
                    content
                    imageUrl
                    createdAt
                }}
            }}
            """
            response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            assert "errors" not in data, f"Query failed: {data.get('errors')}"
            assert data["data"]["post"]["id"] == post.id

    @pytest.mark.asyncio
    async def test_post_query_not_found(self, client, auth_headers):
        """Test the 'post(id)' query with an invalid ID."""
        query = """
        query {
            post(id: 99999) {
                id
                content
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "not found" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_posts_with_filter_by_author(self, client, auth_headers, db_session):
        """Test the 'posts(authorId)' query to filter by author."""
        from users.models import User
        user = db_session.query(User).first()
        
        query = f"""
        query {{
            posts(authorId: {user.id}) {{
                id
                content
                author {{
                    id
                    username
                }}
            }}
        }}
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        # All posts should be from this author
        for post in data["data"]["posts"]:
            if post["author"]:
                assert post["author"]["id"] == user.id

    @pytest.mark.asyncio
    async def test_posts_with_filter_by_tag(self, client, auth_headers, db_session):
        """Test the 'posts(tagId)' query to filter by tag."""
        from tags.models import Tag
        tag = db_session.query(Tag).first()
        
        if tag:
            query = f"""
            query {{
                posts(tagId: {tag.id}) {{
                    id
                    content
                    tags {{
                        id
                        name
                    }}
                }}
            }}
            """
            response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_post_with_author(self, client, auth_headers):
        """Test fetching posts with their authors (nested query)."""
        query = """
        query {
            posts {
                id
                content
                author {
                    id
                    username
                    email
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_post_with_comments(self, client, auth_headers):
        """Test fetching posts with their comments (nested query)."""
        query = """
        query {
            posts {
                id
                content
                comments {
                    id
                    content
                    author {
                        username
                    }
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_post_with_likes(self, client, auth_headers):
        """Test fetching posts with their likes (nested query)."""
        query = """
        query {
            posts {
                id
                content
                likes {
                    id
                    user {
                        username
                        avatarUrl
                    }
                }
                likesCount
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_post_with_tags(self, client, auth_headers):
        """Test fetching posts with their tags (nested query)."""
        query = """
        query {
            posts {
                id
                content
                tags {
                    id
                    name
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_feed_query(self, client, auth_headers):
        """Test the 'feed' query returns posts from followed users."""
        query = """
        query {
            feed {
                id
                content
                author {
                    id
                    username
                }
                createdAt
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert isinstance(data["data"]["feed"], list)

    @pytest.mark.asyncio
    async def test_complex_post_query(self, client, auth_headers):
        """Test a complex query with multiple nested fields."""
        query = """
        query {
            posts {
                id
                content
                likes {
                    user {
                        avatarUrl
                        username
                    }
                }
                tags {
                    name
                }
                comments {
                    content
                    author {
                        bio
                    }
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert data["data"]["posts"] is not None


# ==============================================================================
# COMMENT QUERIES
# ==============================================================================

class TestCommentQueries:
    """Tests for Comment-related GraphQL queries."""

    @pytest.mark.asyncio
    async def test_comments_query(self, client, auth_headers):
        """Test the 'comments' query returns all comments."""
        query = """
        query {
            comments {
                id
                content
                createdAt
                updatedAt
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert isinstance(data["data"]["comments"], list)

    @pytest.mark.asyncio
    async def test_comment_query_by_id(self, client, auth_headers, db_session):
        """Test the 'comment(id)' query to get a specific comment."""
        from comments.models import Comment
        comment = db_session.query(Comment).first()
        
        if comment:
            query = f"""
            query {{
                comment(id: {comment.id}) {{
                    id
                    content
                    createdAt
                }}
            }}
            """
            response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            assert "errors" not in data, f"Query failed: {data.get('errors')}"
            assert data["data"]["comment"]["id"] == comment.id

    @pytest.mark.asyncio
    async def test_comment_query_not_found(self, client, auth_headers):
        """Test the 'comment(id)' query with an invalid ID."""
        query = """
        query {
            comment(id: 99999) {
                id
                content
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "not found" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_comments_by_post_id(self, client, auth_headers, db_session):
        """Test the 'comments(postId)' query to filter by post."""
        from posts.models import Post
        post = db_session.query(Post).first()
        
        if post:
            query = f"""
            query {{
                comments(postId: {post.id}) {{
                    id
                    content
                    author {{
                        username
                    }}
                }}
            }}
            """
            response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_comment_with_author(self, client, auth_headers):
        """Test fetching comments with their authors."""
        query = """
        query {
            comments {
                id
                content
                author {
                    id
                    username
                    email
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_comment_with_post(self, client, auth_headers):
        """Test fetching comments with their parent post."""
        query = """
        query {
            comments {
                id
                content
                post {
                    id
                    content
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_comment_with_replies(self, client, auth_headers):
        """Test fetching comments with their replies."""
        query = """
        query {
            comments {
                id
                content
                parentComment {
                    id
                    content
                }
                replies {
                    id
                    content
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_comment_with_likes(self, client, auth_headers):
        """Test fetching comments with their likes."""
        query = """
        query {
            comments {
                id
                content
                likes {
                    id
                    user {
                        username
                    }
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"


# ==============================================================================
# TAG QUERIES
# ==============================================================================

class TestTagQueries:
    """Tests for Tag-related GraphQL queries."""

    @pytest.mark.asyncio
    async def test_tags_query(self, client, auth_headers):
        """Test the 'tags' query returns all tags."""
        query = """
        query {
            tags {
                id
                name
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"
        assert isinstance(data["data"]["tags"], list)

    @pytest.mark.asyncio
    async def test_tags_with_posts(self, client, auth_headers):
        """Test fetching tags with their associated posts."""
        query = """
        query {
            tags {
                id
                name
                posts {
                    id
                    content
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"


# ==============================================================================
# MUTATION TESTS
# ==============================================================================

class TestMutations:
    """Tests for GraphQL mutations."""

    @pytest.mark.asyncio
    async def test_login_mutation_success(self, client, db_session):
        """Test successful login mutation."""
        from users.models import User
        from auth import get_password_hash
        
        # Ensure test user exists
        user = db_session.query(User).filter(User.username == "testuser").first()
        if not user:
            user = User(
                username="testuser",
                email="test@example.com",
                password_hash=get_password_hash("12345"),
                bio="Test User",
                avatar_url="http://example.com/avatar.jpg"
            )
            db_session.add(user)
            db_session.commit()
        
        mutation = """
        mutation {
            login(input: {username: "testuser", password: "12345"}) {
                accessToken
                tokenType
                user {
                    id
                    username
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Mutation failed: {data.get('errors')}"
        assert data["data"]["login"]["accessToken"] is not None
        assert data["data"]["login"]["tokenType"] == "bearer"
        assert data["data"]["login"]["user"]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_login_mutation_invalid_username(self, client):
        """Test login mutation with invalid username."""
        mutation = """
        mutation {
            login(input: {username: "nonexistentuser", password: "wrongpass"}) {
                accessToken
                tokenType
            }
        }
        """
        response = await client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Invalid username or password" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_login_mutation_invalid_password(self, client, db_session):
        """Test login mutation with invalid password."""
        from users.models import User
        from auth import get_password_hash
        
        # Ensure test user exists
        user = db_session.query(User).filter(User.username == "testuser").first()
        if not user:
            user = User(
                username="testuser",
                email="test@example.com",
                password_hash=get_password_hash("12345"),
                bio="Test User",
                avatar_url="http://example.com/avatar.jpg"
            )
            db_session.add(user)
            db_session.commit()
        
        mutation = """
        mutation {
            login(input: {username: "testuser", password: "wrongpassword"}) {
                accessToken
                tokenType
            }
        }
        """
        response = await client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Invalid username or password" in data["errors"][0]["message"]


# ==============================================================================
# N+1 QUERY TESTS
# ==============================================================================

class TestNPlusOneOptimization:
    """Tests to verify N+1 query optimization with dataloaders."""

    @pytest.mark.asyncio
    async def test_posts_with_authors_n_plus_one(self, client, auth_headers):
        """Test that posts with authors doesn't cause N+1 issues."""
        query = """
        query {
            posts {
                id
                author {
                    username
                }
                comments {
                    id
                    author {
                        username
                    }
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"

    @pytest.mark.asyncio
    async def test_deeply_nested_query(self, client, auth_headers):
        """Test a deeply nested query for performance."""
        query = """
        query {
            posts {
                id
                content
                author {
                    id
                    username
                    posts {
                        id
                        content
                    }
                }
                comments {
                    id
                    content
                    author {
                        id
                        username
                    }
                    replies {
                        id
                        content
                    }
                }
            }
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" not in data, f"Query failed: {data.get('errors')}"


# ==============================================================================
# EDGE CASE TESTS
# ==============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_unauthenticated_posts_query(self, client):
        """Test that posts query fails without authentication."""
        query = """
        query {
            posts {
                id
                content
            }
        }
        """
        response = await client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Not authenticated" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_unauthenticated_comments_query(self, client):
        """Test that comments query fails without authentication."""
        query = """
        query {
            comments {
                id
                content
            }
        }
        """
        response = await client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Not authenticated" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_unauthenticated_tags_query(self, client):
        """Test that tags query fails without authentication."""
        query = """
        query {
            tags {
                id
                name
            }
        }
        """
        response = await client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Not authenticated" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_unauthenticated_feed_query(self, client):
        """Test that feed query fails without authentication."""
        query = """
        query {
            feed {
                id
                content
            }
        }
        """
        response = await client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "Not authenticated" in data["errors"][0]["message"]

    @pytest.mark.asyncio
    async def test_invalid_graphql_query(self, client, auth_headers):
        """Test handling of invalid GraphQL syntax."""
        query = """
        query {
            invalid_field_name
        }
        """
        response = await client.post("/graphql", json={"query": query}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data

    @pytest.mark.asyncio
    async def test_empty_query(self, client, auth_headers):
        """Test handling of empty query."""
        response = await client.post("/graphql", json={"query": ""}, headers=auth_headers)
        # Empty query returns 400 Bad Request in Strawberry/GraphQL
        assert response.status_code == 400

