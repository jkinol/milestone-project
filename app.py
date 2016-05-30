from flask import Flask,render_template,request,redirect
from bokeh.plotting import figure, output_file, show, save
import Quandl
app = Flask(__name__)

app.variables={}

@app.route('/main_page',methods=['GET','POST'])
def main_page():
	if request.method == 'GET':
		return render_template('stockinfo.html')
	else:
		app.variables['symbol']=request.form['stock'].upper()
		app.variables['features']=request.form.getlist('features')

		data = Quandl.get('WIKI/' + app.variables['symbol'])
		x_axis_dates = data.index
		output_file('/templates/lines.html')
		p = figure(x_axis_label='Date',y_axis_label='Stock Price ($)',plot_width=500, plot_height=500,x_axis_type = 'datetime')
		colors = ['blue','red','green','purple']
		for ii, item in enumerate(app.variables['features']):
			y = data[item]
			p.line(x_axis_dates,y,legend=item, color = colors[ii])
		save(p,'./templates/lines.html')
		return render_template('graphs.html',symbol=app.variables['symbol'])

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
