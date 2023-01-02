from flask import Flask,render_template,redirect,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy import String, Integer,Text, DateTime, Boolean
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db=SQLAlchemy(app)

class Usuarios(db.Model):
	id = Column(Integer,primary_key=True)
	user = Column(String(12),nullable=False)
	username = Column(String(35),default="")
	password = Column(Text,nullable=False)
	permision = Column(Integer,nullable=False)

class Contacto(db.Model):
	id = db.Column(Integer,primary_key=True)
	nombre = Column(String(35),nullable=False)
	email = Column(Text,nullable=False)
	telefono = Column(Integer,nullable=False)
	mensaje = Column(String(455),default="")
	tiempo_consulta = Column(DateTime,nullable=False)
	atendido = Column(Boolean,default=False)

class Citas(db.Model):
	id = db.Column(Integer,primary_key=True)
	nombre = Column(String(35),nullable=False)
	documento = Column(Integer,nullable=False)
	email = Column(Text,nullable=False)
	telefono = Column(Integer,nullable=False)
	fecha_cita = Column(Text)
	hora_cita = Column(Text)
	tiempo_consulta = Column(DateTime,nullable=False)
	servicio = Column(Text,nullable=False)
	modalidad = Column(Text,nullable=False)
	atendido = Column(Boolean,default=False)

class Afiliaciones(db.Model):
	id = db.Column(Integer,primary_key=True)
	nombre = Column(String(35),nullable=False)
	email = Column(Text,nullable=False)
	programa = Column(Text,nullable=False)
	tiempo_consulta = Column(DateTime,nullable=False)
	atendido = Column(Boolean,default=False)

@app.route('/')
def inicio():
	return render_template("index.html", titulo="inicio")

@app.route('/cont/', methods=['GET','POST'])
def requercontacto():
	if request.method == 'POST':
		form = request.form.to_dict()
		db.session.add(Contacto(nombre=form['name'],email=form['email'],telefono=form['phone'],mensaje=form['message'],tiempo_consulta=datetime.datetime.now(),atendido=False))
		db.session.commit()
	else:
		abort(404)
	
	return "<script>alert('Su petición se ha realizado con éxito.'); window.location='/';</script>"

@app.route('/consultorio/citas')
def citas():
	return render_template("citas.html",titulo="citas")
		
@app.route('/consultorio/citas/cont/', methods=['GET','POST'])
def pedircita():
	if request.method == 'POST':
		form = request.form.to_dict()
		db.session.add(Citas(nombre=form['name'],documento=form['cedula'],email=form['email'],telefono=form['phone'],fecha_cita=form['date'],hora_cita=form['time'],tiempo_consulta=datetime.datetime.now(),servicio=form['servicio'],modalidad=form['modal'],atendido=False))
		db.session.commit()
	else:
		abort(404)
	
	return "<script>alert('Su petición se ha realizado con éxito.'); window.location='/';</script>"

@app.route('/info/cookies')
def cookies():
	return render_template('cookies.html', titulo="Cookies")

@app.route('/info/legaldict')
def policies():
	return render_template('policies.html', titulo="Declaraciones")

@app.route('/afiliacion/<dend>')
def afiliacion(dend):
	if dend == "familia":
		seedTitle = "Plan familiar"
		seedContent = "Con el plan familiar, puede acceder a todos los servicios nutricionales cancelando una única cuota mensual. Además, obtendrá beneficios de descuento en cursos y productos nutricionales, así como  prioridad de información en las promociones disponibles. Este plan acoje al afiliado, cónyugue, hijos y padres adultos mayores."
	elif dend == "abuelos":
		seedTitle = "Plan abuelos"
		seedContent = "Consulta y asesoría nutricional y alimentaria dirigida a hogares geriatricos; incluye valoración inicial, seguimientos trimestrales, consultas prioritarias, capacitaciones a residentes, familiares y colaboradores. Asesoría al servicio de alimentos, manejo de dietas y talleres de nutrición a directores."
	elif dend == "corp":
		seedTitle = "Plan corporativo"
		seedContent = "Dirigido a empresas; incluye ferias nutricionales, consulta individual y talleres de alimentación saludable."
	elif dend == "ninos":
		seedTitle = "Nutrición de cero a doce"
		seedContent= "Programa nutricional de control del patrón de crecimiento y seguimiento de la gestión alimentaria del menor desde el nacimiento hasta el primer año de edad. Incluye talleres de crecimiento y desarrollo y consultas individuales."
	elif dend == "nutripro":
		seedTitle = "Curso nutri profiláctico"
		seedContent = "Programa dirigido a madres gestantes desde el primer trimestre de gestación. El objetivo es formar a las madres en todo lo referente a su cuidado nutricional y el del bebé, esquemas alimentarios adecuados, además de hacerle un acompañamiento durante su proceso prenatal."
	elif dend == "taller_fam":
		seedTitle = "Talleres familiares"
		seedContent = "Jornadas educativas dirigidas a familiares y cuidadores sobre temas de cuidado nutricional y esquemas alimentarios indicados a los pacientes crónicos. Está incluido en el plan familiar."
	else:
		abort(404)
	
	return render_template("afiliacion.html",titulo="Afiliacion",seedContent=seedContent,seedTitle=seedTitle)

