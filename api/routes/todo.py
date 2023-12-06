from fastapi import APIRouter, HTTPException, status
from api.models.todo import Todo
from api.schemas.todo import GetTodo, PostTodo, PutTodo

todo_router = APIRouter(prefix='/api', tags=['Todo'])


@todo_router.get('/')
async def all_todos():
    data = Todo.all()
    return await GetTodo.from_queryset(data)


@todo_router.post('/')
async def post_todo(body: PostTodo):
    row = await Todo.create(**body.model_dump(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)


@todo_router.put('/{key}')
async def update_todo(key: int, body: PutTodo):
    data = body.model_dump(exclude_unset=True)
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    await Todo.filter(id=key).update(**data)
    return await GetTodo.from_queryset_single(Todo.get(id=key))


@todo_router.delete('/{key}')
async def delete_todo(key: int):
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    await Todo.filter(id=key).delete()
    return 'Todo deleted successfully!'
