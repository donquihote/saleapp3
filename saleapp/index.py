import math

from flask import render_template, request, redirect, url_for, session, jsonify
from saleapp import app, login
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from saleapp.models import UserRole

@app.route("/")

def home():

    cate_id= request.args.get('category_id')
    kw= request.args.get('keyword')
    page= request.args.get('page',1)
    prods=utils.load_product(cate_id=cate_id, kw=kw, page=int(page))
    couter = utils.count_product()
    return render_template('index.html',
                           products=prods,
                           pages= math.ceil(utils.count_product()/app.config['PAGE_SIZE'])
                           )

@app.route("/register" , methods= ['get','post'])
def user_register():
    err_msg=""
    if request.method.__eq__('POST'):
        name=request.form.get('name')
        username=request.form.get('username')
        passworld= request.form.get('passworld')
        email = request.form.get('email')
        confirm=request.form.get('confirm')
        avatar_path = None

        try:
            if passworld.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res= cloudinary.uploader.upload(avatar)
                    avatar_path=res['secure_url']

                utils.add_user(name=name, passworld=passworld, username=username, email=email, avatar= avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg="mật khẩu xac nhan ko khop"
        except Exception as ex:
            err_msg= "He Thong co loi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg=''
    if request.method.__eq__('POST'):
        username=request.form.get('username')
        passworld=request.form.get('passworld')

        user= utils.check_login(username=username, passworld=passworld)

        if user:
            login_user(user=user)
            next= request.args.get('next','home')
            return redirect(url_for(next))
        else:
            err_msg= "Username hoặc pass Không chinh xác"


    return render_template('layout/login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():

    username = request.form.get('username')
    passworld = request.form.get('passworld')

    user = utils.check_login(username=username,
                             passworld=passworld,
                             role=UserRole.ADMIN)

    if user:
        login_user(user=user)
    return redirect('/admin')

@app.route('/user_logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.context_processor
def common_response():
    return {
        'category': utils.load_catergory(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)



@app.route("/products")
def products_list():

    cate_id =request.args.get ("category_id")
    kw= request.args.get("keyword")

    from_price=request.args.get("from_price")
    to_price=request.args.get("to_price")

    prod = utils.load_product(cate_id=cate_id, kw=kw,from_price=from_price, to_price=to_price)

    return render_template('products.html',
                           products=prod)




@app.route('/api/add-cart' , methods=['post'])
def add_to_cart():
    data=request.json
    id= str(data.get('id'))
    name = data.get('name')
    price= data.get('price')


    cart = session.get('cart')
    if not cart:
        cart={}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data=request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart =session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route('/api/pay', methods = ['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code':200})

@app.route('/api/delete-cart/<product_id>', methods= ['delete'])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product=utils.get_product_by_id(product_id)
    comments=utils.get_comment(product_id=product_id,
                                page= int(request.args.get('page', 1)))

    return render_template('product_detail.html',
                           comments=comments,
                           product=product,
                           pages = math.ceil(utils.count_comment(product_id=product_id) /app.config['COMMENT-SIZE']))


@app.route('/api/comments', methods= ['post'])
@login_required
def add_comment():
    data = request.json
    content = data.get('content')
    product_id = data.get('product_id')

    try:
        c = utils.add_comment(content=content, product_id=product_id)
    except:
        return {'status': 404, 'err_msg': 'Chuong trinh dang bi loi!!!'}

    return  {'status' : 201, 'comment': {
        'id': c.id,
        'content': c.content,
        'created_date': c.create_date,
        'user': {
            'username': current_user.username,
            'avatar': current_user.avatar
        }
    }}

@app.route('/cart')
def cart():
    return render_template('cart.html',
                           stats=utils.count_cart(session.get('cart')))

if __name__=='__main__':
    from saleapp.admin import *

    app.run(debug=True)