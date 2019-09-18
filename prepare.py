import pip
import pip._internal

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package, '--user'])

# Example
if __name__ == '__main__':
    install('pyglet')
