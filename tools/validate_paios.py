import sys
from paios_cli import main

if __name__== '__main__':
    sys.argv[1:]=['validate']+sys.argv[1:]
    main()
