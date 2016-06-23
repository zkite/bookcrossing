from bookcrossing.email.email import send_async_email
from bookcrossing.forms.register_form import RegistrationForm
from bookcrossing.models.user import UserModel
from bookcrossing.views.users.base_user import BaseUserView
from flask import flash, url_for, render_template, redirect


class UserView(BaseUserView):

    def get(self):
        form = RegistrationForm()
        return render_template('registration.html', form=form)

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            user_list = ['login', 'email', 'first_name', 'last_name', 'office', 'phone', 'password']
            user_dict = {
                'login': form.login.data,
                'email': form.email.data,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'office': form.office.data,
                'phone': form.phone.data,
                'password': form.password.data
            }
            self.create_model(UserModel, user_list, user_dict)
            flash('You can now login.')
            flash('A confirmation email has been sent to you by email.')
            send_async_email(form.email.data,
                             'Your Account in Bookcrossing',
                             'email/greeting',
                             first_name=form.first_name.data)
            return redirect(url_for('login'))
        return render_template('registration.html', form=form)



    def put(self):
        pass

    def delete(self):
        pass



# def registration():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = UserModel(login=form.login.data,
#                          email=form.email.data,
#                          first_name=form.first_name.data,
#                          last_name=form.last_name.data,
#                          office=form.office.data,
#                          phone_number=form.phone.data,
#                          password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('You can now login.')
#         flash('A confirmation email has been sent to you by email.')
#         send_async_email(user.email,
#                          'Your Account in Bookcrossing',
#                          'email/greeting',
#                          user=user)
#         return redirect(url_for('login'))
#     return render_template('registration.html', form=form)