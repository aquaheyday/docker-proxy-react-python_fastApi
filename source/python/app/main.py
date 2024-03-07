from fastapi import FastAPI
import pymysql

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

""" @app.get("/")
async def first_get():
    example = session.query(Test).all()
    return example

@app.get("/api/test")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q} """

# 데이터베이스 연결 설정
def get_db_connection():
    return pymysql.connect(
        host='api-maria',
        user='fastapi',
        password='fastapi',
        db='fastapi',
        cursorclass=pymysql.cursors.DictCursor
    )

""" @app.get("/api/tests/")
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
        connection.close() """

@app.get("/api/companyList")
def read_item():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql1 = "SELECT name FROM deliveryCompany WHERE type = 'kr'"
            cursor.execute(sql1)

            resultKr = cursor.fetchall()

            sql2 = "SELECT name FROM deliveryCompany WHERE type = 'en'"
            cursor.execute(sql2)

            resultEn = cursor.fetchall()

            return {"kr": resultKr, "en": resultEn}
    finally:
        connection.close()


@app.get("/api/ratePlan")
def read_item():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT type, monthlyPlan, selectLimit, daySameSelectLimit, trackingPageYn FROM ratePlan"
            cursor.execute(sql)

            result = cursor.fetchall()

            return result
    finally:
        connection.close()

@app.get("/api/description")
def read_item():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM inquiry"
            cursor.execute(sql)

            result = cursor.fetchall()

        return result
    finally:
        connection.close()


class Item(BaseModel):
    name: str
    number: str
    email: str = None
    type: str = None
    description: str
    agreeYn: str = 'N'

@app.post("/api/description")
async def create_item(item: Item):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO inquiry (name, number, email, type, description, agreeYn) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (item.name, item.number, item.email, item.type, item.description, item.agreeYn))

            connection.commit()
            id = cursor.lastrowid

            return id
    finally:
        connection.close()
