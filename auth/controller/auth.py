from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from service.auth import AuthService
import asyncpg
from datetime import timedelta, datetime
from model.model import RawJSONData

router = APIRouter(
    prefix="/auth",
    tags=["auth and usermgmt"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/reg")
async def register(email:str=Form(...),password:str=Form(...)):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
        )
    
    check = await conn.fetch(
    '''
    SELECT * FROM authen WHERE email = $1;
    '''
    , email)

    if len(check) == 0:
        authen_id = await conn.fetchval(
            '''
            INSERT INTO authen(email, password) VALUES($1, $2) RETURNING id;
            '''
            , email, AuthService.hash_password(password)
            )
        
        user_id = await conn.fetchval(
            '''
            INSERT INTO users(authen_id, firstname, lastname, point) VALUES($1, $2, $3, $4) RETURNING id;
            '''
            , authen_id, "temp_firstname", "temp_lastname", 100
            )
        
        await conn.execute(
            '''
            INSERT INTO "delivery_source"(user_id, detail, phone, province, district, subdistrict, zipcode) VALUES($1, $2, $3, $4, $5, $6, $7)
            '''
            , user_id, "temp", "temp", "temp", "temp", "temp", "temp"
            )

        await conn.close()
        return {"status":True,"message":""}
    else:
        await conn.close()
        return {"status":False,"message":"Email already in use"}

@router.post("/login")
async def login(email:str=Form(...),password:str=Form(...)):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    check = await conn.fetch(
        '''
    SELECT * FROM authen WHERE email = $1;
    ''', email)

    await conn.close()

    if len(check) == 0:
        return {"status":False,"message":"Email is not registered"}
    elif len(check) == 1:
        token = AuthService.create_token(str(check[0]["id"]), timedelta(minutes=59))
        return {"status":True,"message":{"access_token": token, "token_type":"bearer","exp":"30 minutes"}}
    else:
        return {"status":False,"message":"IDK why it pass this condition it must be miracle(db admin fault LOL)"}

@router.post("/Profile")
async def profileEdit(
    token:str = Depends(oauth2_scheme),
    firstname:str=Form(...),
    lastname:str=Form(...),
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    await conn.execute(
        '''
        UPDATE users SET firstname = $2, lastname = $3 WHERE id = $1
        '''
        , int(id), firstname, lastname
    )

    return {"status":True,"message":""}

@router.get("/Profile")
async def profileGet(
    token:str = Depends(oauth2_scheme)
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    profile = await conn.fetch(
    '''
    SELECT * FROM users WHERE id = $1;
    '''
    , int(id)
    )

    return {"status":True,"message":profile[0]}

@router.post("/Delivery")
async def deliveryEdit(
    token:str = Depends(oauth2_scheme),
    detail:str=Form(...),
    phone:str=Form(...),
    province:str=Form(...),
    district:str=Form(...),
    subdistrict:str=Form(...),
    zipcode:str=Form(...),
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    await conn.execute(
        '''
        UPDATE delivery_source SET detail = $2, phone = $3, province = $4, district = $5, subdistrict = $6, zipcode = $7 WHERE user_id = $1
        '''
        , int(id), detail, phone, province, district, subdistrict, zipcode
    )

    return {"status":True,"message":""}

@router.get("/Delivery")
async def deliveryget(
    token:str = Depends(oauth2_scheme)
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    delivery = await conn.fetch(
    '''
    SELECT * FROM delivery_source WHERE user_id = $1;
    '''
    , int(id)
    )

    return {"status":True,"message":delivery[0]}

@router.post("/Cart")
async def cartAdd(
    token:str = Depends(oauth2_scheme),
    product_id:int=Form(...),
    quantity:int=Form(...),
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )
    await conn.execute(
        '''
            INSERT INTO cart(user_id,product_id,quantity) VALUES($1,$2,$3);
        '''
        , int(id), product_id, quantity
    )

    return {"status":True,"message":""}

@router.get("/Cart")
async def cartGet(
    token:str = Depends(oauth2_scheme)
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
        )
    
    result = await conn.fetch(
        '''SELECT product_id, quantity FROM cart WHERE user_id = $1;'''
        , int(id)
    )

    return {"status":True,"message":result}

@router.delete("/Cart")
async def cartClear(
    token:str = Depends(oauth2_scheme)
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
        )
    
    await conn.execute(
        '''DELETE FROM cart WHERE user_id = $1;'''
        , int(id)
    )

    return {"status":True,"message":""}

# mount
# @router.post("/editCart")
# async def cartMount(
#     token:str = Depends(oauth2_scheme),
#     data:list=Form(...)
# ):
#     for item in data:
#         pass

#     return "x"

@router.post("/Ordered")
async def orderedAdd(
    data:RawJSONData ,
    token:str = Depends(oauth2_scheme),
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    data=data.data

    ordered_id = await conn.fetchval(
        '''
            INSERT INTO ordered(user_id, orderdate) VALUES($1, $2) RETURNING id;
            ''', 
        int(id), datetime.now(),
    )

    for item in data:
        await conn.execute(
            '''
            INSERT INTO ordered_list(ordered_id, product_id, quantity) VALUES($1, $2, $3)
            '''
            , ordered_id, item.product_id, item.quantity
        )

    return {"status":True,"message":""}

@router.get("/Ordered")
async def orderedGet(
    token:str = Depends(oauth2_scheme)
    ):
    id = AuthService.decode_jwt(token)["sub"]
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    ordered = await conn.fetch(
        '''
        SELECT * FROM ordered;
        '''
    )

    result = []

    for item in ordered:
        new_item = dict(item)
        ordered_list = await conn.fetch(
        '''
        SELECT product_id, quantity FROM ordered_list WHERE ordered_id = $1;
        '''
        ,item['id']
        )

        temp = []
        for pro in ordered_list:
            product = await conn.fetch(
                '''
                SELECT name, price FROM product WHERE id = $1;
                '''
                ,pro["product_id"]
                )
            
            new_pro = dict(pro)
            new_pro["name"] = product[0]["name"] if product else None
            new_pro["price"] = product[0]["price"] if product else None
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,pro["product_id"]
                )
            new_pro["img"] = img
            temp.append(new_pro)
        new_item["Product_list"] = temp
        result.append(new_item)

    return result

@router.post("/editPassword")
async def editPassword(
    newPass:str=Form(...),
    token:str = Depends(oauth2_scheme)
    ):
    jwt = AuthService.decode_jwt(token)

    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    await conn.execute(
            '''
            UPDATE authen SET password = $2 WHERE id=$1
            '''
            , int(jwt["sub"]), AuthService.hash_password(newPass))

    return {"status":True,"message":"Finish"}

@router.post("/editEmail")
async def editEmail(
    newMail:str=Form(...),
    token:str = Depends(oauth2_scheme)
    ):
    jwt = AuthService.decode_jwt(token)

    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    await conn.execute(
            '''
            UPDATE authen SET email = $2 WHERE id=$1
            '''
            , int(jwt["sub"]), newMail)

    return {"status":True,"message":"Finish"}

@router.post("/review")
async def review(
    token:str = Depends(oauth2_scheme),
    product_id:int=Form(...),
    detail:str=Form(...)
    ):
    score = AuthService.sentimental(detail)
    id = AuthService.decode_jwt(token)["sub"]

    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    await conn.execute(
            '''
            INSERT INTO review(user_id,product_id,detail,score) VALUES($1,$2,$3,$4);
            '''
            ,int(id), product_id, detail, score
        )



