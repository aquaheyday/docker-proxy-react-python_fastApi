from fastapi import FastAPI
import pymysql

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

@app.get("/")
async def first_get():
    example = session.query(Test).all()
    return example

@app.get("/api/test")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# 데이터베이스 연결 설정
def get_db_connection():
    return pymysql.connect(
        host='api-maria',
        user='fastapi',
        password='fastapi',
        db='fastapi',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/api/tests/")
def read_items():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM users"
            cursor.execute(sql)

            # 결과 가져오기
            result = cursor.fetchall()
            return result
    finally:
        # 데이터베이스 연결 종료
        connection.close()