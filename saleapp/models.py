from sqlalchemy import Column, Integer, String, Boolean, Float,Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from saleapp import app
from saleapp import db
from flask_login import UserMixin
from enum import Enum as UserEnum


class Basemodel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    USER =2

class User(Basemodel, UserMixin):
    name = Column(String(50), nullable=False)
    username= Column(String(50), nullable=False, unique=True)
    passworld = Column(String(50), nullable= False)
    avatar=Column(String(250))
    email= Column(String(50))
    active= Column(Boolean, default=True)
    join_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole) , default=UserRole.USER)
    receipts= relationship('Receipt', backref= 'user', lazy=True)
    comments= relationship('Comment', backref='user', lazy=True)


    def __str__(self):
        return self.name




class Category(Basemodel):
    __tablename__= 'category'

    name = Column(String(120), nullable=False)
    products=relationship('Product', backref='category', lazy=False) #backref=category: lấy tên catergory đai diện

    def __str__(self):
        return self.name
class Product(Basemodel):
    __tablename__= 'product'

    name= Column(String(150), nullable=False)

    price=Column(Float, default=0)
    image= Column(String(100))
    description = Column(String(250))
    active= Column(Boolean, default=True)
    created_date= Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_detail = relationship('ReceiptDetail', backref='product', lazy= True )
    comments= relationship('Comment' , backref = 'product', lazy= True)

    def __str__(self):
        return self.name

class Comment(Basemodel):
    content= Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable= False)
    user_id = Column(Integer, ForeignKey(User.id), nullable= False)
    create_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.content

class Receipt(Basemodel):
    created_date= Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details= relationship('ReceiptDetail', backref='receipt', lazy= True )

class ReceiptDetail(db.Model):
    receipt_id= Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key= True)
    product_id= Column(Integer, ForeignKey(Product.id), nullable=False, primary_key= True)
    quantity= Column(Integer, default=0)
    unit_price= Column(Integer, default=0)






if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        #c1= Category(name="Nhiệt độ")
        #c2= Category(name="Khoảng cách")
        #c3= Category(name="Khối lượng")

        #db.session.add(c1)
        #db.session.add(c2)
        #db.session.add(c3)
        #db.session.commit()






