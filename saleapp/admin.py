from saleapp import app,db
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category,Product, UserRole
from flask_login import current_user, logout_user
from flask import redirect
import utils
from flask import request
from datetime import datetime


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class ProductView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_labels = {
        'name': 'Tên Sp',
        'price':'giá',
        'description':'Mô Tả'
    }

class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw=request.args.get('kw')
        from_date=request.args.get('from_date')
        to_date= request.args.get('to_date')
        year= request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw,
                                                     from_date=from_date,
                                                     to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',stats=utils.category_stats())

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

admin=Admin(app=app,
            name="E-commerce Administration",
            template_mode='bootstrap4',
            index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout b'))

