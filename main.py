from src import create_app

app = create_app('development')

if __name__ == '__main__':
	app.run(port=app.config['PORT_APP'])