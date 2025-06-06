from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):
    """Test creating a new user."""
    with mock_db_time(model=User) as time:
        new_user = User(
            username='testuser', email='test@mail.com', password='password'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert user.username == 'testuser'
    assert asdict(user) == {
        'id': 1,
        'username': 'testuser',
        'email': 'test@mail.com',
        'password': 'password',
        'created_at': time,
        'updated_at': time,
    }