@app.route('/afiliacion/cont/', methods=['GET','POST'])
def afiliados():
	if request.method == 'POST':
		form = request.form.to_dict()
		db.session.add(Afiliaciones(nombre=form['name'],email=form['email'],programa=form['orus'],tiempo_consulta=datetime.datetime.now(),atendido=False))
		db.session.commit()
	else:
		abort(404)

	return "<script>alert('Su petición se ha realizado con éxito.'); window.location='/';</script>"

@app.route('/consultorio')
def consultorio():
	if session and 'username' in session:
		usuarios=Usuarios.query.all()
		contacto=Contacto.query.all()
		citas=Citas.query.all()
		afiliaciones=Afiliaciones.query.all()
		return render_template("admin.html",username=session['username'],usuarios=usuarios,contactos=contacto,citas=citas,afiliaciones=afiliaciones)
	else:
		return "Bienvenido. por favor, <a href='/consultorio/login'>Inicie sesion</a>"

@app.route('/consultorio/login')
def login():
	if session and 'username' in session:
		return redirect('/consultorio')
	else:
		return """<br><br><div align='center'><form action='/consultorio/auth' method='POST'>
			<h1>Login Account</h1>
			<table>
			<tr><td><input type='text' name='user' placeholder='username' required=''></td></tr>
			<tr><td><input type='password' name='pass' placeholder='password' required=''></td></tr>
			<tr><td><input type='submit' value='Ingresar'></td></tr>
			</table>
		</form></div>"""

@app.route('/consultorio/logout')
def logout():
	if session and 'username' in session:
		session.pop('username')
		return redirect('/consultorio')
	else:
		return "No hay una sesion iniciada <a href='/consultorio'>Volver</a>"

@app.route('/consultorio/auth',methods=['POST'])
def auth():
	query = Usuarios.query.filter_by(user=request.form['user'],password=request.form['pass']).first()
	if query:
		session['username'] = query.username
		session['permision'] = query.permision
		return redirect('/consultorio')
	else:
		return "<script>alert('usuario o contraseña incorrectas');window.location = '/consultorio/login';</script>"

@app.route('/consultorio/session/add',methods=['POST'])
def new_user():
	if session and request.method == 'POST' and session['permision'] >= 8:
		if request.form['pass'] == request.form['ver']:
			db.session.add(Usuarios(user=request.form['user'],username=request.form['username'],password=request.form['pass'],permision=5))
			db.session.commit()
			return redirect('/consultorio')
		else:
			return "<script>alert('contraseña no coincide');window.location = '/consultorio';</scrip>"
	else:
		return "<script>alert('No tiene permisos suficientes para esta operacion');window.location = '/consultorio';</script>"

@app.route('/consultorio/session/edit/<aidi>')
def edit_user(aidi):
	if session and 'username' in session:
		query = Usuarios.query.filter_by(id=aidi).first()
		return """<div align='center'><form action="/consultorio/session/change/{}" method='POST'>
		<h2>Nuevo usuario</h2>
		<input type='text' name='user' placeholder='{}' required=''><br>
		<input type='text' name='username' placeholder='{}'><br>
		<input type='password' name='pass' placeholder='Contraseña' required=''><br>
		<input type='password' name='ver' placeholder='Verificar contraseña' required=''><br>
		<input type='number' name='permisions' placeholder='{}' required=''><br>
		<input type='submit' value='Enviar'>
	</form></div>""".format(query.id,query.user,query.username,query.permision)
	else:
		return redirect('/consultorio')

@app.route('/consultorio/session/change/<aidi>',methods=['POST'])
def change_user(aidi):
	if request.method == 'POST' and session:
		if request.form['pass'] == request.form['ver'] and session['permision'] >=9:
			query = Usuarios.query.filter_by(id=aidi).update({'user':request.form['user'],'username':request.form['username'],'password':request.form['pass'],'permision':request.form['permisions']})
			db.session.commit()
			return "<script>alert('Modificacion realizada con exito');window.location = '/consultorio';</script>"
		else:
			return "<script>alert('No tiene permisos suficientes para esta operacion');window.location = '/consultorio';</script>"
	else:
		return redirect('/consultorio')

@app.route('/consultorio/session/delete/<aidi>')
def delete_user(aidi):
	if session and session['permision'] >=9:
		Usuarios.query.filter_by(id=aidi).delete()
		db.session.commit()
		return redirect('/consultorio')
	else:
		return "<script>alert('No tiene permisos suficientes para esta operacion');window.location = '/consultorio';</script>"

@app.route('/consultorio/contactos/activate/<aidi>')
def contact_alta(aidi):
	if session:
		if session['permision'] >=4:
			Contacto.query.filter_by(id=aidi).update({'atendido':True})
			db.session.commit()
			return redirect('/consultorio')
		else:
			return "<script>alert('No tiene permisos suficientes para esta operacion');window.location = '/consultorio';</script>"
	else:
		return redirect('/consultorio')

@app.route('/consultorio/afiliacion/activate/<aidi>')
def afilia_alta(aidi):
	if session and session['permision'] >=4:
		Afiliaciones.query.filter_by(id=aidi).update({'atendido':True})
		db.session.commit()
		return redirect('/consultorio')	
	else:
		return "<script>alert('No tiene permisos suficientes para esta operacion');window.location = '/consultorio';</script>"

if __name__ == "__main__":
	db.create_all()
	app.run(debug=False, host="192.168.0.28", port=8080)
