import aiohttp
import asyncio

# Function to fetch posts for a user
async def get_posts(session, user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}/posts"
    async with session.get(url) as response:
        return await response.json()

# Function to fetch todos for a user
async def get_todos(session, user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}/todos"
    async with session.get(url) as response:
        return await response.json()

# Function to fetch all users
async def get_users():
    try:
        # Fetch users' data from the API
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jsonplaceholder.typicode.com/users') as response:
                users = await response.json()

                # Map users data to the desired format
                formatted_users = [
                    {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'phone': user['phone']
                    }
                    for user in users
                ]

                # Fetch and add posts and todos for each user
                users_with_posts_and_todos = []
                for user in formatted_users:
                    posts = await get_posts(session, user['id'])
                    todos = await get_todos(session, user['id'])

                    # Map posts and todos to the desired format
                    formatted_posts = []
                    for post in posts:
                        formatted_posts.append({
                            'title': post['title'],
                            'body': post['body']
                        })

                    formatted_todos = []
                    for todo in todos:
                        formatted_todos.append({
                            'title': todo['title']
                        })

                    # Add posts and todos to the user object
                    user_with_posts_and_todos = {
                        **user,
                        'posts': formatted_posts,
                        'todos': formatted_todos
                    }
                    users_with_posts_and_todos.append(user_with_posts_and_todos)

                # return all users with their posts and todos in a list
                return users_with_posts_and_todos
    except Exception as error:
        print('Error:', error)
        raise error

# Function to print users' data to the console
async def print_users_data():
    try:
        users = await get_users()
        print(users)
    except Exception as error:
        print('Error:', error)

# Main function
async def main():
    await print_users_data()

# Entry point
if __name__ == '__main__':
    asyncio.run(main())