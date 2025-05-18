import pytest
from app import crud

@pytest.fixture
def mock_firestore(mocker):
    # Mocka o 'db' que é importado dentro do módulo crud
    return mocker.patch("app.crud.db")

def test_create_task(mock_firestore):
    mock_tasks_collection = (
        mock_firestore
        .collection.return_value
        .document.return_value
        .collection.return_value
    )

    mock_add = mock_tasks_collection.add
    mock_add.return_value = ("mock_id", None)

    user_id = "user123"
    task_data = {"title": "Test Task", "completed": False}

    result = crud.create_task(user_id, task_data)

    mock_add.assert_called_once_with(task_data)
    assert result[0] == "mock_id"

def test_list_tasks(mock_firestore, mocker):
    mock_task = mocker.Mock()
    mock_task.to_dict.return_value = {"title": "Test Task", "completed": False}
    mock_stream = [mock_task]

    (
        mock_firestore
        .collection.return_value
        .document.return_value
        .collection.return_value
        .stream
        .return_value
    ) = mock_stream

    user_id = "user123"
    tasks = crud.list_tasks(user_id)

    assert isinstance(tasks, list)
    assert tasks[0]["title"] == "Test Task"
