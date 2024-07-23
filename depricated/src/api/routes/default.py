from fastapi import APIRouter

router = APIRouter()


@router.get("/hello", name="default:say-hello")
async def say_hello():
    return {"Hello": "World!"}


@router.get("/add", name="default:add")
async def add(first: int, second: int):
    return {
        "first": first,
        "second": second,
        "result": first + second,
    }
