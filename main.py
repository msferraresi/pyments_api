import sys
from src import create_app

environment = 'development'

def main():
    global environment
    if len(sys.argv) > 1:
        if sys.argv[1]  == 'prod':
            environment = 'production'
            
    app=create_app(environment)
    app.run()

if __name__ == '__main__':
    main()
