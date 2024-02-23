from umleditor.mvc_controller import Controller
from umleditor.mvc_controller.cli_controller import CLI_Controller

def debug_main():
    app = CLI_Controller()
    app.run()

def main():
    try:
        app = CLI_Controller()
        app.run()
    except KeyboardInterrupt:
        # This handles ctrl+C
        pass
    except EOFError:
        # This handles ctrl+D
        pass
    except Exception as e:
        # Never expect errors to be caught here
        print(e)

if __name__ == '__main__':
    if not __debug__:
        debug_main()
    else:
        main()