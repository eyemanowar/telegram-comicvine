import pytest
from database_helper import DbHandler

@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setattr('database_helper.SQLITE_PATH', str(tmp_path / 'test.db'))
    db = DbHandler()
    db.init_db()
    return db

def test_add_and_get(db):
    db.add_user(1, "tester")
    db.add_series(1,"Batman")
    assert db.get_reading_list(1) == ['Batman'], f'Received list is {db.get_reading_list(1)}, when expected ["Batman"]'

def test_unique_user(db):
    db.add_user(1, "tester")
    db.add_user(1, 'tester')
    assert db.get_user(1) == [1], f'Received users list {db.get_user(1,)}, expected [1]'

def test_remove_series(db):
    db.add_user(1, "tester")
    db.add_series(1,"Batman")
    db.remove_series(1, 'Batman')
    assert db.get_reading_list(1) == [], f'Received list is {db.get_reading_list(1)}, when expected []'
