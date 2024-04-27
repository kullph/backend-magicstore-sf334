from fastapi import APIRouter, Form
import asyncpg
import os

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)

@router.get("/revenue")
async def revenue():
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
    )

    revenue = 0

    products = await conn.fetch(
        '''
        SELECT sales_quantity ,price FROM product;
        '''
    )

    for item in products:
        revenue += item['sales_quantity'] * item['price']

    return revenue

@router.get("/topproduct")
async def topproduct():
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
    )

    temp = []
    products = await conn.fetch(
        '''
        SELECT * FROM product;
        '''
    )

    for item in products:
        img = await conn.fetch(
        '''
        SELECT img FROM img WHERE product_id = $1;
        '''
        ,item['id']
        )
        new_item = dict(item)
        new_item['img'] = img
        temp.append(new_item)

    return sorted(temp, key=lambda x: x["sales_quantity"], reverse=True)
@router.get("/detail")
async def detail():
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
    )

    user = await conn.fetch(
        '''
        SELECT id FROM users;
        '''
    )

    products = await conn.fetch(
        '''
        SELECT id FROM product;
        '''
    )

    review = await conn.fetch(
        '''
        SELECT id FROM review;
        '''
    )

    category = await conn.fetch(
        '''
        SELECT id FROM category;
        '''
    )

    element = await conn.fetch(
        '''
        SELECT id FROM element;
        '''
    )

    return {
        "status":True,
        "message":{
            "user":len(user),
            "products":len(products),
            "review":len(review),
            "category":len(category),
            "element":len(element)
        }
    }

@router.get("/totalsales")
async def totalsales(): 
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
    )

    result = 0
    products = await conn.fetch(
        '''
        SELECT sales_quantity FROM product;
        '''
    )

    for item in products:
        result += item['sales_quantity']

    return result

@router.get("/ordercompleted")
async def ordercompleted():
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
    )

    products = await conn.fetch(
        '''
        SELECT id FROM ordered;
        '''
    )

    return len(products)

@router.get("/graph")
async def graph():
    pass
