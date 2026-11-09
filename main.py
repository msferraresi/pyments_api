import sys
from src import create_app
environment = 'development'

def main():
    global environment
    if len(sys.argv) > 1:
        if sys.argv[1]  == 'prod':
            environment = 'production'
            
    app_instance=create_app(environment)
    app_instance.run(host='0.0.0.0', port=5001)
    
if __name__ == '__main__':
    main()
