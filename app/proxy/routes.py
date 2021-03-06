from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from . import proxy_bp
from .. import db

from .forms import ProxyForm
from ..models import Proxy, get_or_create


@proxy_bp.route('/')
def index():
    proxies = Proxy.query.all()
    return render_template('proxy/index.html', title='Index', proxies=proxies)


@proxy_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ProxyForm()
    if form.validate_on_submit():
        host = form.host.data
        port = form.port.data

        instance, is_created = get_or_create(model=Proxy, host=host, port=port)
        if is_created:
            flash('Proxy was added.', category='success')
        return redirect(url_for('proxy.index'))
    return render_template('proxy/add.html', title='Adding proxy host', form=form)


@proxy_bp.route('/edit/<int:proxy_id>', methods=['GET', 'POST'])
@login_required
def edit(proxy_id):
    proxy = Proxy.query.filter_by(id=proxy_id).first()
    form = ProxyForm(formdata=request.form, obj=proxy)
    if form.validate_on_submit():
        proxy.host = form.host.data
        proxy.port = form.port.data
        db.session.add(proxy)
        try:
            db.session.commit()
            flash('Proxy was edited.', category='success')
        except IntegrityError as e:
            flash('Сan not edit proxy, because the same proxy exist in database.', category='danger')
            return redirect(url_for('proxy.index'))
        return redirect(url_for('proxy.index'))
    return render_template('proxy/edit.html', title='Editing proxy host', form=form, proxy=proxy)


@proxy_bp.route('/delete/<int:proxy_id>', methods=['GET', 'POST'])
@login_required
def delete(proxy_id):
    proxy = Proxy.query.filter_by(id=proxy_id).first()
    db.session.delete(proxy)
    db.session.commit()
    flash('Proxy was deleted.', category='info')
    return redirect(url_for('proxy.index'))
