from flask import Flask, render_template, request
import os, uuid
from hide import hideImage, show
import datetime
from delete import deletefile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	folder = os.path.join('./static/encode/')
	old_duration = 120
	deletefile(folder, old_duration)
	if request.method == "POST":
		id=uuid.uuid1()
		file = request.files['file']
		msg = request.form.get('msg')
		# check if file and msg empty 
		if file.filename == '':
			error = '<div class="alert alert-warning">File empty!</div>'
			return render_template('index.html', errors=error)
		if msg == '':
			error = '<div class="alert alert-warning">Message is empty!</div>'
			return render_template('index.html', errors=error)
		# check if extension allowed
		allowed_ext = ['.JPG', '.JPEG', '.PNG', '.jpg', '.jpeg', '.png']
		name, ext = os.path.splitext(file.filename)
		if ext not in  allowed_ext:
			error = '<div class="alert alert-warning">'+ext+' is not supported<div>'
			return render_template('index.html', errors=error) 

		# now save uploaded image
		os.mkdir('./static/encode/'+str(id))
		file.save(os.path.join('./static/encode/'+str(id)+'/'+file.filename))
		# name, ext = os.path.splitext(file.filename)
		output_dir = './static/encode/'+str(id)+'/'
		output = output_dir+str(id)+'.png'
		image = output_dir+file.filename
		encode = hideImage(image, msg, output)
		if os.path.isfile(output):
			encoded_img = "<center><a href="+output+" download><h3>Download Encoded Image</h3></a></center>"
			return render_template('index.html', encoded_img=encoded_img)
		else:
			error = "<div class='alert alert-warning'>Something went wrong!</div>"
			return render_template('index.html', encoded_img=encoded_img)

	return render_template('index.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
	folder = os.path.join('./static/decoder/')
	old_duration = 600
	deletefile(folder, old_duration)
	if request.method == "POST":
		id = uuid.uuid1()
		file = request.files['file']
		# check if file exist
		if file.filename == '':
			error = '<div class="alert alert-warning">File empty!</div>'
			return render_template('decode.html', errors=error)
		# check allowed extension
		allowed_ext = ['.PNG', '.png']
		name, ext = os.path.splitext(file.filename)
		if ext not in  allowed_ext:
			error = '<div class="alert alert-warning">'+ext+' is not supported</div>'
			return render_template('decode.html', errors=error)
		# now save uploaded image
		os.mkdir('./static/decoder/'+str(id))
		img = './static/decoder/'+str(id)+'/'+file.filename
		file.save(os.path.join(img))
		# decode
		output = show(img)	
		if output == '':
			decoded = ""
			return render_template('decode.html', decoded=decoded)
		else:
			decoded = output
			return render_template('decode.html', decoded=decoded)

	return render_template('decode.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
	if request.method == "POST":
		name = request.form.get('name')
		email = request.form.get('email')
		feedback = request.form.get('feedback')

		if name == '' or email == '' or feedback == '':
			error = "<div class='alert alert-warning'>Field(s) cannot be empty!</div>"
			return render_template('feedback.html', errors=error)

		date = datetime.datetime.now()
		f = open("feedback.txt", "a")
		f.write("\n")
		f.write("______________________________________________")
		f.write("\n")
		f.write(str(date))
		f.write("\n")
		f.write("Name: "+name)
		f.write("\n")
		f.write("Email: "+email)
		f.write("\n")
		f.write("Feedback: "+feedback)
		f.write('\n')
		f.close()

		print(date)

		# print(name, email)
		# print('\n')
		# print(feedback)

	return render_template('feedback.html')

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)